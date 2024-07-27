
''' requirements.txt
pandas==2.2.2
psycopg[c]==3.2.1
SQLAlchemy==2.0.30
'''
import os
import sys
import pandas as pd
import sqlalchemy

def sync_table(table_name : str, interval: int, connexion_1, connexion_2, dry_run = True) -> None:
    # ATTENTION: Si le champs date contient ou non la time zone, le filtre peut nécessiter un changement
    '''
    Construction de la requête pour récupérer les données et execution pour créer 2 dataframes distincts
    '''
    # query=f"SELECT * FROM {table_name} WHERE col_date >= now()::date - interval '{interval} hours'"
    query=f"SELECT * FROM public.\"{table_name.strip()}\""
    # df_server1=pd.read_sql(query, engine=connexion_1)
    # df_server2=pd.read_sql(query, engine=connexion_2)
    df_server1=pd.read_sql(query, con=connexion_1)
    df_server2=pd.read_sql(query, con=connexion_2)
    '''
    Concatène les deux tables et supprime tout ce qui est en double.
    Il ne reste que ce qui est uniquement dans une seule des deux tables.
    '''
    df_diff_global=pd.concat([df_server1, df_server2]).drop_duplicates(keep=False)
    '''
    Cette dernière étape permet de ne récupérer que les lignes qui sont dans la table 2 mais pas dans la table 1 pour faire les insertions.
    '''
    df_diff_1=pd.merge(df_diff_global, df_server1, how='outer', indicator=True)
    rows_in_df_diff_global_not_in_df_server1 = df_diff_1[df_diff_1['_merge']=='left_only'][df_diff_global.columns]
    if not dry_run:
      print("not dry_run")
      #rows_in_df_diff_global_not_in_df_server1.to_sql(name=table_name, if_exists='append', con=connexion_1)
    '''
    Cette dernière étape permet de ne récupérer que les lignes qui sont dans la table 1 mais pas dans la table 2 pour faire les insertions.
    '''
    df_diff_2=pd.merge(df_diff_global, df_server2, how='outer', indicator=True)
    rows_in_df_diff_global_not_in_df_server2 = df_diff_2[df_diff_2['_merge']=='left_only'][df_diff_global.columns]
    if not dry_run:
      print("not dry_run")
      #rows_in_df_diff_global_not_in_df_server2.to_sql(name=table_name, if_exists='append', con=connexion_2)

    print(f"\n\n\nTable: {table_name.strip()}")
    print("Lignes presentes dans la bdd 2 mais pas dans la bdd 1")
    print(rows_in_df_diff_global_not_in_df_server1)

    print("-----------------------------------------------------")
    print("Lignes presentes dans la bdd 1 mais pas dans la bdd 2")
    print(rows_in_df_diff_global_not_in_df_server2)

'''
Point d'entrée du programme
Création des connexions pour les deux instances PG à partir des variables d'environnement
'''
hostname_1=os.environ["HOSTNAME_1"]
port_1=os.environ["PORT_1"]
user_1=os.environ["USERNAME_1"]
password_1=os.environ["PASSWORD_1"]
db_1=os.environ["DB_1"]
hostname_2=os.environ["HOSTNAME_2"]
port_2=os.environ["PORT_2"]
user_2=os.environ["USERNAME_2"]
password_2=os.environ["PASSWORD_2"]
db_2=os.environ["DB_2"]

interval=os.environ["INTERVAL"]

#conn_1=sqlalchemy.create_engine(f"psycopg://{user_1}:{password_1}@{hostname_1}:{port_1}/{db_1}")
conn_1=sqlalchemy.create_engine(f"postgresql+psycopg://{user_1}:{password_1}@{hostname_1}:{port_1}/{db_1}")
#conn_2=sqlalchemy.create_engine(f"psycopg://{user_2}:{password_2}@{hostname_2}:{port_2}/{db_2}")
conn_2=sqlalchemy.create_engine(f"postgresql+psycopg://{user_2}:{password_2}@{hostname_2}:{port_2}/{db_2}")


sys.exit()
'''
Liste des tables a synchroniser
'''
table_list=os.environ["TABLES"].split(',')
print(table_list)
for table in table_list:
    sync_table(table_name=table, interval=interval, connexion_1=conn_1, connexion_2=conn_2,dry_run=True)


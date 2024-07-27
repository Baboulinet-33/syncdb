# SyncDB

Synchronisation de 2 bases de données.

## Configuration

Remplir le fichier .env-exemple
Taper la commande suivante pour charger les variables d'environnement:
```sh
source .env
```

*Note: INTERVAL ne sert plus, a supprimer*



### Variables d'environnement

| Nom | Description |
|-----|-------------|
| HOSTNAME_1 | url vers la bdd source |
| PORT_1 | port de la bdd source |
| USERNAME_1 | login de la bdd source |
| PASSWORD_1 | mot de passe pour la bdd source |
| DB_1 | nom de la base dans la bdd source |
| HOSTNAME_2 | url vers la bdd de destination |
| PORT_2 | port de la bdd de destination |
| USERNAME_2 | login de la bdd de destination |
| PASSWORD_2 | mot de passe de la bdd de destination |
| DB_2 | nom de la base dans la bdd de destination |
| INTERVAL | Combien de temps on remonte en arrière |
| TABLES | Nom des tables par ordre a synchroniser |


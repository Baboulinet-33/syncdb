ARG py_version=3.12.4
ARG wolfi_version=latest

###########################################
# Base image with python

FROM chainguard/wolfi-base:$wolfi_version AS python_base

ARG py_version

RUN apk add --no-cache --no-check-certificate python3~$py_version tzdata


###########################################
# Throwaway image with C compiler installed
FROM python_base AS builder

ARG py_version

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

# install the C compiler
RUN apk add --no-cache --no-check-certificate python3-dev~$py_version gcc glibc-dev postgresql-16-dev uv

# Make sure we use the virtualenv:
ENV VIRTUAL_ENV=/opt/venv PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

# install in venv
RUN uv venv /opt/venv && uv pip install --compile --no-cache -r requirements.txt


###########################################
# Image WITHOUT C compiler
FROM python_base

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

RUN apk add --no-cache --no-check-certificate libpq-16

# Copy from venv
COPY --from=builder  /opt/venv /opt/venv

WORKDIR /app

COPY ./pg_sync_tables.py /app/pg_sync_tables.py
RUN mkdir scripts
COPY ./run.sh /app/scripts

RUN find /app/scripts/ -type f -iname "*.sh" -exec chmod a+x {} +

# change to the nonroot user
USER nonroot

ENV PATH=/opt/venv/bin:$PATH LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/app:/opt/venv TZ=UTC

# Run the API
CMD ["./scripts/run.sh"]

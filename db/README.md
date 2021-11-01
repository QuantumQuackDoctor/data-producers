# How to Start Docker Postgres Container

# This folder is deprecated

## Setup
```
pip install docker
docker pull postgres
```

## dbsetup.py
### set_up_docker_db()
starts a new postgres docker container

### create_schema()
runs dbschema.sql to create all tables

### truncate_db()
runs truncate.sql to remove all contents from tables


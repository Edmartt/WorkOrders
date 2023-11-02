# work orders

## Requirements

- Python 3.11
- PostgreSQL
- Docker
- Redis


Work order REST API


## Running Development Version With Flask

1. Clone the repo:

```
git clone https://github.com/Edmartt/WorkOrders.git
```

2. Browse into the project directory

```
cd WorkOrders/
```

3. Create a virtual environment

```
python -m venv <virtual-environment-name>
```

4. Activate the virtual environment

```
source <virtual-environment-name>/bin/activate
```

5. Set the environment variables following the envrc.example file here ![.envrc.example](https://github.com/Edmartt/WorkOrders/blob/dev/.envrc.example)

```
source .envrc
```

#### Note

Remember to set a .env file for docker-compose ![env.example](https://github.com/Edmartt/WorkOrders/blob/dev/env.example) and run `docker-compose up -d` for creating a postgres instance


6. Migrations

We need migrations for our data models

```
flask db upgrade
```

7. Run with

```
flask run
```

#### Note

For requesting the api docs after running the project just go to `/api/docs`

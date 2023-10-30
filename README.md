# work orders

## Requirements

- Python 3.11
- Flask
- PostgreSQL
- Docker


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

6. Run with

```
flask run
```

#### Note

For requesting the api docs after running the project just go to `/api/docs`

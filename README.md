
![python version](https://img.shields.io/badge/python-v3.x-blue)

# Inventory Management System

This repository provides a simple Inventory Management System implemented in Python using FastAPI, SQL Server, and SQLAlchemy ORM.

## Getting Started

To run this project, follow the steps below after cloning the repository.

### Setting up the Environment

1. **Create a Conda Environment:**

    ```bash
    conda create --name my_new_environment --file requirements.txt
    conda activate my_new_environment
    ```

2. **Setting Up the Database:**

    - Create a database in SQL Server.

3. **Configure Environment Variables:**

    - Create a `.env` file in the `src` directory and define the following variables:

        ```plaintext
        SECRET_KEY='a key'
        ALGORITHM='choose an algorithm'
        CONNECTION_STRING='mssql+pyodbc://{user}:{password}@{database_url}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server'
        ```

### Running the Application

4. **Initialize Alembic:**

    ```bash
    cd src
    alembic init migrations
    ```

5. **Update env.py:**

    Update the `env.py` file in the `migrations` directory:

    ```python
    from dotenv import load_dotenv
    import os

    load_dotenv()
    config.set_main_option('sqlalchemy.url', os.getenv('CONNECTION_STRING'))

    from src.repository.models import BASE
    target_metadata = BASE.metadata
    ```

6. **Run Migrations:**

    ```bash
    cd migrations
    alembic revision --autogenerate -m "write a message"
    ```

7. **Run Tests:**

    ```bash
    pytest
    ```

8. **Run the Application:**

    ```bash
    cd ..
    uvicorn src.main:app
    ```



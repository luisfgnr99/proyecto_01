import os
import json
from google.cloud import secretmanager
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.engine.url import make_url


# credenciales de la base de datos
def custom_json_parser(dct):
    for key, value in dct.items():
        if value.lower() == "true":
            dct[key] = True
        elif value.lower() == "false":
            dct[key] = False
    return dct


def get_database_config():
    db_config_json = os.environ.get('DATASOURCE')
    project_id = os.environ.get('_projectid_')

    if db_config_json is not None and db_config_json != "":
        db_config = json.loads(db_config_json, object_hook=custom_json_parser)
        print("_variable de entorno_")
    else:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/databaseaccess/versions/latest"
        response = client.access_secret_version(name=name)
        db_config = json.loads(response.payload.data.decode("UTF-8"), object_hook=custom_json_parser)
        print("_secret_")
    
    return db_config


def create_engine_and_session():
    db_config = get_database_config()

    # Construir la cadena de conexión manualmente
    connection_string = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

    # Utilizar make_url para convertir la cadena en un objeto URL
    db_url = make_url(connection_string)

    # Configuración del pool de conexiones
    engine = create_engine(db_url, poolclass=QueuePool, pool_size=10, max_overflow=20)
    conexion = engine.connect()


    return engine, conexion
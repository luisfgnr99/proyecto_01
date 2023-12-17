import os
import json
from google.cloud import secretmanager

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

    if db_config_json is not None or db_config_json != "":
        db_config = json.loads(db_config_json, object_hook=custom_json_parser)
        print("_variable de entorno_")
    else:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/databaseaccess/versions/latest"
        response = client.access_secret_version(name=name)
        db_config = json.loads(response.payload.data.decode("UTF-8"))
        print("_secret_")
    
    return db_config
    
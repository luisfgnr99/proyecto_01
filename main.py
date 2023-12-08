# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudrun_helloworld_service]
# [START run_helloworld_service]
import os
import mysql.connector

from flask import Flask, request, jsonify


app = Flask(__name__)

# credenciales de la base de datos
db_config = {
    'user': 'appestudiante',
    'password': '1234abcd',
    'host': '35.239.168.101',
    'database': 'estudiantes',
    'raise_on_warnings': True,
}

# if os.getenv("GAE_INSTANCE"):
#     db.config["unix_socket"] = "cloudsql/tutorial-20231201:us-central1:estudiantesdb"

conexion = mysql.connector.connect(**db_config)
cursor = conexion.cursor()


@app.route("/estudiantes", methods=["POST"])
def agregar_estudiante():
    data = request.get_json()
    nombre = data.get("nombre")
    identificacion = data.get("identificacion")
    edad = data.get("edad")
    direccion = data.get("direccion")

    consulta_insert = "INSERT INTO estudiantes (nombre, identificacion, edad, direccion) VALUES (%s, %s, %s, %s)"
    cursor.execute(consulta_insert, (nombre, identificacion, edad, direccion))
    conexion.commit()
    return jsonify({"Estudiante agregado exitosamente"}), 201


@app.route("/estudiantes", methods=["GET"])
def obtener_estudiantes():
    consulta_select = "SELECT * FROM estudiantes"
    cursor.execute(consulta_select)
    resultados = cursor.fetchall()

    estudiantes = []
    for resultado in resultados:
        estudiante = {
            "nombre" : resultado[1],
            "identificacion" : resultado[2],
            "edad" : resultado[3],
            "direccion" : resultado[4]
        }
        estudiantes.append(estudiante)

    return jsonify(estudiantes)

@app.route("/estudiantes/<string:estudianteid>", methods=["GET"])
def obtener_estudianteid(estudianteid):

    consulta_select = "SELECT * FROM estudiantes WHERE identificacion = %s"
    cursor.execute(consulta_select, (estudianteid,))
    resultado = cursor.fetchone()

    if resultado:
        estudiante = {
            "nombre" : resultado[1],
            "identificacion" : resultado[2],
            "edad" : resultado[3],
            "direccion" : resultado[4]
        }
        return jsonify(estudiante), 200
    else:
        return jsonify({"Estudiante no encontrado"}), 404
    
    
@app.route("/estudiantes/<string:estudianteid>", methods=["PUT"])
def actualizar_estudiante(estudianteid):
        
        data = request.get_json()
        nombre = data.get("nombre")
        edad = data.get("edad")
        direccion = data.get("direccion")

        consulta_update = ("UPDATE estudiantes SET nombre = %s, edad = %s, direccion = %s WHERE identificacion = %s")
        cursor.execute(consulta_update, (nombre, edad, direccion, estudianteid))
        conexion.commit()

        return jsonify({"Estudiante actualizado exitosamente"}), 200


@app.route("/estudiantes/<string:estudianteid>", methods=["DELETE"])
def eliminar_estudiante(estudianteid):

    consulta_delete = "DELETE FROM estudiantes WHERE identificacion = %s"
    cursor.execute(consulta_delete, (estudianteid,))
    conexion.commit()

    return jsonify({"Estudiante eliminado exitosamente"}), 204


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END run_helloworld_service]
# [END cloudrun_helloworld_service]

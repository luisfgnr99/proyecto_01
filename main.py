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
from flask import Flask, request, jsonify
from estudianteDAO import EstudianteDAO, EstudianteDTO
from database_config import create_engine_and_session
import os


app = Flask(__name__)

engine, db_session = create_engine_and_session()

# instancia estudianteDAO
estudiante_dao = EstudianteDAO(db_session)


@app.route("/estudiantes", methods=["POST"])
def agregar_estudiante():
    try:
        data = request.get_json()

        for est in data:
            estudiante = EstudianteDTO(**est)
            estudiante_dao.create(estudiante)
        return jsonify({"Mensaje" : "Estudiante agregado exitosamente"}), 201
    except Exception as error:
        return jsonify({"Error": f"Error en la base de datos: {str(error)}"}), 400


@app.route("/estudiantes", methods=["GET"])
def obtener_estudiantes():
    try:
        estudiantes = estudiante_dao.read_all()
        if estudiantes:
            estudiantes_json = []
            for estudiante in estudiantes:
                estudiantes_json.append(estudiante.__dict__)

            return jsonify(estudiantes_json)
        else:
            return jsonify({"Mensaje" : "No hay datos en la tabla"}), 404
    except Exception as e:
        return jsonify({"Mensaje" : f"Error en la base de datos: {str(e)}"}), 400


@app.route("/estudiantes/<string:estudianteid>", methods=["GET"])
def obtener_estudianteid(estudianteid):
    try:
        estudiante = estudiante_dao.read_by_id(estudianteid)

        if estudiante:
            return jsonify(estudiante.__dict__), 200
        else:
            return jsonify({"Mensaje" : "Estudiante no encontrado"}), 404
    except Exception as e:
        return jsonify({"Mensaje" : f"Error en la base de datos: {str(e)}"}), 400
    
    
@app.route("/estudiantes/<string:estudianteid>", methods=["PUT"])
def actualizar_estudiante(estudianteid):
        try:
            data = request.get_json()
            new_estudiante = EstudianteDTO(**data)
            
            if new_estudiante.identificacion == estudianteid:
                update_status = estudiante_dao.update(estudianteid, new_estudiante)
                if update_status:
                    return jsonify({"Mensaje" : f"Estudiante actualizado exitosamente"}), 200
                else:
                    return jsonify({"Mensaje" : f"Estudiante no existe"}), 404
            else:
                return jsonify({"Mensaje" : f"No coinciden los datos del estudiante con el id enviado"}), 404
        except Exception as e:
            return jsonify({"Mensaje" : f"Error en la base de datos: {str(e)}"}), 400


@app.route("/estudiantes/<string:estudianteid>", methods=["DELETE"])
def eliminar_estudiante(estudianteid):
    try:
        deletion_status = estudiante_dao.delete(estudianteid)

        if deletion_status:
            return jsonify({"Mensaje" : "Estudiante eliminado exitosamente"}), 204
        else:
            return jsonify({"Mensaje" : "Error al eliminar estudiante. No existe"}), 500
    except Exception as e:
            return jsonify({"Mensaje" : f"Error en la base de datos: {str(e)}"}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END run_helloworld_service]
# [END cloudrun_helloworld_service]

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

from flask import Flask, request


app = Flask(__name__)


@app.route("/estudiantes", methods=["POST"])
def login():
    data = request.get_json()
    nombre = data.get("nombre")
    identificacion = data.get("identificacion")
    edad = data.get("edad")
    direccion = data.get("direccion")
    print("objeto: {0}, {1}, {2}, {3}".format(nombre, identificacion, edad, direccion))
    return ("succesfull", 201)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END run_helloworld_service]
# [END cloudrun_helloworld_service]

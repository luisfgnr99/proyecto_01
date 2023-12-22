import sqlalchemy
import traceback
from estudianteDTO import EstudianteDTO


class EstudianteDAO:
    def __init__(self, db_config):
        self.db_config = db_config


    def create(self, estudiante):
        try:
            consulta_insert = sqlalchemy.text("""INSERT INTO estudiantes (nombre, identificacion, edad, direccion) 
                                              VALUES (:nombre, :identificacion, :edad, :direccion)""")
            # with mysql.connector.connect(**self.db_config) as conexion:
            #     with conexion.cursor() as cursor:
            #         cursor.execute(consulta_insert, (estudiante.nombre, estudiante.identificacion, estudiante.edad, estudiante.direccion))
            #     conexion.commit()
            self.db_config.execute(
                consulta_insert, 
                parameters={
                    "nombre": estudiante.nombre, 
                    "identificacion": estudiante.identificacion,
                    "edad": estudiante.edad, 
                    "direccion": estudiante.direccion})
            self.db_config.commit()
        except Exception as e:
            traceback.print_exc()
            raise Exception("Error ejecutando el query")
    

    def read_all(self):
        try:
            consulta_select = sqlalchemy.text("SELECT nombre, identificacion, edad, direccion FROM estudiantes")
            # '''with mysql.connector.connect(**self.db_config) as conexion:
            #     with conexion.cursor() as cursor:
            #         cursor.execute(consulta_select)
            #         resultados = cursor.fetchall()'''
            resultados = self.db_config.execute(consulta_select, parameters={}).fetchall()
            
            if resultados:
                estudiantes = []
                for resultado in resultados:
                    estudiante = EstudianteDTO(
                        nombre = resultado[0],
                        identificacion = resultado[1],
                        edad = resultado[2],
                        direccion = resultado[3]
                    )
                    estudiantes.append(estudiante)
                return(estudiantes)
            else:
                return None
        except Exception as e:
            traceback.print_exc()
            raise Exception("Error ejecutando el query")
    

    def read_by_id(self, estudiante_id):
        try:
            consulta_select = sqlalchemy.text("""SELECT nombre, identificacion, edad, direccion 
                                              FROM estudiantes WHERE identificacion = :identificacion""")
            # with mysql.connector.connect(**self.db_config) as conexion:
            #     with conexion.cursor() as cursor:
            #         cursor.execute(consulta_select, (estudiante_id,))
            #         resultado = cursor.fetchone()
            resultado = self.db_config.execute(consulta_select, parameters={"identificacion": estudiante_id}).fetchone()

            if resultado:
                estudiante = EstudianteDTO(
                        nombre = resultado[0],
                        identificacion = resultado[1],
                        edad = resultado[2],
                        direccion = resultado[3]
                    )
                return estudiante
            else:
                return None
        except Exception as e:
            traceback.print_exc()
            raise Exception("Error ejecutando el query")
        
    
    def update(self, estudiante_id, new_estudiante):
        try:
            consulta_update = sqlalchemy.text("""UPDATE estudiantes 
                                              SET nombre = :nombre, edad = :edad, direccion = :direccion 
                                              WHERE identificacion = :identificacion""")
            resultado = self.db_config.execute(
                consulta_update, 
                parameters={
                    "nombre": new_estudiante.nombre,
                    "edad":   new_estudiante.edad,
                    "direccion": new_estudiante.direccion,
                    "identificacion": new_estudiante.identificacion
                })
            num_rows_affected = resultado.rowcount
            self.db_config.commit()
            
            if num_rows_affected:
                return True
            else:
                return False
        except Exception as e:
            traceback.print_exc()
            raise Exception("Error ejecutando el query")


    def delete(self, estudiante_id):
        try:
            consulta_delete = sqlalchemy.text("""DELETE FROM estudiantes WHERE identificacion = :identificacion""")
            resultado = self.db_config.execute(consulta_delete, parameters={"identificacion": estudiante_id})
            num_rows_affected = resultado.rowcount
            self.db_config.commit()

            if num_rows_affected:
                return True
            else:
                return False
        except Exception as e:
            traceback.print_exc()
            raise Exception("Error ejecutando el query")
import mysql.connector
from estudianteDTO import EstudianteDTO


class EstudianteDAO:
    def __init__(self, db_config):
        self.db_config = db_config


    def create(self, estudiante):
        consulta_insert = "INSERT INTO estudiantes (nombre, identificacion, edad, direccion) VALUES (%s, %s, %s, %s)"
        with mysql.connector.connect(**self.db_config) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(consulta_insert, (estudiante.nombre, estudiante.identificacion, estudiante.edad, estudiante.direccion))
            conexion.commit()
    

    def read_all(self):
        consulta_select = "SELECT nombre, identificacion, edad, direccion FROM estudiantes"
        with mysql.connector.connect(**self.db_config) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(consulta_select)
                resultados = cursor.fetchall()
        
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
    

    def read_by_id(self, estudiante_id):
        consulta_select = "SELECT nombre, identificacion, edad, direccion FROM estudiantes WHERE identificacion = %s"
        with mysql.connector.connect(**self.db_config) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(consulta_select, (estudiante_id,))
                resultado = cursor.fetchone()
        
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
        
    
    def update(self, estudiante_id, new_estudiante):
        try:
            consulta_select = "SELECT 1 FROM estudiantes WHERE identificacion = %s"
            consulta_update = "UPDATE estudiantes SET nombre = %s, edad = %s, direccion = %s WHERE identificacion = %s"
            with mysql.connector.connect(**self.db_config) as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(consulta_select, (estudiante_id,))
                    resultado = cursor.fetchone()
                    if resultado:
                        cursor.execute(consulta_update, (new_estudiante.nombre, new_estudiante.edad, new_estudiante.direccion, estudiante_id))
                        conexion.commit()
                        return True
                    else:
                        return False
        except Exception as e:
            print(f"Error borrando el registro: {str(e)}")
            return False


    def delete(self, estudiante_id):
        try:
            consulta_select = "SELECT 1 FROM estudiantes WHERE identificacion = %s"
            consulta_delete = "DELETE FROM estudiantes WHERE identificacion = %s"
            with mysql.connector.connect(**self.db_config) as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(consulta_select, (estudiante_id,))
                    resultado = cursor.fetchone()
                    if resultado:
                        cursor.execute(consulta_delete, (estudiante_id,))
                        conexion.commit()
                        return True
                    else:
                        return False
        except Exception as e:
            print(f"Error borrando el registro: {str(e)}")
            return False
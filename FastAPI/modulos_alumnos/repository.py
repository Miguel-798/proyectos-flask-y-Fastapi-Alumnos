from modulos_alumnos.database import get_db
from modulos_alumnos.schemas import schema
import pymysql.cursors
from modulos_alumnos.models import Alumno

class AlumnoRepository:

    def __init__(self):
        self.db = get_db()

    def get_all(self):
        with self.db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM alumnos")
            results = cursor.fetchall()
            return [schema(alumno) for alumno in results]

    def get_by_id(self, id: int):
        with self.db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM alumnos WHERE alumnoid = %s", (id,))
            result = cursor.fetchone()
            if result:
                return schema(result)
            return None

    def add_alumno(self, alumno: Alumno):
        with self.db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO alumnos (alumnodni, nombre, apellido, fechanacimiento, email, telefono) VALUES (%s, %s, %s, %s, %s, %s)",
                (alumno.AlumnoDNI, alumno.Nombre, alumno.Apellido, alumno.FechaNacimiento, alumno.Email, alumno.Telefono)
            )
            self.db.commit()
            return alumno

    def update_alumno(self, alumno: Alumno):
        with self.db.cursor() as cursor:
            cursor.execute(
                "UPDATE alumnos SET alumnodni = %s, nombre = %s, apellido = %s, fechanacimiento = %s, email = %s, telefono = %s WHERE AlumnoID = %s",
                (alumno.AlumnoDNI, alumno.Nombre, alumno.Apellido, alumno.FechaNacimiento, alumno.Email, alumno.Telefono, alumno.AlumnoID)
            )
            self.db.commit()
            return alumno

    def delete_alumno(self, id: int):
        with self.db.cursor() as cursor:
            cursor.execute("DELETE FROM alumnos WHERE alumnoid = %s", (id,))
            self.db.commit()
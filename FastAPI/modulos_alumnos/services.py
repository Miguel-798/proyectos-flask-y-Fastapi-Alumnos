from modulos_alumnos.repository import AlumnoRepository
from modulos_alumnos.models import Alumno

class AlumnoService:

    def __init__(self):
        self.repositorio = AlumnoRepository()

    def listar_alumnos(self):
        return self.repositorio.get_all()

    def obtener_por_id(self, id: int):
        return self.repositorio.get_by_id(id)

    def registrar_alumno(self, alumno: Alumno):
        return self.repositorio.add_alumno(alumno)

    def actualizar_alumno(self, alumno: Alumno):
        return self.repositorio.update_alumno(alumno)

    def borrar_alumno(self, id: int):
        return self.repositorio.delete_alumno(id)
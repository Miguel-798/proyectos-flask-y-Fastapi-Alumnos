from modulos_alumnos.models import Alumno

# Función auxiliar para mapear resultados de la base de datos a un objeto Alumno
def schema(user):
    user['FechaNacimiento'] = str(user['FechaNacimiento'])
    return Alumno(**user)
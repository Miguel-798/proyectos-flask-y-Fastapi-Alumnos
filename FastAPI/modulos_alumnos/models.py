from pydantic import BaseModel

# Modelo de Alumno
class Alumno(BaseModel):
    AlumnoID: int | None = None
    AlumnoDNI: str
    Nombre: str
    Apellido: str
    FechaNacimiento: str
    Email: str
    Telefono: str
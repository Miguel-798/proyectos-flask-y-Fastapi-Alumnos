from fastapi import APIRouter, HTTPException


from modulos_alumnos.services import AlumnoService
from modulos_alumnos.models import Alumno
router = APIRouter( prefix="/alumno",
                    tags= ["users"],
                    responses={404: {"message": "No encontrado"}})

# Rutas
@router.get("/users")
def get_users():
    service = AlumnoService()
    return service.listar_alumnos()


@router.get("/user/{id}")
async def get_user_by_id(id: int):
    service = AlumnoService()
    alumno = service.obtener_por_id(id)
    if alumno:
        return alumno
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.post("/user/", response_model=Alumno, status_code=201)
async def create_user(user: Alumno):
    service = AlumnoService()
    alumno_existente = service.obtener_por_id(user.AlumnoID)
    if alumno_existente:
        raise HTTPException(status_code=400, detail="El usuario ya está inscrito")
    return service.registrar_alumno(user)


@router.put("/user/")
async def update_user(user: Alumno):
    service = AlumnoService()
    alumno_existente = service.obtener_por_id(user.AlumnoID)
    if alumno_existente:
        return service.actualizar_alumno(user)
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.delete("/user/{id}")
async def delete_user(id: int):
    service = AlumnoService()
    alumno_existente = service.obtener_por_id(id)
    if alumno_existente:
        service.borrar_alumno(id)
        return {"message": "Alumno eliminado correctamente"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

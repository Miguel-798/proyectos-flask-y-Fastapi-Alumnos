from flask import Blueprint, render_template, flash, redirect, url_for, request
from config import Config
import pymysql
from models.alumno_models import get_all_alumnos, get_alumno_by_dni, get_alumno_by_id, add_alumno, delete_alumno, update_alumno


# Definición del blueprint

alumnos_bp = Blueprint('alumnos', __name__)


@alumnos_bp.route("/registrar", methods = ["GET", "POST"])
def registra():
    if request.method == "POST":
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha']
        email = request.form['email']
        telefono = request.form['telefono']
        

        try:
            add_alumno(dni, nombre, apellido, fecha_nacimiento, email, telefono)
            flash("El alumno se ha agregado correctamente", "success")
        except pymysql.MySQLError:
            flash("No se pudo registrar el alumno", "danger")
    return render_template("registrar_alumno.html")



@alumnos_bp.route("/consultar", methods = ["GET", "POST"])
def consulta():
    if request.method == "POST":
        dni = request.form['dni']
        alumno_buscado = get_alumno_by_dni(dni)

        if alumno_buscado:
            return render_template("consultar_alumno.html", alumno = alumno_buscado)
        
        else:
            flash("No se pudo encontrar ningun alumno con el DNI proporcionado", "danger")
            return redirect(url_for('consulta'))
    return render_template("consultar_alumno.html")



@alumnos_bp.route("/eliminar/<int:id>")
def eliminarAlumnos(id):
    
    try:
        delete_alumno(id)
        flash("alumno eliminado", "success")
    except pymysql.MySQLError:
        flash("No se pudo eliminar el alumno, tiene cursos registrados", "danger")
    return redirect(url_for('lista'))


# return render_template("eliminar_alumno.html")

@alumnos_bp.route("/listar")
def lista():
    listAlumnos = get_all_alumnos()
    return render_template("listar_alumno.html", total_alumnos = listAlumnos)



@alumnos_bp.route("/modificar", methods = ["GET", "POST"])
@alumnos_bp.route("/modificar/<int:alumnoid>", methods = ["GET", "POST"])
def modifica(alumnoid=None):
    if request.method == "POST":
        if "buscar" in request.form:
            dni = request.form['dni']
            alumno_buscado = get_alumno_by_dni(dni)

            if alumno_buscado:
                return render_template("modificar_alumno.html", alumno = alumno_buscado)
            
            else:
                flash("No se pudo encontrar ningun alumno con el DNI proporcionado", "danger")
                return redirect(url_for('modifica'))
            
        elif "modificar" in request.form:
            alumnoid = request.form['alumnoid']
            dni = request.form['dni']
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            fecha_nacimiento = request.form['fecha']
            email = request.form['email']
            telefono = request.form['telefono']

            try:
                update_alumno(alumnoid, dni, nombre, apellido, fecha_nacimiento, email, telefono)
                flash("Los datos del alumno han sido actualizados", "success")
            except pymysql.MySQLError:
                flash("No se pudieron actualizar los datos del alumno", "danger")
            return render_template("modificar_alumno.html")   
         
        elif "eliminar" in request.form:
            alumnoid = request.form['alumnoid']
            return redirect(url_for("eliminarAlumnos", alumno_id = alumnoid))
        
    if request.method == "GET":
        if alumnoid:
            alumno_buscado = get_alumno_by_id(alumnoid)
            if alumno_buscado:
                return render_template("modificar_alumno.html", alumno = alumno_buscado)
            else:
                flash("DNI no registrado!!!", "danger")

    return render_template("modificar_alumno.html")
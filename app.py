from flask import Flask, render_template, flash, redirect, url_for, request
from config import Config
from models.alumno_models import get_all_alumnos, delete_alumno, add_alumno, get_alumno_by_dni, update_alumno, get_alumno_by_id
import os, pymysql

app = Flask("__main__")

# Cargar la configuracion
app.config.from_object(Config)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/registrar", methods = ["GET", "POST"])
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



@app.route("/consultar", methods = ["GET", "POST"])
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



@app.route("/eliminar/<int:id>")
def eliminarAlumnos(id):
    
    try:
        delete_alumno(id)
        flash("alumno eliminado", "success")
    except pymysql.MySQLError:
        flash("No se pudo eliminar el alumno, tiene cursos registrados", "danger")
    return redirect(url_for('lista'))


# return render_template("eliminar_alumno.html")

@app.route("/listar")
def lista():
    listAlumnos = get_all_alumnos()
    return render_template("listar_alumno.html", total_alumnos = listAlumnos)



@app.route("/modificar", methods = ["GET", "POST"])
@app.route("/modificar/<int:alumnoid>", methods = ["GET", "POST"])
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
   



if __name__ == "__main__":
    app.run(debug=True)
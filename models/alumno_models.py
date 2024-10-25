import pymysql
from flask import current_app, g

import click
import pymysql.cursors

def get_db():
    
    if "db" not in g:
        g.db = pymysql.connect(
            host=current_app.config['MYSQL_HOST'], # conecta con el archivo config.py
            port=current_app.config['MYSQL_PORT'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB'],
        )
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()



def get_all_alumnos():
    db = get_db()
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM alumnos")
        return cursor.fetchall()
    
def get_alumno_by_dni(dni):
    db = get_db()
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM alumnos WHERE alumnodni = %s", (dni,))
        return cursor.fetchone()
    

def get_alumno_by_id(alumno_id):
    db = get_db()
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM alumnos WHERE alumnoid = %s", (alumno_id,))
        return cursor.fetchone()
    
def add_alumno(dni, nombre, apellido, fecha_nacimiento, email, telefono):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO alumnos (alumnodni, nombre, apellido, fechanacimiento, email, telefono) VALUES (%s, %s, %s, %s, %s, %s)",
            (dni, nombre, apellido, fecha_nacimiento, email, telefono)
        )
        db.commit()
    
def update_alumno(alumnoid, dni, nombre, apellido, fecha_nacimiento, email, telefono):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            "UPDATE alumnos SET alumnodni = %s, nombre =%s, apellido = %s, fechanacimiento = %s, email = %s, telefono = %s WHERE AlumnoID = %s",
            (dni, nombre, apellido, fecha_nacimiento, email, telefono, alumnoid)
        )
        db.commit()

def delete_alumno(alumno_id):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            "DELETE FROM alumnos WHERE alumnoid = %s", (alumno_id,)
        )
        db.commit()
from flask import Flask, render_template
from config import Config

from blueprints.alumnos_blueprint import alumnos_bp

# Ejemplos de otras importaciones
# from blueprints.cursos_blueprint import cursos_bp
# from blueprints.cursos_alumno_blueprint import cursos_alumno_bp

app = Flask("__main__")

# Cargar la configuracion
app.config.from_object(Config)


# Registrar Blueprints
app.register_blueprint(alumnos_bp, url_prefix='/alumnos')

# Ejemplos de otros registros:
# app.register_blueprint(cursos_bp, url_prefix='/cursos')
# app.register_blueprint(cursos_alumno_bp, url_prefix='/cursos-alumno')

@app.route("/")
def index():
    return render_template("index.html")


#---------------INICIO----------------
if __name__ == "__main__":
    app.run(debug=True)
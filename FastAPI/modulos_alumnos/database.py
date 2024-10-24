import pymysql
from decouple  import config



# Configuración de la base de datos
config = pymysql.connect(
    host = config('MYSQL_HOST'),
    port = int(config('MYSQL_PORT')),
    database = config('MYSQL_DB'),
    user = config('MYSQL_USER'),
    password = config('MYSQL_PASSWORD'),
)

# Función para obtener la conexión a la base de datos
def get_db():
    connection = config
    return connection
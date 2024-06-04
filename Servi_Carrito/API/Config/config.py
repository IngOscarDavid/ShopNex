import MySQLdb
import os

# Configuracion
db_config = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'servicios_catalogo')
}

# Conectamos
conn = MySQLdb.connect(**db_config)

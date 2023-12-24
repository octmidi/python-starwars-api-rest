import json
import psycopg2

# Configuración de la conexión a PostgreSQL
conn_params = {
    'host': 'localhost',
    'database': 'starwars2',
    'user': 'postgres',
    'password': '10644',
    'port': '5432'
}

# Ruta al archivo JSON
json_file_path = './data/planet.json'

# Función para cargar datos en PostgreSQL desde el archivo JSON


def cargar_datos_postgres(conn_params, json_file_path):
    # Conexión a PostgreSQL
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()

    try:
        # Leer el archivo JSON
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Iterar sobre los datos y ejecutar consultas de inserción
        # '%s' es un marcador de posición para los valores que se proporcionan en la tupla, evita inyeccion de sql
        for item in data:
            cursor.execute(
                "INSERT INTO planets (id, name, url) VALUES (%s, %s, %s)",
                (item.get('uid'), item.get('name'), item.get('url'))
            )

        # Confirmar las transacciones
        conn.commit()
        print("Datos insertados correctamente en PostgreSQL.")

    except Exception as error_code:
        print(f"Error: {error_code}")

    finally:
        # Cerrar la conexión
        cursor.close()
        conn.close()


# Llamar a la función para cargar datos en PostgreSQL
cargar_datos_postgres(conn_params, json_file_path)

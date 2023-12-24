import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import Favorite_Planets, People, Planets, User, Favorite_Planets, db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:10644@localhost:5432/starwars2'
db.init_app(app)
migrate = Migrate(app, db)
print('hola')

# Handle/serialize errors like a JSON object
# generate sitemap with all your endpoints


@app.route('/', methods=['GET'])
def get_admin():
    return ('<h1>Hola</h1>')


@app.route('/people', methods=['GET'])
def get_people():
    people_list = People.query.all()
    if people_list:
        # Crear una lista de diccionarios con los datos de todas las personas
        people_data = []
        for people in people_list:
            people_data = {
                'id': person.id,
                'name': person.name,
                'url': person.url
                # Agregar otros campos según la estructura de tu modelo de datos
            }
            people_data.append(people_data)

        # Devolver la lista de datos de todas las personas en formato JSON
        return jsonify(people=people_data)
    else:
        return 'No se encontraron usuarios', 404


@app.route('/people/<int:id>', methods=['GET'])
def get_people_id(id):
    people = People.query.get(id)
    if people:
        # Aquí puedes devolver los datos del usuario en el formato que desees, por ejemplo, como JSON
        return {
            'id': people.id,
            'name': people.name,
            'url': people.url
        }
    else:
        return 'Planeta no encontrado', 404


@app.route('/planets', methods=['GET'])
def get_planet():
    planet_list = Planets.query.all()
    if planet_list:
        # Crear una lista de diccionarios con los datos de todas las personas
        planet_data = []
        for planet in planet_list:
            planet_info = {
                'id': planet.id,
                'name': planet.name,
                'url': planet.url
                # Agregar otros campos según la estructura de tu modelo de datos
            }
            planet_data.append(planet_info)

        # Devolver la lista de datos de todas las personas en formato JSON
        return jsonify(people=planet_data)
    else:
        return 'No se encontraron planetas', 404


@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_id(id):
    planet = Planets.query.get(id)
    if planet:
        # Aquí puedes devolver los datos del usuario en el formato que desees, por ejemplo, como JSON
        return {
            'id': planet.id,
            'name': planet.name,
            'url': planet.url
        }
    else:
        return 'Usuario no encontrado', 404


@app.route('/user', methods=['GET'])
def get_db():
    try:
        # Ejemplo de consulta a la tabla User
        user = User.query.all()

        # Transformar los resultados a un formato deseado
        user_list = [{"id": user.id, "email": user.email} for user in user]

        response_body = {
            "msg": "Hello, this is your GET /user response",
            "user": user_list
        }

        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/favorite_planets', methods=['GET'])
def get_favorite_planets():
    try:
        # Recupera todos los registros de la tabla Favorite_Planets
        favorite_planets = Favorite_Planets.query.all()

        # Serializa los registros en un formato JSON
        serialized_favorite_planets = []
        for favorite_planet in favorite_planets:
            serialized_favorite_planet = {
                "id_user": favorite_planet.id_user,
                "id_planet": favorite_planet.id_planet,
                "created": favorite_planet.created.strftime('%Y-%m-%d %H:%M:%S')
            }
            serialized_favorite_planets.append(serialized_favorite_planet)

        return jsonify(serialized_favorite_planets), 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_favorit_planet_id(planet_id):
    try:
        data = request.json
        # Obtener el ID del usuario de los datos de la solicitud
        id_user = data.get('id_user')
        # Obtener la fecha de creación de los datos de la solicitud
        created = data.get('created')

        # Crea un nuevo registro en la tabla Favorite_Planets
        new_favorite = Favorite_Planets(
            id_user=id_user,
            id_planet=planet_id,  # Utiliza el ID del planeta de la URL
            created=created
        )
        db.session.add(new_favorite)
        db.session.commit()

        response_body = {
            "msg": "Data added successfully",
            "id_user": id_user,
            "id_planet": planet_id,
            "created": created
        }

        return response_body, 200
    except Exception as e:
        db.session.rollback()  # Rollback en caso de error
        return {"error": str(e)}, 500
    finally:
        db.session.close()

 # [POST] /favorite/people/<int:people_id>


@app.route('/consulta/<int:id>', methods=['GET'])
def consulta(id):
    user = User.query.get(id)
    if user:
        # Aquí puedes devolver los datos del usuario en el formato que desees, por ejemplo, como JSON
        return {
            'id': user.id,
            'email': user.email,
            'is_active': user.is_active
        }
    else:
        return 'Usuario no encontrado', 404


if __name__ == '__main__':
    app.run(debug=True)

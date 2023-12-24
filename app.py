import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import Favorite_Planets, Planets, User, db


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


@app.route('/favorit_planet', methods=['POST'])
def post_favorit_planet():
    try:
        data = request.json
        id_user = data.get('id_user')
        id_planet = data.get('id_planet')

        # Verifica si el usuario y el planeta existen
        user = User.query.get(id_user)
        planet = Planets.query.get(id_planet)

        if user is None or planet is None:
            return {"error": "User or planet not found"}, 404

        new_favorite = Favorite_Planets(id_user=id_user, id_planet=id_planet)
        db.session.add(new_favorite)
        db.session.commit()

        response_body = {
            "msg": "Data added successfully",
            "id_user": id_user,
            "id_planet": id_planet
        }

        return response_body, 200

    except Exception as e:
        db.session.rollback()  # Rollback en caso de error
        return {"error": str(e)}, 500

    finally:
        db.session.close()


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

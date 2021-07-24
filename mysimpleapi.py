from os import name
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, DEFAULT_REPRESENTATIONS, Resource
from werkzeug.wrappers import Request

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, unique=True, nullable=False)
    lastname = db.Column(db.String)
    emailaddress = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.firstname} - {self.lastname} - {self.emailaddress} - {self.age} "


@ app.route('/')
def index():

    # api = Api(app)
    return 'Hello user, Welcome here!'


@ app.route('/user')
def get_users():
    users = User.query.all()

    output = []
    for user in users:
        user_data = {'first name': user.firstname, 'last name': user.lastname, 'email address': user.emailaddress,
                     'age': user.age, }

    output.append(user_data)
    return{"users": "output"}


@app.route('/users/<id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return ({"first name": user.firstname, "last name": user.lastname, "email address": user.emailaddress,
             "age": user.age, })


@app.route('/users/', methods=['POST'])
def add_user():
    user = User(firstname=request.json['firstname'], lastname=request.json['lastname'], emailaddress=request.json['emailaddress '],
                age=request.json['age'],)
    db.session.add(user)
    db.session.commit()
    return{'id': user.id}


@app.route('/users/<id>', method=['DELETE'])
def add_user(id):
    user = User.query.get(id)
    if user is None:
        return{"error": "user not found"}
    db.session.delete(user)
    db.session.commit()
    return {"Message": "{Deleted successfully!"}


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, DEFAULT_REPRESENTATIONS, Resource
from werkzeug.wrappers import Request

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///destination.db'


db = SQLAlchemy(app)


class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serviceprovider = db.Column(db.String, unique=True, nullable=False)
    residentrates = db.Column(db.Integer)
    nonresidentrates = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    peakseasons = db.Column(db.String, nullable=False)
    codetogetdiscount = db.Column(
        db.String, unique=True, nullable=False)
    agentcontact = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"{self.serviceprovider} - {self.location} - {self.residentrates} - {self.nonresidentrates} - {self.agentcontact} - {self.peakseasons} - {self.codetogetdiscount}"


@ app.route('/')
def index():

    # api = Api(app)
    return 'Hello user, Traverza here!'


@ app.route('/destination')
def get_destinations():
    destinations = Destination.query.all()

    output = []
    for destination in destinations:
        destination_data = {'service provider': destination.serviceprovider, 'resident rates': destination.residentrates, 'non resident rates': destination.nonresidentrates,
                            'location': destination.location, 'peak seasons': destination.peakseasons, 'code to get discount': destination.codetogetdiscount, 'agent contact': destination.agentcontact}

    output.append(destination_data)
    return{"destinations": "output"}


@app.route('/destinations/<id>')
def get_destination(id):
    destination = Destination.query.get_or_404(id)
    return ({{"service provider": destination.serviceprovider, "resident rates": destination.residentrates, "non resident rates": destination.nonresidentrates,
              "location": destination.location, "peak seasons": destination.peakseasons, "code to get discount": destination.codetogetdiscount, "agent contact": destination.agentcontact}})


@app.route('/destinations/', methods=['POST'])
def add_destination():
    destination = Destination(serviceprovider=request.json['service provider'], residentrates=request.json['resident rates'], nonresidentrates=request.json['non resident rates'],
                              location=request.json['location'], codetogetdiscount=request.json['code to get discount'], agentcontact=request.json['agent contact'], peakseasons=request.json['peak seasons'],)

    db.session.add(destination)
    db.session.commit()
    return{'id': destination.id}


@app.route('/destinations/<id>', method=['DELETE'])
def delete_destination(id):
    destination = Destination.query.get(id)
    if destination is None:
        return{"error": "destination not found"}
    db.session.delete(destination)
    db.session.commit()
    return {"Message": "{Deleted successfully!"}

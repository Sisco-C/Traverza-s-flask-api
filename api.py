from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.wrappers import Request
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///destinations.db'

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
    return 'Hello!'


@ app.route('/travelDestination')
def get_destinations():

    return{"destinations": "destination data"}


@ app.route('/destination')
def get_destinations():
    destinations = Destination.query.all()

    output = []
    for destination in destinations:
        destination_data = {'service provider': destination.serviceprovider, 'resident rates': destination.residentrates, 'non resident rates': destination.nonresidentrates,
                            'location': destination.location, 'peak seasons': destination.peakseasons, 'code to get discount': destination.codetogetdiscount, 'agent contact': destination.agentcontact}

    output.append(destination_data)
    return{"destinations": "output"}

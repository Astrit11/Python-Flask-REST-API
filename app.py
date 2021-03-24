from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# Init app
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)
# User Class/Model
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  surname = db.Column(db.String(200))
  telNo = db.Column(db.String(100))
  address = db.Column(db.String(100))

  def __init__(self, name, surname, telNo, address):
    self.name = name
    self.surname = surname
    self.telNo = telNo
    self.address = address

class Administrator(db.Model):
  aid = db.Column(db.Integer, primary_key=True)
  aname = db.Column(db.String(100))
  asurname = db.Column(db.String(100))

  def __init__(self, aname, asurname, ):
    self.aname = aname
    self.asurname = asurname

# User Schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'surname', 'telNo', 'address')
# Admin schema
class AdministratorSchema(ma.Schema):
  class Meta:
    fields = ('aid', 'aname', 'asurname')

# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

administrator_schema = AdministratorSchema()
administrators_schema = AdministratorSchema(many=True)


# Create a User
@app.route('/user', methods=['POST'])
@cross_origin()
def add_User():
  name = request.json['name']
  surname = request.json['surname']
  telNo = request.json['telNo']
  address = request.json['address']

  new_User = User(name, surname, telNo, address)

  db.session.add(new_User)
  db.session.commit()

  return user_schema.jsonify(new_User)

# Create administrator
@app.route('/Administrator', methods=['POST'])
def add_Administrator():
  aname = request.json['aname']
  asurname = request.json['asurname']

  new_Administrator = Administrator(aname, asurname)

  db.session.add(new_Administrator)
  db.session.commit()

  return administrator_schema.jsonify(new_Administrator)

# Get All Users
@app.route('/users', methods=['GET'])
def get_Users():
  all_Users = User.query.all()
  result = users_schema.dump(all_Users)
  return jsonify(result)

# Get All Administrators
@app.route('/Administrator', methods=['GET'])
def get_Adminsitrators():
  all_Administrators = Administrator.query.all()
  result = administrators_schema.dump(all_Administrators)
  if not all_Administrators:
    return jsonify({'msg':'No administrators found'}),400

  if all_Administrators is not None:
    return jsonify(result),200


# Get Single Users
@app.route('/user/<id>', methods=['GET'])
def get_User(id):
  user = User.query.get(id)
  return user_schema.jsonify(user)

# Get Single Administrators
@app.route('/Administrator/<aid>', methods=['GET'])
def get_Administrator(aid):
  administrator = Administrator.query.get(aid)
  return administrator_schema.jsonify(administrator)

# Update a User
@app.route('/update/<id>', methods=['PUT'])
def update_User(id):
  user = User.query.get(id)

  name = request.json['name']
  surname = request.json['surname']
  telNo = request.json['telNo']
  address = request.json['address']

  user.name = name
  user.surname = surname
  user.telNo = telNo
  user.address = address

  db.session.commit()

  return user_schema.jsonify(user)

# Update Administrator
@app.route('/Administrator/<aid>', methods=['PUT'])
def update_Administrator(aid):
  administrator = Administrator.query.get(aid)

  aname = request.json['aname']
  asurname = request.json['asurname']


  administrator.aname = aname
  administrator.asurname = asurname

  db.session.commit()

  return administrator_schema.jsonify(administrator)

# Delete User
@app.route('/delete/<id>', methods=['DELETE'])
def delete_User(id):
  user = User.query.get(id)
  db.session.delete(user)
  db.session.commit()

  return user_schema.jsonify(user)
# Delete Administrator
@app.route('/Administrator/<aid>', methods=['DELETE'])
def delete_Administrator(aid):
  administrator = Administrator.query.get(aid)
  db.session.delete(administrator)
  db.session.commit()

  return administrator_schema.jsonify(administrator)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)
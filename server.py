from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Adv, Session, User
from sqlalchemy.exc import IntegrityError
from schema import CreateAdv, CreateUser
import pydantic

app = Flask('app')

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response):
    request.session.close()
    return response

def get_adv_by_id(adv_id: int):
    adv = request.session.get(Adv, adv_id)
    if adv is None:
        raise HttpError(404, "advertisement not found")
    return adv

class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description

def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(409, "user already exists")
    return user

def add_adv(adv: Adv):
    try:
        request.session.add(adv)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(409, "adv already exists")
    return adv

def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)

class Userview(MethodView):
    def post(self):
        json_data = validate(CreateUser, request.json)
        user = User(**json_data)
        add_user(user)
        response = jsonify(user.json)
        return response

class Advview(MethodView):

    def get(self, adv_id: int):
        adv = get_adv_by_id(adv_id)
        return jsonify(adv.json)

    def post(self):
        json_data = validate(CreateAdv, request.json)
        adv = Adv(**json_data)
        add_adv(adv)
        response = jsonify(adv.json)
        return response

    def delete(self, adv_id: int):
        adv = get_adv_by_id(adv_id)
        request.session.delete(adv)
        request.session.commit()
        return jsonify({"status": "success"})

adv_view = Advview.as_view('adv_view')
user_view = Userview.as_view('user_view')

app.add_url_rule(rule='/adv', view_func='adv_view', methods=['POST'])
app.add_url_rule(rule='/adv/<int:adv_id>', view_func='adv_view', methods=['GET', 'DELETE'])
app.add_url_rule(rule='/user', view_func='user_view', methods=['POST'])

app.run()
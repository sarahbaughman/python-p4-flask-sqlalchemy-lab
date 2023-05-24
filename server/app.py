from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    response_body = f'''
        <ul>ID: {animal.id}</ul>
        <ul>Name: {animal.name}</ul>
        <ul>Species: {animal.species}</ul>
        <ul>Zookeeper: {animal.zookeeper.name}</ul>
        <ul>Enclosure: {animal.enclosure.environment}</ul>
    '''
    # response_body += f'<ul>ID: {animal.id}</ul>'
    # response_body += f'<ul>Name: {animal.name}</ul>'
    # response_body += f'<ul>Species: {animal.species}</ul>'
    # response_body += f'<ul>Zookeeper: {animal.zookeeper.name}</ul>'
    # response_body += f'<ul>Enclosure: {animal.enclosure.environment}</ul>'
    
    response = make_response(response_body, 200)
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()

    if not zookeeper:
            response_body = '<h1>404 Error: Zookeeper not found.</h1>'
            return make_response(response_body, 404)
    
    response_body = f'''
        <ul>ID: {zookeeper.id}</ul>
        <ul>Name: {zookeeper.name}</ul>
        <ul>Birthday: {zookeeper.birthday}</ul>
        '''
    
    for animal in zookeeper.animals:
        response_body += f'<ul>Animal: {animal.name}</ul>'

    # animals = [animal for animal in zookeeper.animals]

    # if not animals:
    #     response_body = f'<h1>{zookeeper.name} has no animals right now.</h1>'
    
    # else: 
    #     for animal in animals:
    #         response_body += f'<h1>Animal:{animal.name} </h1>'
    response = make_response(response_body, 200)
    
    return response


@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()

    if not enclosure:
            response_body = '<h1>404 Error: Enclosure not found.</h1>'
            return make_response(response_body, 404)
    
    response_body = f'''
        <ul>ID: {enclosure.id}</ul>
        <ul>Environment: {enclosure.environment}</ul>
        <ul>Open to Visitors: {enclosure.open_to_visitors}</ul>
        '''
    
    for animal in enclosure.animals:
        response_body += f'<ul>Animal: {animal.name}</ul>'

    
    # animals = [animal for animal in enclosure.animals]

    # if not animals:
    #     response_body = f'<h1>{enclosure.environment} has no animals right now.</h1>'
    
    # else: 
    #     for animal in animals:
    #         response_body += f'<h1>Animal:{animal.name} </h1>'
    response = make_response(response_body, 200)
    
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)

from flask import Flask, url_for, redirect
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
app.config['SECRET_KEY'] = "123"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

class cliente(db.Model):
    id = db.Column("cliente_id", db.Integer, primary_key = True)
    cliente_nombre = db.Column(db.String(100))
    cliente_telefono = db.Column(db.String(100))
    cliente_direccion = db.Column(db.String(100))
    cliente_usuario = db.Column(db.String(100))

    def __init__(self,datos):
        self.cliente_nombre = datos["nombre"]
        self.cliente_telefono = datos["telefono"]
        self.cliente_direccion = datos["direccion"]
        self.cliente_usuario = datos["usuario"]

@app.route("/")
@cross_origin()
def principal():
    data = cliente.query.all()
    diccionario_cliente = {}
    for d in data:
        p = {"id": d.id,
             "nombre":d.cliente_nombre,
              "telefono": d.cliente_telefono,
              "direccion": d.cliente_direccion,
              "usuario": d.cliente_usuario,
              }
        diccionario_cliente[d.id] = p
    return diccionario_cliente

@app.route("/agregar/<nombre>/<telefono>/<direccion>/<usuario>")
@cross_origin()
def agregar(nombre, telefono, direccion,usuario):
    datos = {"nombre": nombre,
            "telefono": telefono,
            "direccion": direccion,
            "usuario": usuario
            }
    p = cliente(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/eliminar/<int:id>")
@cross_origin()
def eliminar(id):
    p = cliente.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/actualizar/<int:id>/<nombre>/<telefono>/<direccion>/<usuario>")
@cross_origin()
def actualizar(id,nombre, telefono, direccion,usuario):
    p = cliente.query.filter_by(id=id).first()
    p.cliente_nombre = nombre
    p.cliente_telefono = telefono
    p.cliente_direccion = direccion
    p.cliente_usuario = usuario
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/buscar/<int:id>")
@cross_origin()
def buscar(id):
    d = cliente.query.filter_by(id=id).first()
    p = {"id": d.id,
        "nombre":d.cliente_nombre,
        "telefono": d.cliente_telefono,
        "direccion": d.cliente_direccion,
        "usuario": d.cliente_usuario
        }
    return p

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
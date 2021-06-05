from flask import Flask, url_for, redirect
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pedidos.db'
app.config['SECRET_KEY'] = "123"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

class pedido(db.Model):
    id = db.Column("pedido_id", db.Integer, primary_key = True)
    pedido_idCliente = db.Column(db.Integer)
    pedido_idProducto = db.Column(db.Integer)
    pedido_cantidad = db.Column(db.Integer)

    def __init__(self,datos):
        self.pedido_idCliente = datos["idCliente"]
        self.pedido_idProducto = datos["idProducto"]
        self.pedido_cantidad = datos["cantidad"]

@app.route("/")
@cross_origin()
def principal():
    data = pedido.query.all()
    diccionario_pedido = {}
    for d in data:
        p = {"id": d.id,
             "idCliente":d.pedido_idCliente,
              "idProducto": d.pedido_idProducto,
              "cantidad": d.pedido_cantidad
              }
        diccionario_pedido[d.id] = p
    return diccionario_pedido

@app.route("/agregar/<int:idCliente>/<int:idProducto>/<int:cantidad>")
@cross_origin()
def agregar(idCliente, idProducto, cantidad):
    datos = {"idCliente": idCliente,
            "idProducto": idProducto,
            "cantidad": cantidad
            }
    p = pedido(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/eliminar/<int:id>")
@cross_origin()
def eliminar(id):
    p = pedido.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/actualizar/<int:id>/<int:idCliente>/<int:idProducto>/<int:cantidad>")
@cross_origin()
def actualizar(id,idCliente, idProducto, cantidad):
    p = pedido.query.filter_by(id=id).first()
    p.pedido_idCliente = idCliente
    p.pedido_idProducto = idProducto
    p.pedido_cantidad = cantidad
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/buscar/<int:id>")
@cross_origin()
def buscar(id):
    d = pedido.query.filter_by(id=id).first()
    p = {"id": d.id,
        "idCliente":d.pedido_idCliente,
        "idProducto": d.pedido_idProducto,
        "cantidad": d.pedido_cantidad
        }
    return p

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
from flask import Flask, url_for, redirect
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///domiciliarios.db'
app.config['SECRET_KEY'] = "123"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

class domiciliario(db.Model):
    id = db.Column("domiciliario_id", db.Integer, primary_key = True)
    domiciliario_nombre = db.Column(db.String(100))
    domiciliario_telefono = db.Column(db.String(100))
    domiciliario_idTienda = db.Column(db.Integer)
    domiciliario_habilitado = db.Column(db.String(2))

    def __init__(self,datos):
        self.domiciliario_nombre = datos["nombre"]
        self.domiciliario_telefono = datos["telefono"]
        self.domiciliario_idTienda = datos["idTienda"]
        self.domiciliario_habilitado = datos["habilitado"]

@app.route("/")
@cross_origin()
def principal():
    data = domiciliario.query.all()
    diccionario_domiciliario = {}
    for d in data:
        p = {"id": d.id,
             "nombre":d.domiciliario_nombre,
              "telefono": d.domiciliario_telefono,
              "idTienda": d.domiciliario_idTienda,
              "habilitado": d.domiciliario_habilitado,
              }
        diccionario_domiciliario[d.id] = p
    return diccionario_domiciliario

@app.route("/agregar/<nombre>/<telefono>/<int:idTienda>/<habilitado>")
@cross_origin()
def agregar(nombre, telefono, idTienda,habilitado):
    datos = {"nombre": nombre,
            "telefono": telefono,
            "idTienda": idTienda,
            "habilitado": habilitado
            }
    p = domiciliario(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/eliminar/<int:id>")
@cross_origin()
def eliminar(id):
    p = domiciliario.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/actualizar/<int:id>/<nombre>/<telefono>/<int:idTienda>/<habilitado>")
@cross_origin()
def actualizar(id,nombre, telefono, idTienda,habilitado):
    p = domiciliario.query.filter_by(id=id).first()
    p.domiciliario_nombre = nombre
    p.domiciliario_telefono = telefono
    p.domiciliario_idTienda = idTienda
    p.domiciliario_habilitado = habilitado
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/buscar/<int:id>")
@cross_origin()
def buscar(id):
    d = domiciliario.query.filter_by(id=id).first()
    p = {"id": d.id,
        "nombre":d.domiciliario_nombre,
        "telefono": d.domiciliario_telefono,
        "idTienda": d.domiciliario_idTienda,
        "habilitado": d.domiciliario_habilitado
        }
    return p

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
from app import db
from datetime import datetime

class Ingreso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

class Egreso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

class MetaAhorro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad_objetivo = db.Column(db.Float, nullable=False)
    cantidad_actual = db.Column(db.Float, default=0.0)
    fecha_limite = db.Column(db.DateTime, nullable=True)

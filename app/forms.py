from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, NumberRange

class IngresoForm(FlaskForm):
    descripcion = StringField('Descripción', validators=[DataRequired(message="La descripción es obligatoria."), Length(max=100)])
    cantidad = FloatField('Cantidad', validators=[
        DataRequired(message="La cantidad es obligatoria."),
        NumberRange(min=0.01, message="La cantidad debe ser mayor que cero.")
    ])
    submit = SubmitField('Agregar Ingreso')


class EgresoForm(FlaskForm):
    descripcion = StringField('Descripción', validators=[DataRequired(message="La descripción es obligatoria."), Length(max=100)])
    cantidad = FloatField('Cantidad', validators=[
        DataRequired(message="La cantidad es obligatoria."),
        NumberRange(min=0.01, message="La cantidad debe ser mayor que cero.")
    ])
    submit = SubmitField('Agregar Egreso')


class MetaAhorroForm(FlaskForm):
    nombre = StringField('Nombre de la Meta', validators=[DataRequired(message="El nombre es obligatorio."), Length(max=100)])
    cantidad_objetivo = FloatField('Cantidad Objetivo', validators=[
        DataRequired(message="La cantidad objetivo es obligatoria."),
        NumberRange(min=1.0, message="La cantidad debe ser mayor que cero.")
    ])
    fecha_limite = DateField('Fecha Límite (opcional)', format='%Y-%m-%d', validators=[], default=None)
    submit = SubmitField('Crear Meta')


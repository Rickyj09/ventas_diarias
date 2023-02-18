from random import choices
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField,\
    TextAreaField, SelectField, PasswordField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField
from wtforms.validators import Required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, FileField, SelectField, RadioField
from wtforms import FloatField
from wtforms.validators import DataRequired, Email, Length, ValidationError, AnyOf
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required


def validar_obvio(form, field):
    if field.data == "12345678":
        raise ValidationError('La clave debe ser más segura!!')


class buscaform(FlaskForm):
    iden = StringField('Número Reporte', validators=[DataRequired(),Length(min=10,max=14)], render_kw={"placeholder": ""})
    submit = SubmitField('Buscar')


class Publicaciones(FlaskForm):
    post = TextAreaField('Notas de las fotos', validators=[
        DataRequired(), Length(min=1, max=140)
    ])
    imagen = FileField('image')

    submit = SubmitField('Subir')


class FormArticulo(FlaskForm):
    nombre = StringField("Nombre:",
                         validators=[Required("Tienes que introducir el dato")]
                         )
    precio = DecimalField("Precio:", default=0,
                          validators=[Required("Tienes que introducir el dato")
                                      ])
    iva = IntegerField("IVA:", default=21,
                       validators=[Required("Tienes que introducir el dato")])
    descripcion = TextAreaField("Descripción:")
    photo = FileField('Selecciona imagen:')
    stock = IntegerField("Stock:", default=1,
                         validators=[Required("Tienes que introducir el dato")]
                         )
    CategoriaId = SelectField("Categoría:", coerce=int)
    submit = SubmitField('Enviar')


class FormSINO(FlaskForm):
    si = SubmitField('Si')
    no = SubmitField('No')


class LoginForm(FlaskForm):
    username = StringField('User', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Entrar')


class FormUsuario(FlaskForm):
    username = StringField('Login', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    nombre = StringField('Nombre completo')
    email = EmailField('Email')
    
    submit = SubmitField('Aceptar')



class list_formulario(FlaskForm):
    nombre = SelectField('Formulario', choices=[('Reporte Inspeccion Poleas', 'Poleas'), ('Formato Inspección visual Eslinga Cable Acero', 'Eslinga Cable Acero'),('Reporte Inspección Cadena','Cadena'),('Reporte Inspección visual Eslinga Faja Sintética','Eslinga Faja Sintética'),('Reporte Inspección visual Ganchos','Ganchos'),('Reporte Inspección visual Grilletes','Grilletes'),('Reporte Inspeccion King Pin','King Pin'),('Reporte Inspeccion Quinta Rueda','Quinta Rueda'),('Reporte Inspeccion Sistemas de Elevación de Personal','Sistemas de Elevación de Personal'),('Reporte Inspeccion Horquillas','Horquillas'),('Reporte Inspección  Pasteca Principal','Pasteca Principal'),('Reporte Inspeccion Pasteca Auxiliar','Pasteca Auxiliar'),('Reporte Inspección Aparejos','Aparejos'),('Reporte Inspección Tensor Trinquete','Tensor Trinquete')])
    
    submit = SubmitField('Enviar')

class diario(FlaskForm):
    costo = StringField('valor venta', validators=[DataRequired()])
    nombre = StringField('descripción', validators=[DataRequired()])
    
    submit = SubmitField('Enviar')

class FormChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Aceptar')


class UploadForm(FlaskForm):
    photo = FileField('selecciona imagen:', validators=[FileRequired()])
    submit = SubmitField('Submit')

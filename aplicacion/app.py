from http.client import OK
from pydoc import html
from typing import Text
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from aplicacion import config
from aplicacion.forms import diario
from aplicacion.forms import LoginForm, UploadForm
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import DateField
from jinja2 import Environment, FileSystemLoader
from os import listdir
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
from aplicacion.forms import LoginForm, FormUsuario
import pdfkit
import os

import xhtml2pdf.pisa as pisa
from io import StringIO
#from flask_weasyprint import HTML, render_pdf



UPLOAD_FOLDER = os.path.abspath("./static/uploads/")
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpge"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'ventas'
mysql = MySQL(app)

# setting
app.secret_key = 'millave'


@login_manager.user_loader
def load_user(user_id):
    return (user_id)


@app.route('/')
def inicio():
    return render_template("inicio.html")


@app.route('/inicio_1')
@app.route('/inicio_1/<id>')
def inicio_1(id='0'):
    from aplicacion.models import Articulos, Categorias
    categoria = Categorias.query.get(id)
    if id == '0':
        articulos = Articulos.query.all()
    else:
        articulos = Articulos.query.filter_by(CategoriaId=id)
    categorias = Categorias.query.all()
    return render_template("inicio_1.html", articulos=articulos, categorias=categorias, categoria=categoria)


@app.route('/inicio_new')
@app.route('/inicio_new/<id>')
def inicio_new(id='0'):
    from aplicacion.models import Articulos, Categorias
    categoria = Categorias.query.get(id)
    if id == '0':
        articulos = Articulos.query.all()
    else:
        articulos = Articulos.query.filter_by(CategoriaId=id)
    categorias = Categorias.query.all()
    return render_template("inicio_new.html", articulos=articulos, categorias=categorias, categoria=categoria)


@login_manager.user_loader
def load_user(user_id):
    from aplicacion.models import Usuarios
    return Usuarios.query.get(int(user_id))


@app.route('/upload', methods=['get', 'post'])
def upload():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/"+filename)
        return redirect(url_for('inicio_foto'))
    return render_template('upload.html', form=form)


@app.route('/upload_1', methods=['get', 'post'])
def upload_1():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/"+filename)
        return redirect(url_for('reporte_foto'))
    return render_template('upload_1.html', form=form)


@app.route('/inicio_foto')
@login_required
def inicio_foto():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/"):
        lista.append(file)
    return render_template("inicio_foto.html", lista=lista)



@app.route('/diario_venta', methods=['GET', 'POST'])
@login_required
def diario_venta():
    form = diario()
    if form.validate_on_submit():
        costo = request.form['costo']
        nombre = request.form['nombre']
        cursor = mysql.connection.cursor()
        cursor.execute("select CURDATE();")
        fecha_hoy = cursor.fetchone()
        cursor.execute('insert into diario (precio,descrip,fecha) VALUES (%s,%s,%s)',(costo, nombre,fecha_hoy))
        mysql.connection.commit()
        
        return redirect(url_for('dv_1'))

    return render_template('diario_venta.html', form=form)





@app.route('/total_dia', methods=['GET', 'POST'])
@login_required
def total_dia():
    form = diario()
    cursor = mysql.connection.cursor()
    cursor.execute("select CURDATE();")
    fecha_hoy = cursor.fetchone()
    cursor.execute("select sum(precio), fecha from diario where fecha = %s;", [fecha_hoy]) 
    data = cursor.fetchall()
    return render_template('total_dia.html',form=form, data=data)


@app.route('/dv_1', methods=['GET', 'POST'])
@login_required
def dv_1():
    form = diario()
    cursor = mysql.connection.cursor()
    cursor.execute("select CURDATE();")
    fecha_hoy = cursor.fetchone()
    cursor.execute("select * from diario where fecha = %s;", [fecha_hoy]) 
    data = cursor.fetchall()
    return render_template('diario_venta.html',form=form, data=data)

@app.route('/edit-venta/<id>', methods=['POST', 'GET'])
@login_required
def get_venta(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM diario WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-venta.html', contact=data[0])



@app.route('/update_venta/<id>', methods=['POST'])
@login_required
def update_venta(id):
    if request.method == 'POST':
        valor = request.form['valor']
        desc = request.form['desc']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE diario
            SET precio = %s,
                descrip = %s
            WHERE id = %s
        """, (valor, desc, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('dv_1'))



@app.route('/edit-venta1/<id>', methods=['POST', 'GET'])
@login_required
def get_venta1(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM diario WHERE id = %s ', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frapa1.html', contact=data[0])


       

@app.route('/update_frapa1/<id>', methods=['POST'])
@login_required
def update_frapa1(id):
    if request.method == 'POST':
        num = request.form['num']
        ref = request.form['ref']
        cod_enii = request.form['cod_enii']
        medidas = request.form['medidas']
        capac = request.form['capac']
        medida_cu = request.form['medida_cu']
        tipo_acc = request.form['tipo_acc']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frapa1
            SET num = %s,
                ref = %s, 
                cod_enii = %s,
                medidas = %s,
                capac = %s,
                medida_cu = %s,
                tipo_acc = %s,
				vt = %s,
                pt = %s
            WHERE num = %s
        """, (num,ref, cod_enii, medidas, capac,medida_cu,tipo_acc, vt, pt, num))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('frapa1'))








@app.route('/REP_FOTO_CARGA', methods=['GET', 'POST'])
@login_required
def REP_FOTO_CARGA():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/"+filename)
        return redirect(url_for('inicio_foto'))
    return render_template('REP_FOTO_CARGA.html', form=form)



@app.route('/reporte_fotofrgba')
@login_required
def reporte_fotofrgba():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/freca/"):
        lista.append(file)
    return render_template("reporte_fotofrgba.html", lista=lista)


@app.route('/upload_frgba', methods=['get', 'post'])
def upload_frgba():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/frgba/"+filename)
        foto = app.root_path+"/static/img/subidas/frgba/"+filename
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select MAX(id_formulario) from formulario where llave_formulario = 'FR-INPS-009.02';")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_frgba (foto,id_f) VALUES (%s,%s)',
                    ( foto,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotofrgba'))
    return render_template('upload_frgba.html', form=form)

@app.route('/inicio_fotofrgba')
@login_required
def inicio_fotofrgba():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frgba/"):
        lista.append(file)
    return render_template("inicio_fotofrgba.html", lista=lista)


@app.route('/REP_FOTO', methods=['GET', 'POST'])
@login_required
def REP_FOTO():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/"+filename)
        return redirect(url_for('reporte_foto'))
    return render_template('REP_FOTO.html', form=form)





@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404


@app.route('/cons_404', methods=['GET', 'POST'])
def cons_404():
    return render_template('404_cons.html')


@app.route('/login', methods=['get', 'post'])
def login():
    from aplicacion.models import Usuarios
    # Control de permisos
    if current_user.is_authenticated:
        # return 'OK'
        return redirect(url_for("inicio_new"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(username=form.username.data).first()
        print(user)
        pas1 = Usuarios.query.filter_by(password=form.password.data).first()
        print(pas1)
        pas = user.verify_password(form.password.data)
        print(pas)
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('inicio_new'))
        form.username.errors.append("Usuario o contraseña incorrectas.")
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('inicio'))


@app.route('/perfil/<username>', methods=["get", "post"])
@login_required
def perfil(username):
    from aplicacion.models import Usuarios
    user = Usuarios.query.filter_by(username=username).first()
    if user is None:
        render_template("404.html")
    form = FormUsuario(request.form, obj=user)
    del form.password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("usuarios_new.html", form=form, perfil=True)


@login_manager.user_loader
def load_user(user_id):
    from aplicacion.models import Usuarios
    return Usuarios.query.get(int(user_id))





@app.route('/listar_form/<id>', methods=['POST', 'GET'])
@login_required
def listar_form(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frpol  ')
    data1 = cur.fetchall()
    cur.close()
    print(data1)
    return render_template('listar_form.html')

from flask import render_template, session, Blueprint, request, url_for, redirect
import mysql.connector
from app.db_config import db_config

login_bp = Blueprint('login', __name__)

@login_bp.route('/login')
def login():
    return render_template('login.html')

@login_bp.route('/datos-login', methods=['GET', 'POST'])
def datos():
    cnx = mysql.connector.connect(**db_config)
    if request.method == 'POST':
        nombres = request.form['Usuario']
        contraseña = request.form['Contraseña']
        cursor = cnx.cursor()
        sql = "SELECT * FROM usuario WHERE NombresUsuario=%s AND ContraseñaUsuario=%s"
        data = (nombres, contraseña)
        cursor.execute(sql, data)
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['usuario'] = {
                'id': user[0],
                'nombre': user[1],
                'correo': user[13],
                'rol': user[21],
                
            }
            print(session['usuario']['rol'])
            if session['usuario']['rol'] == 1:
                return redirect(url_for('admin.admin'))
            return redirect(url_for('home.home'))
        else:
            return "Inicio de sesion fallido"
    return render_template('login.html')


@login_bp.route('/formulario-usuario', methods=['POST'])
def formulario_u():
    
    cnx = mysql.connector.connect(**db_config)
    nombre = request.form['nombres']
    p_apellido = request.form['p_apellido']
    s_apellido = request.form['s_apellido']
    telefono = request.form['celular_u']
    tipo_documento = request.form['tipo_documento']
    numero_documento = request.form['numero_documento']
    direccion = request.form['direccion']
    correo = request.form['correo']
    contrasena = request.form['contraseña']
    estado = 'activo'
    rol = 3
    sql = "insert into usuario (NombresUsuario, PrimerApellidoUsuario, SegundoApellidoUsuario, CelularUsuario, TipoDocumentoUsuario, NumeroDocumentoUsuario,   DireccionUsuario,  CorreoUsuario, ContraseñaUsuario, EstadoUsuario, FK_IdRol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" # Parámetros de la consulta SQL   
    data = (nombre,p_apellido, s_apellido, telefono, tipo_documento, numero_documento, direccion, correo, contrasena, estado, rol)
    
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    cursor.close()
    cnx.commit()
    cnx.close()
    return  render_template('login.html', mensaje="Registrado ingrese su usuario")

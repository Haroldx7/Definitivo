from flask import Blueprint, render_template, request, session, redirect, url_for
import mysql.connector
from app.db_config import db_config

formulario_bp = Blueprint('formulario', __name__)


@formulario_bp.route('/formulario/empleados')
def formulario():
    usuario = None
    if 'usuario' in session:
        if session['usuario']['rol'] == 1:
            usuario = session['usuario']
    return render_template('formulario.html', usuario=usuario)


@formulario_bp.route('/procesar-datos', methods=['GET','POST'])
def procesar_datos(): 
    cnx = mysql.connector.connect(**db_config)
    nombres = request.form['nombres']
    p_apellido = request.form['p_apellido']
    s_apellido = request.form['s_apellido']
    genero = request.form['genero']
    tipo_documento = request.form['tipo_documento']
    numero_documento = int(request.form['numero_documento'])
    fecha_nacimiento = request.form['fecha_nacimiento']
    celular_u = int(request.form['celular_u'])
    celular_d = int(request.form['celular_d'])
    direccion = request.form['direccion']
    estrato = request.form['estrato']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    estadocivil = request.form['estado_civil']
    personasacargo = request.form['personasacargo']
    LibretaMilitar = request.form['LibretaMilitar']
    Contenido = request.form['Contenido']
    rol = 2
    Estado = 'ACTIVO'
    cursor = cnx.cursor()
    sql = "insert into usuario (NombresUsuario, PrimerApellidoUsuario, SegundoApellidoUsuario, GeneroUsuario, TipoDocumentoUsuario, NumeroDocumentoUsuario, FechaNacimiento, CelularUsuario, Celular2Usuario, DireccionUsuario, EstratoResidencia, CorreoUsuario, ContraseñaUsuario, EstadoCivil, PersonasACargo, LibretaMilitar, ContenidoPerfil, FK_IdRol, EstadoUsuario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" # Parámetros de la consulta SQL   
    data = (nombres, p_apellido, s_apellido, genero, tipo_documento, numero_documento, fecha_nacimiento, celular_u, celular_d, direccion, estrato, correo, contraseña, estadocivil, personasacargo, LibretaMilitar, Contenido, rol, Estado)
    cursor.execute(sql, data)
    cnx.commit()    
    sql = 'select * from usuario where NumeroDocumentoUsuario = %s'
    cursor.execute(sql, (tipo_documento))
    result = cursor.fetchone()
    nombre = result

    cursor.close()
    cnx.close()
    if 'usuario' in session:
        rol = session['usuario']['rol']
        if rol == 1:
            return redirect(url_for('admin.admin'))
    return redirect(url_for('formulario.habilidad', nombre=nombre))

@formulario_bp.route('/habilidad')
def habilidad():
    usuario = None
    if 'usuario' in session:
        if session['usuario']['rol'] == 1:
            usuario = session['usuario']
    return render_template('habilidades.html', usuario=usuario)

@formulario_bp.route('/procesar-datos-habildad', methods=['POST'])
def datoshabilidad():
    nombre_habilidad = request.form['nombre_habilidad']
    descripcion = request.form['descripcion']
    nivel = request.form['nivel']
    categoria = request.form['categoria'] 
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    sql= "insert into habilidades(NombreHabilidad, DescipcionHabilidad, current_Nivel, FK_IdCategoria) values (%s, %s, %s, %s)"
    datos = (nombre_habilidad, descripcion, nivel, categoria)
    cursor.execute(sql, datos)
    cnx.commit()
    cursor.close()
    cnx.close()

    return render_template('resultado.html')

from flask import Blueprint, render_template, redirect, request
import mysql.connector
from app.db_config import db_config


crud_bp = Blueprint('crud', __name__)

@crud_bp.route('/consultas')
def mostrar_empleados(): 
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()  
    sql = "SELECT * FROM usuario"
    try:     
        cursor.execute(sql)     
        empleados = cursor.fetchall()
    except mysql.connector.Error as error:       
        print("Error al obtener los empleados:", error)
        empleados = []  
    cursor.close()
    cnx.close()  
    return render_template('/consultas.html', empleados=empleados)



@crud_bp.route('/eliminar/<int:id>')
def eliminar_empleados(id):  
    cnx = mysql.connector.connect(**db_config) # Consulta SQL para insertar los datos en la tabla "empleados"   
    cursor = cnx.cursor() # Eliminar SQL para obtener los datos de todos los empleados         # Ejecutar la consulta SQL 
    sql = "UPDATE usuario SET Estadousuario = IF(Estadousuario = 'ACTIVO', 'INACTIVO', 'ACTIVO') WHERE IdUsuario = %s;"
    cursor.execute(sql, (id,))
    cnx.commit()
    cursor.close()
    cnx.close() # Retornar los empleados a la plantilla HTML para mostrarlos   
    return redirect('/consultas')

@crud_bp.route('/editar/<int:id>')
def editar(id):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    
    sql = "SELECT * FROM usuario WHERE IdUsuario = %s"
    try:
        cursor.execute(sql, (id,))
        empleados = cursor.fetchall()
        cnx.commit()
    except mysql.connector.Error as error:
        
        print("Error al obtener los empleados:", error)
        empleados = []
    return render_template('/modificar.html',empleados=empleados)



@crud_bp.route('/actualizar', methods=['POST'])

def actualizar():
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
    rol = request.form['rol']
    Barrio = request.form['Barrio']
    Estado = request.form['Estado']
    id=request.form['id']
    cursor = cnx.cursor()
    
    sql = "UPDATE usuario SET NombresUsuario=%s, PrimerApellidoUsuario=%s, SegundoApellidoUsuario=%s, GeneroUsuario=%s, TipoDocumentoUsuario=%s, NumeroDocumentoUsuario=%s, FechaNacimiento=%s, CelularUsuario=%s, Celular2Usuario=%s, DireccionUsuario=%s, EstratoResidencia=%s, CorreoUsuario=%s, ContraseñaUsuario=%s, EstadoCivil=%s, PersonasACargo=%s, Libreta=%s, contenido=%s, FK_IdRol=%s, ZonaResidencia=%s, Estado=%s WHERE IdUsuario=%s"

    data = (nombres, p_apellido, s_apellido, genero, tipo_documento, numero_documento, fecha_nacimiento, celular_u, celular_d, direccion, estrato, correo, contraseña, estadocivil, personasacargo, LibretaMilitar, Contenido, rol, Barrio, Estado, id)
    cursor.execute(sql, data)
    cnx.commit()
    cursor.close()
    cnx.close() 
    return redirect('/consultas') 

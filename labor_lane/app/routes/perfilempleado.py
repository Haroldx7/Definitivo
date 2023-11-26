from flask import Blueprint, render_template, session, redirect, current_app, url_for, send_from_directory, request
import mysql.connector
from werkzeug.utils import secure_filename
import os
from app.db_config import db_config


perfilempleado_bp = Blueprint('perfilempleado', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@perfilempleado_bp.route('/perfilempleado/<int:id_usuario>', methods=['GET'])
def perfilempleado(id_usuario):

    if 'usuario' in session:
        if session['usuario']['rol'] == 3:
            sesion = session['usuario']
            id_usuario = id_usuario

            cnx = mysql.connector.connect(**db_config)
            cursor = cnx.cursor(dictionary=True)
            # Obtener el nombre de la imagen asociada al usuario
            sql = 'SELECT NombreImagen FROM usuario WHERE IdUsuario = %s'
            cursor.execute(sql, (id_usuario,))
            result = cursor.fetchone()
            cursor.close()
            cnx.commit()
            cnx.close()

            cnx = mysql.connector.connect(**db_config)
            cursor = cnx.cursor(dictionary=True)
            sql = 'SELECT * FROM usuario where IdUsuario = %s'
            cursor.execute(sql, (id_usuario,))
            datos = cursor.fetchone()
            print(datos['ContenidoPerfil'])
            cursor.close()
            cnx.commit()
            cnx.close()

            url_imagen = None
            if result and 'NombreImagen' in result and result['NombreImagen']:
                nombre_imagen = result['NombreImagen']
                print(nombre_imagen)
                url_imagen = url_for('perfilempleado.serve_image', filename=nombre_imagen)

            else:
                url_imagen = url_for('perfilempleado.serve_image', filename='logo.png')

            return render_template('perfilempleado.html', nombre=session['usuario']['nombre'], url_imagen=url_imagen, sesion=sesion, datos=datos)
        
        if session['usuario']['rol'] == 2:
            sesion = session['usuario']


            cnx = mysql.connector.connect(**db_config)
            cursor = cnx.cursor(dictionary=True)
            # Obtener el nombre de la imagen asociada al usuario
            sql = 'SELECT NombreImagen FROM usuario WHERE IdUsuario = %s'
            cursor.execute(sql, (id_usuario,))
            result = cursor.fetchone()
            cursor.close()
            cnx.commit()
            cnx.close()

            cnx = mysql.connector.connect(**db_config)
            cursor = cnx.cursor(dictionary=True)
            sql = 'SELECT * FROM usuario where IdUsuario = %s'
            cursor.execute(sql, (id_usuario,))
            datos = cursor.fetchone()
            print(datos['ContenidoPerfil'])
            cursor.close()
            cnx.commit()
            cnx.close()

            url_imagen = None
            if result and 'NombreImagen' in result and result['NombreImagen']:
                nombre_imagen = result['NombreImagen']
                print(nombre_imagen)
                url_imagen = url_for('perfilempleado.serve_image', filename=nombre_imagen)

            else:
                url_imagen = url_for('perfilempleado.serve_image', filename='logo.png')

            return render_template('perfilempleado.html', nombre=session['usuario']['nombre'], url_imagen=url_imagen, sesion=sesion, datos=datos)
    return redirect(url_for('login.login'))




@perfilempleado_bp.route('/guardar-imagen-empleado', methods=['POST'])
def guardar_imagen_empleado():
    if 'usuario' in session:
        id_usuario = session['usuario']['id']

        if 'imagen' not in request.files:
            return 'No file part'

        file = request.files['imagen']

        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            
            cnx = mysql.connector.connect(**db_config)
            sql = 'UPDATE usuario SET NombreImagen = %s WHERE IdUsuario = %s'
            cursor = cnx.cursor()
            data = (filename, id_usuario)
            cursor.execute(sql,data)    
            cnx.commit()
            cursor.close()
            cnx.close()
            return redirect(url_for('perfilempleado.perfilempleado', id_usuario=id_usuario))
    return redirect(url_for('home.home'))



@perfilempleado_bp.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
from flask import Blueprint, render_template, session, redirect, url_for, request, current_app, send_from_directory
import mysql.connector
from werkzeug.utils import secure_filename
import os
from app.db_config import db_config


perfilcliente_bp = Blueprint('perfilcliente', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']



@perfilcliente_bp.route('/perfilcliente', methods=['GET'])   
def perfilcliente():
    if 'usuario' in session:
        id_usuario = session['usuario']['id']

        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)

        # Obtener el nombre de la imagen asociada al usuario
        sql = 'SELECT NombreImagen FROM usuario WHERE IdUsuario = %s'
        cursor.execute(sql, (id_usuario,))
        result = cursor.fetchone()


        url_imagen = None
        if result and 'NombreImagen' in result and result['NombreImagen']:
            nombre_imagen = result['NombreImagen']
            print(nombre_imagen)
            url_imagen = url_for('perfilcliente.serve_image', filename=nombre_imagen)

        else:
            url_imagen = url_for('perfilcliente.serve_image', filename='logo.png')
        
        sql = 'select a.IdAplicaciones, o.IdEmpleo,o.TituloEmpleo, o.DescripcionEmpleo, o.RequisitosEmpleo, o.FechaPublicacion, o.EstadoOferta ,u.IdUsuario, a.FK_IdEmpleo,a.EstadoAplicacion, a.FechaAplicacion, a.ValorSugerido, u.NombresUsuario, u.NombreImagen from aplicaciones a inner join ofertaempleo o on IdEmpleo = FK_IdEmpleo inner join usuario u on u.IdUsuario = a.FK_IdUsuario  where o.FK_IdUsuario = %s'
        cursor.execute(sql, (id_usuario,))
        result = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        print(result)

        url_imagen_aplicacion = None
        if result and result[0] and 'NombreImagen' in result[0] and result[0]['NombreImagen']:
            nombre_imagen = result[0]['NombreImagen']
            print(nombre_imagen)
            url_imagen_aplicacion = url_for('perfilempleado.serve_image', filename=nombre_imagen)

        else:

            url_imagen_aplicacion = url_for('perfilempleado.serve_image', filename='1.png')


        return render_template('perfilcliente.html', sesion=session['usuario'], url_imagen=url_imagen, aplicaciones=result, url_imagen_aplicacion=url_imagen_aplicacion)
    return redirect(url_for('login.login'))





@perfilcliente_bp.route('/guardar-imagen', methods=['POST'])
def guardar_imagen():
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
            return redirect(url_for('perfilcliente.perfilcliente'))
    return redirect(url_for('home.home'))



@perfilcliente_bp.route('/desactivar-oferta/<int:id>')
def desactivaoferta(id):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    sql = 'update ofertaempleo set EstadoOferta = "Inactiva" where idEmpleo = %s'
    cursor.execute(sql, (id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('perfilcliente.perfilcliente'))



@perfilcliente_bp.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
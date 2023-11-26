from flask import Blueprint, redirect, render_template, url_for, request, session
import mysql.connector
from app.db_config import db_config


ofertaempleo_bp = Blueprint('ofertaempleo', __name__)


@ofertaempleo_bp.route('/oferta-empleo')
def ofertaempleo():
    if 'usuario' in session:
        sesion = session['usuario']

    return render_template('ofertaempleo.html')




@ofertaempleo_bp.route('/datos-ofertaempleo', methods=['POST'])
def oferta():
    if 'usuario' in session:
        id_usuario = session['usuario']['id']
        tituloEmpleo = request.form['tituloEmpleo']
        descripcionEmpleo = request.form['descripcionEmpleo']
        requisitosEmpleo = request.form['requisitosEmpleo']
        habilidadesEmpleo = request.form['habilidadesEmpleo']
        fechaPublicacion = request.form['fechaPublicacion']
        fechaVencimiento = request.form['fechaVencimiento']
        categoria = request.form['categoria']
        estado = 'Activa'

        cnx = mysql.connector.connect(**db_config)  
        cursor = cnx.cursor()
        
        sql = "insert into ofertaempleo (TituloEmpleo, DescripcionEmpleo, RequisitosEmpleo, HabilidadesEmpleo, FechaPublicacion, FechaVencimiento, EstadoOferta, FK_IdCategoria, FK_IdUsuario) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        datos = (tituloEmpleo, descripcionEmpleo, requisitosEmpleo, habilidadesEmpleo, fechaPublicacion, fechaVencimiento, estado, categoria, id_usuario)
    

        cursor.execute(sql, datos)

        cursor.close()
        cnx.commit()  
        cnx.close()
        
        return redirect(url_for('perfilcliente.perfilcliente'))

    return render_template('ofertaempleo.html')


@ofertaempleo_bp.route('/aceptar-oferta/<int:idEmpleo>/<int:idEmpleado>', methods=['POST', 'GET'])
def aceptaroferta(idEmpleo, idEmpleado):
    if 'usuario' in session:
        fechaActual = request.form['fechaActual']
        valorSugerido = request.form['valorSugerido']
        estado = 'pendiente'
        idEmpleo = idEmpleo
        idEmpleado = idEmpleado
        
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        sql = 'insert into aplicaciones(FechaAplicacion, ValorSugerido, EstadoAplicacion ,FK_idEmpleo, FK_idUsuario) values (%s, %s, %s, %s, %s)'
        datos = (fechaActual, valorSugerido, estado, idEmpleo, idEmpleado)
        cursor.execute(sql, datos)
        cursor.close()
        cnx.commit()
        cnx.close()

        return redirect(url_for('home.home'))
    return "dsfsadfsaf"
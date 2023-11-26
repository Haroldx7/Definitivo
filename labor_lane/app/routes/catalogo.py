from flask import Blueprint, render_template, session, redirect, url_for
import mysql.connector
from app.db_config import db_config


catalogo_bp = Blueprint('catalogo', __name__)

@catalogo_bp.route('/catalogo') 
def catalogo(): 
    if 'usuario' in session:
        if session['usuario']['rol'] == 2:
            sesion = session['usuario']
            datosUser = ""
            cnx = mysql.connector.connect(**db_config)
            try:
                cursor = cnx.cursor()
                sql = "select * from ofertaempleo"
                cursor.execute(sql)
                datosUser = cursor.fetchall()
                cnx.commit()
                cnx.close()
                print(datosUser)
            except Exception as ex:
                print(ex)
            return render_template("catalogo.html", datos = datosUser, sesion=sesion)
        
    if 'usuario' not in session or session['usuario']['rol'] == 3:
        datosUser = ""
        cnx = mysql.connector.connect(**db_config)
        try:
            cursor = cnx.cursor()
            sql = "select * from usuario WHERE FK_IdRol = 2"
            cursor.execute(sql)
            datosUser = cursor.fetchall()
            cnx.commit()
            cnx.close()
            print(datosUser)
        except Exception as ex:
            print(ex)
        return render_template("catalogo.html", datos = datosUser, sesion=None)
    return render_template("catalogo.html")


@catalogo_bp.route('/contratar')
def contratar():
    if 'usuario' in session:

        if session['usuario']['rol'] == 3:
            return redirect(url_for('ofertaempleo.ofertaempleo'))
        else:
            return redirect(url_for('home.home'))
    return render_template('login.html')


@catalogo_bp.route('/catalogo-cliente')
def catalogocliente():

    return redirect(url_for('home.home'))

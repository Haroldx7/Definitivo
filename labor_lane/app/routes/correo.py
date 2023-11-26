from flask import Blueprint, redirect, render_template, session, url_for, flash
import mysql.connector
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import ssl
from app.db_config import db_config

correo_bp = Blueprint('correo', __name__)




@correo_bp.route('/contrato/<int:ido>/<string:id>/<int:ide>')
def contrato(ido,id,ide):
    
    
    cnx = mysql.connector.connect(**db_config) 
    cursor = cnx.cursor()

    sql = "SELECT EstadoAplicacion FROM aplicaciones where IdAplicaciones=%s"

    
    cursor.execute(sql, (ide,))
    empleados = cursor.fetchall()

    cnx.commit()

    print("este el id de las aplicaciones :", empleados)
    if empleados:
        estado_empleo = empleados[0][0]  # Acceder al primer resultado (primer fila, primer campo)

        if estado_empleo == "pendiente":

            mensaje=" Contrato enviado por correo"
            flash(mensaje)

            sql = "select CorreoUsuario from usuario where IdUsuario = %s"

            cursor.execute(sql, (ido,))

            empleados = cursor.fetchall()
            cnx.commit()

            print(empleados)

            email_sender = "laborlane.def@gmail.com"
            password = "eniq zlnc alti hhyy"
            email_reciver = empleados[0][0]

            subject = "Ejemplo Labor Lane"
            cuerpo_mensaje = f"""
            Hola,

            Un cliente {id} esta dispuesto a contratarte y para recordarte que.
            Este es un ejemplo de correo electrónico enviado desde Python.

            Saludos
            """

            em = EmailMessage()
            em["From"] = email_sender
            em["To"] = email_reciver
            em["Subject"] = subject
            em.set_content(cuerpo_mensaje)

            contexto = ssl.create_default_context()

            # Conexión al servidor SMTP de Gmail
            
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls(context=contexto)
                smtp.login(email_sender, password)
                smtp.send_message(em)

            sql = 'update aplicaciones set EstadoAplicacion = "admitida" where IdAplicaciones = %s'
            cursor.execute(sql, (ide,))
            cnx.commit()

            return redirect(url_for('perfilcliente.perfilcliente'))

    return redirect(url_for('home.home'))




@correo_bp.route('/rechazar/<int:ida>')
def rechazar(ida):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    sql = 'update aplicaciones set EstadoAplicacion = "rechazada" where IdAplicaciones = %s'
    cursor.execute(sql, (ida,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('perfilcliente.perfilcliente'))

@correo_bp.route('/finalizar/<int:idu>')
def finalizar(idu):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    sql = 'update aplicaciones set EstadoAplicacion = "finalizada" where IdAplicaciones = %s'
    print("dssssssssssssssssssssssssssssssssss",idu)
    cursor.execute(sql, (idu,))
    cnx.commit()
    cursor.close()
    cnx.close()

    return redirect(url_for('perfilcliente.perfilcliente'))


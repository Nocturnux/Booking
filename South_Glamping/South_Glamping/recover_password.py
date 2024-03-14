import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string

def generate_password():
    characters = string.ascii_letters + string.digits
    length = 10
    return ''.join(random.choice(characters) for i in range(length))

def send_email(addressee, password):
    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender = 'southglamping.sg@gmail.com'
    password_smtp = 'cwne kdqi pzpn xoln'

    # Crear el mensaje
    message = MIMEMultipart()
    message['From'] = sender #remitente
    message['To'] = addressee #destinatario
    message['Subject'] = 'Recuperación de contraseña'

    body = f'Tu nueva contraseña es: {password}'
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    # Iniciar sesión en el servidor SMTP
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender, password_smtp)

    # Enviar el correo electrónico
    server.send_message(message)

    # Cerrar la conexión
    server.quit()

# Función principal
def recover_password(email):
    destination_email= email
    new_password= generate_password()
    send_email(destination_email, new_password)

def recover_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        """ Cosultar el usuario por el correo  y cambiar la contraseña encriptada"""
        recover_password(email)
    return render (request, 'recover_password.html', {'email': email})

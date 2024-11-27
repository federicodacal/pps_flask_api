import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..services.config_service import ConfigService
from config import Config

class MailService:

    @staticmethod
    def send_confirmation_email(user_email, full_name, user_id):
        confirmation_link = f"{ConfigService.current_url}/users/confirm-email/{user_id}"

        subject = "Confirmación de email - AudioLibre"
        body = f"""
        {full_name}, te damos la bienvenida a AudioLibre.
        Por favor, haz click en el siguiente enlace para validar tu email:
        {confirmation_link}
        """

        try:
            smtp_server = Config.SMTP_SERVER
            smtp_port = Config.SMTP_PORT
            smtp_user = Config.SMTP_USER
            smtp_password = Config.SMTP_PASSWORD

            if not smtp_user or not smtp_password:
                return {"message":"SMTP_USER y SMTP_PASSWORD no están configurados correctamente"}, 500
            
            if not smtp_port or not smtp_server:
                return {"message":"SMTP_PORT y SMTP_SERVER no están configurados correctamente"}, 500

            mail_server = smtplib.SMTP(smtp_server, smtp_port)
            mail_server.starttls()

            mail_server.login(smtp_user, smtp_password)

            msg = MIMEMultipart()
            msg["From"] = smtp_user
            msg["To"] = user_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))
            mail_server.sendmail(smtp_user, user_email, msg.as_string())
            mail_server.quit()

            return {"message:":"Correo de confirmación enviado"}, 200

        except Exception as e:
            return {"message": f'Ocurrió un error al enviar el correo: {str(e)}', "error_type": "Unhandled Exception"}, 500
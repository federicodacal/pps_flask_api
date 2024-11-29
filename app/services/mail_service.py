import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..repositories.audio_repository import AudioRepository
from ..repositories.creator_repository import CreatorRepository
from ..services.config_service import ConfigService
from config import Config

class MailService:

    @staticmethod 
    def send_email(user_email, subject, body):
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

            return {"message:":"Correo enviado"}, 200

        except Exception as e:
            return {"message": f'Ocurrió un error al enviar el correo: {str(e)}', "error_type": "Unhandled Exception"}, 500

    @staticmethod
    def send_confirmation_email(user_email, full_name, user_id):
        confirmation_link = f"{ConfigService.current_url}/users/confirm-email/{user_id}"

        subject = "Confirmación de email - AudioLibre"
        body = f"""
        {full_name}, te damos la bienvenida a AudioLibre.
        Por favor, haz click en el siguiente enlace para validar tu email:
        {confirmation_link}

        AudioLibre
        """

        msg, status = MailService.send_email(user_email, subject, body)
        return msg, status

    @staticmethod
    def send_approval_email(user):
        link = f"{ConfigService.current_url}"
        subject = "Aprobación de usuario - AudioLibre"
        body = f"""
        {user["user_detail"]["full_name"]}, nos alegra comunicar que tu usuario se encuentra habilitado para usar AudioLibre.
        ¡Que lo disfrutes!
        {link}

        AudioLibre
        """

        msg, status = MailService.send_email(user["email"], subject, body)
        return msg, status
    
    @staticmethod
    def send_rejection_email(user):
        link = f"{ConfigService.current_url}"
        subject = "Rechazo de solicitud de usuario - AudioLibre"
        body = f"""
        {user["user_detail"]["full_name"]}, lamentamos comunicarte que tu usuario no cumple con las normas de aprobación de la plataforma.
        {link}

        AudioLibre
        """

        msg, status = MailService.send_email(user["email"], subject, body)
        return msg, status
    
    @staticmethod
    def send_debt_notice_email(user_email, full_name):
        link = f"{ConfigService.current_url}"
        subject = "Suscripción impaga - AudioLibre"
        body = f"""
        {full_name}, nos comunicamos para dar aviso que tu subscripción se encuentra impago.
        En caso de no renovar en 60 días su usuario se dará de baja y sus audios dejarán de estar disponibles en la plataforma.
        {link}

        AudioLibre
        """

        msg, status = MailService.send_email(user_email, subject, body)
        return msg, status
    
    @staticmethod
    def send_deactivation_email(user):
        link = f"{ConfigService.current_url}"
        subject = "Inhabilitación de creador - AudioLibre"
        body = f"""
        {user["user_detail"]["full_name"]}, lamentamos informarte que por superar el periódo límite de renovación por suscripción impaga sus facultades como 'Creador' han sido inhabilitadas.
        {link}

        AudioLibre
        """

        msg, status = MailService.send_email(user["email"], subject, body)
        return msg, status
    
    
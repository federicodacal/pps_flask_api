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
        confirmation_link = f"https://pps-nextjs-frontend.vercel.app/pages/mail/{user_id}"

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
        link = "https://pps-nextjs-frontend.vercel.app/"
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
        link = "https://pps-nextjs-frontend.vercel.app/"
        subject = "Rechazo de solicitud de usuario - AudioLibre"
        body = f"""
        {user["user_detail"]["full_name"]}, lamentamos comunicarte que tu usuario no cumple con las normas de aprobación de la plataforma.
        {link}

        AudioLibre
        """

        msg, status = MailService.send_email(user["email"], subject, body)
        return msg, status
    
    @staticmethod
    def send_debt_notice_email(user, days_overdue):
        link = "https://pps-nextjs-frontend.vercel.app/"
        subject = "Suscripción impaga - AudioLibre"
        body = f"""
        {user["user_detail"]["full_name"]}, nos comunicamos para dar aviso que tu subscripción se encuentra impaga, con {days_overdue} días desde el vencimiento. 
        En caso de no renovar en {60-days_overdue} días su usuario se dará de baja y sus audios dejarán de estar disponibles en la plataforma.
        {link}

        AudioLibre
        """

        msg, status = MailService.send_email(user["email"], subject, body)
        return msg, status
    
    @staticmethod
    def send_deactivation_email(user):
        link = "https://pps-nextjs-frontend.vercel.app/"
        subject = "Inhabilitación de creador - AudioLibre"
        body = f"""
        {user["user_detail"]["full_name"]}, lamentamos informarte que por superar el periódo límite de renovación por suscripción impaga sus facultades como 'Creador' han sido inhabilitadas.
        {link}

        AudioLibre
        """

        msg, status = MailService.send_email(user["email"], subject, body)
        return msg, status
    
    @staticmethod
    def send_purchase_email_to_buyer(buyer_email, purchase_details):
        link = "https://pps-nextjs-frontend.vercel.app/"
        subject = "Confirmación de tu compra - AudioLibre"
        body = "Gracias por tu compra en AudioLibre. Aquí están los detalles de tu compra:\n\n"

        for detail in purchase_details:
            body += f" - {detail['audio_name']}: ${detail['price']}\n"

        body += f"\nEsperamos que disfrutes tu compra.\n\nAudioLibre {link}"
        

        msg, status = MailService.send_email(buyer_email, subject, body)
        return msg, status
    
    @staticmethod
    def send_purchase_email_to_creators(creator_info):
        subject = "Notificación de venta de tus audios - AudioLibre"
        body = f"Hola,\n\nSe han vendido los siguientes audios asociados a tu cuenta:\n\n"

        for audio in creator_info["audios"]:
            body += f" - {audio['name']}: ${audio['price']}\n"

        body += "\nGracias por ser parte de AudioLibre.\n\nAudioLibre"

        msg, status = MailService.send_email(creator_info["email"], subject, body)
        return msg, status
    
    @staticmethod
    def send_audio_approval_email(user):
        link = "https://pps-nextjs-frontend.vercel.app/"
        subject = "Aprobación de audio - AudioLibre"
        body = f"""
        {user["user_detail"]["full_name"]}, nos alegra comunicar que tu audio {user["audio_name"]} se encuentra habilitado.
        {link}

        AudioLibre
        """

        msg, status = MailService.send_email(user["email"], subject, body)
        return msg, status
    
    @staticmethod
    def send_audio_rejection_email(user):
        link = "https://pps-nextjs-frontend.vercel.app/"
        subject = "Rechazo de solicitud de audio - AudioLibre"
        body = f"""
        {user["user_detail"]["full_name"]}, lamentamos comunicarte que tu audio {user["audio_name"]} no cumple con las normas de aprobación de la plataforma.
        {link}

        AudioLibre
        """

        msg, status = MailService.send_email(user["email"], subject, body)
        return msg, status
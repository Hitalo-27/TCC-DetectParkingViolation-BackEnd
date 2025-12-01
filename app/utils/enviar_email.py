import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

from sqlalchemy.orm import Session

from app.database import get_db
from app import models

EMAIL_REMETENTE = os.getenv("EMAIL")
SENHA_APP = os.getenv("SENHA_APP")


def enviar_email(
    destinatario: str,
    assunto: str,
    mensagem: str,
    user_id: int,
):
    # -------------------------------------------------
    # Criar sessão do BD manualmente (equivalente ao Depends)
    # -------------------------------------------------
    db: Session = next(get_db())

    try:
        # -------------------------------------------------
        # ENVIO DO EMAIL
        # -------------------------------------------------
        email_msg = EmailMessage()
        email_msg["From"] = EMAIL_REMETENTE
        email_msg["To"] = destinatario
        email_msg["Subject"] = assunto
        email_msg.set_content(mensagem, subtype='html')

          # Conectando ao servidor SMTP do Outlook
        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()  # Ativa TLS
            smtp.ehlo()
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            smtp.send_message(email_msg)

        # -------------------------------------------------
        # CRIAR NOTIFICAÇÃO
        # -------------------------------------------------
        if user_id:
            notificacao = models.Notification(
                mensagem=mensagem,
                data=datetime.now(),
                user_id=user_id
            )

            db.add(notificacao)
            db.commit()
            db.refresh(notificacao)

        return {
            "success": True,
            "notification": notificacao
        }

    except Exception as e:
        # desfaz alterações no banco
        db.rollback()

        return {
            "success": False,
            "error": str(e)
        }

    finally:
        # fechar sessão sempre
        db.close()
import email, smtplib, ssl
from providers import PROVIDERS

# used for MMS
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from os.path import basename
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

##### DECRYPTION
from encrypt import Encrypt, Decrypt

key = b'12345678909876543212345678909876'
iv = b'1234567890987654'
###########

def send_mms_via_email(
    number: str,
    message: str,
    file_path: str,
    mime_maintype: str,
    mime_subtype: str,
    provider: str,
    sender_credentials: tuple,
    subject: str = "sent using etext",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):

    sender_email, email_password = sender_credentials
    receiver_email = f'{number}@{PROVIDERS.get(provider).get("mms")}'

    email_message=MIMEMultipart()
    email_message["Subject"] = subject
    email_message["From"] = sender_email
    email_message["To"] = receiver_email

    email_message.attach(MIMEText(message, "plain"))

    with open(file_path, "rb") as attachment:
        part = MIMEBase(mime_maintype, mime_subtype)
        part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={basename(file_path)}",
        )

        email_message.attach(part)

    text = email_message.as_string()

    # with smtplib.SMTP_SSL(
    #     smtp_server, smtp_port, context=ssl.create_default_context()
    # ) as email:
    #     email.login(sender_email, email_password)
    #     email.sendmail(sender_email, receiver_email, text)
    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl._create_unverified_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, text)
        

def text(input):
    number = "6692923036"
    message = input
    provider = "Xfinity Mobile"

    sender_credentials = ("kwalwayssmile17@gmail.com", "qurn yyxr tfgh rqdv")

    # MMS
    #file_path = "/Users/kendalwin/eepasa_final/shrek.png"
    file_path = "shrek.png"

    mime_maintype = "image"
    mime_subtype = "png"

    send_mms_via_email(
        number,
        message,
        file_path,
        mime_maintype,
        mime_subtype,
        provider,
        sender_credentials,
    )

if __name__ == "__main__":
    main()

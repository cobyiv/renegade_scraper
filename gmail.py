import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import make_msgid


class GoogleMailClient:
    def __init__(self, email_params):
        # expect inputs as a dictionary
        self.sender_email = email_params['sender_email']
        self.recipient_email = email_params['recipient_email']
        self.password = email_params['password']

        # optional parameters
        self.in_reply_to = email_params.get('message_id')
        self.subject = email_params.get('subject')

        # this is the message body, optional
        self.content = email_params.get('content')

        # create a msg_id by default
        self.message_id = make_msgid()

        # build core message
        self.build_message


    @property
    def build_message(self):
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = ', '.join(self.recipient_email)
        message['Subject'] = self.subject
        message["Message-ID"] = self.message_id
        message["In-Reply-To"] = self.in_reply_to
        message["References"] = self.in_reply_to
        self.message = message

    def add_attachment(self, file_path, filename):
        with open(file_path, "r") as file:
            csv_contents = file.read()

        part = MIMEBase("text", "csv")
        part.set_payload(csv_contents)

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        self.message.attach(part)

    def send_email(self):
        session = smtplib.SMTP('smtp.gmail.com', 587)  # outlook: smtp.office365.com
        session.starttls()  # enable security
        session.login(self.sender_email, self.password)  # login with mail_id and password
        text = self.message.as_string()
        session.sendmail(self.sender_email, self.recipient_email, text)
        session.quit()
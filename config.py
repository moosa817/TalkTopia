from os import getenv
import os

# config Variables
template_dir = os.path.abspath('app/templates/')
static_dir = os.path.abspath('app/public/')
log_file = 'logs/debug.log'

# secrets
debug_mode = getenv("DEBUG", True)
auth = getenv("AUTH")

email_sender = getenv("EMAIL_SENDER")
mail_passwd = getenv("SMTP_PWD")
mail_email_reciever = getenv("EMAIL_RECIEVER")
mail_server = getenv("MAIL_SERVER")
mail_port = 587
mail_user = getenv("MAIL_USER")

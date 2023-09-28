from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'This is a secret, keep it safe.'

app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'lincolnstcafe@outlook.com'
app.config['MAIL_PASSWORD'] = '3WaKe3Up3'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

DATABASE = 'lincolnstcafe'

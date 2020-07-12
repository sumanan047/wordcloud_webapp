from flask import Flask


#===================================configs================================

app = Flask(__name__)
app.config['SECRET_KEY']= 'ixpay2002whatbqpedg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0    # sets the cache life


from wd_app import routes
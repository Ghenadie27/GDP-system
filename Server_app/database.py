from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ESP32.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class sensors(db.Model):
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True)
    denumire = db.Column(db.String(120), nullable=False)
    timp = db.Column(db.String(120), nullable=False)
    temperatura = db.Column(db.String(120), nullable=False)
    umiditatea = db.Column(db.String(120), nullable=False)

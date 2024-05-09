from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)

# Configs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Records.sqlite3"


# Connect flask app to sqlalchemy before doing anything
db = SQLAlchemy(app)


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(3))


class Classroom(db.Model):
    id = db.Column(db.String(3), primary_key=True)


class LoudnessData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
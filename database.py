from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

# Configs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Records.db"


# Code past this has been auto-generated by flask-sqlacodegen
# https://github.com/ksindi/flask-sqlacodegen
# GODBLESS GITHUB PROJECTS

db = SQLAlchemy()
db.init_app(app)


class AnemometerDatum(db.Model):
    __tablename__ = 'AnemometerData'

    ID = db.Column(db.Integer, primary_key=True)
    ClassroomID = db.Column(db.ForeignKey('Classrooms.ClassroomID'))
    AnemometerReading = db.Column(db.Float)
    DateRecorded = db.Column(db.DateTime)

    Classroom = db.relationship('Classroom', primaryjoin='AnemometerDatum.ClassroomID == Classroom.ClassroomID', backref='anemometer_data')


class Classroom(db.Model):
    __tablename__ = 'Classrooms'

    ClassroomID = db.Column(db.Text, primary_key=True)

    Teachers = db.relationship('Teacher', secondary='TeacherClassrooms', backref='classrooms')


class LoudnessData(db.Model):
    __tablename__ = 'LoudnessData'

    ID = db.Column(db.Integer, primary_key=True)
    ClassroomID = db.Column(db.ForeignKey('Classrooms.ClassroomID'))
    LoudnessReading = db.Column(db.Float)
    DateRecorded = db.Column(db.DateTime)

    Classroom = db.relationship('Classroom', primaryjoin='LoudnessData.ClassroomID == Classroom.ClassroomID', backref='loudness_data')


t_TeacherClassrooms = db.Table(
    'TeacherClassrooms',
    db.Column('TeacherID', db.ForeignKey('Teachers.ID')),
    db.Column('ClassroomID', db.ForeignKey('Classrooms.ClassroomID'))
)


class Teacher(db.Model):
    __tablename__ = 'Teachers'

    ID = db.Column(db.Integer, primary_key=True)
    TeacherName = db.Column(db.Text)
    TeacherCode = db.Column(db.Text)


class TemperatureHumidityDatum(db.Model):
    __tablename__ = 'TemperatureHumidityData'

    ID = db.Column(db.Integer, primary_key=True)
    ClassroomID = db.Column(db.ForeignKey('Classrooms.ClassroomID'))
    TemperatureReading = db.Column(db.Float)
    HumidityReading = db.Column(db.Float)
    DateRecorded = db.Column(db.DateTime)

    Classroom = db.relationship('Classroom', primaryjoin='TemperatureHumidityDatum.ClassroomID == Classroom.ClassroomID', backref='temperature_humidity_data')

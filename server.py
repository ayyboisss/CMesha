from database import app, AnemometerDatum, Classroom, LoudnessDatum, TemperatureHumidityDatum, Teacher, t_TeacherClassrooms
from flask import render_template

@app.route("/")
def home():
    return(render_template("main.html"))

if "__main__" == __name__:
    app.run(debug=False) 

from database import app, AnemometerDatum, Classroom, LoudnessDatum, TemperatureHumidityDatum, Teacher, t_TeacherClassrooms, db
from flask import render_template

@app.route("/")
def home():
    wind_speed = db.session.execute(db.select(AnemometerDatum))
    print(wind_speed)

    return(render_template("main.html"))

if "__main__" == __name__:
    app.run(debug=True) 

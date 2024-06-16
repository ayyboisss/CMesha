from database import app, Classroom, LoudnessData, TemperatureHumidityDatum, AnemometerDatum
from flask import render_template


@app.route("/")
def home():
    classrooms = Classroom.query.with_entities(
                    Classroom.ClassroomID).limit(6).all()
    return (render_template("pages/main.html", classrooms=classrooms))


@app.route("/classroom/<string:classroom_id>")
def analytics(classroom_id):
    # Queries
    loudness = LoudnessData.query.filter_by(
        ClassroomID=classroom_id).with_entities(
        LoudnessData.LoudnessReading).all()

    temperature = TemperatureHumidityDatum.query.filter_by(
        ClassroomID=classroom_id).with_entities(
        TemperatureHumidityDatum.TemperatureReading).all()

    humidity = TemperatureHumidityDatum.query.filter_by(
        ClassroomID=classroom_id).with_entities(
        TemperatureHumidityDatum.HumidityReading).all()

    wind_speed = AnemometerDatum.query.filter_by(
        ClassroomID=classroom_id).with_entities(
        AnemometerDatum.AnemometerReading).all()

    return (render_template("pages/analytics.html",
                            classroom=classroom_id, loudness=loudness,
                            temperature=temperature, humidity=humidity,
                            wind_speed=wind_speed))


@app.route("/staff")
def staff():
    return (render_template("pages/staff.html"))


@app.route("/about")
def about():
    return (render_template("pages/about.html"))


if "__main__" == __name__:
    app.run(debug=True)
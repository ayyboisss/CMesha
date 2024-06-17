from database import app, Classroom, LoudnessData, TemperatureHumidityDatum, AnemometerDatum
from flask import render_template


def kowalski_analyze(classroom_id=str):
    "Get all data relevent to the specific classroom"
    result = []
    result.append(classroom_id)

    # Loudness
    result.append(LoudnessData.query.filter_by(
        ClassroomID=classroom_id).with_entities(
        LoudnessData.LoudnessReading).all())

    # Temperature / Humidity
    result.append(TemperatureHumidityDatum.query.filter_by(
        ClassroomID=classroom_id).with_entities(
        TemperatureHumidityDatum.TemperatureReading).all())

    result.append(TemperatureHumidityDatum.query.filter_by(
        ClassroomID=classroom_id).with_entities(
        TemperatureHumidityDatum.HumidityReading).all())

    # Wind speed
    result.append(AnemometerDatum.query.filter_by(
        ClassroomID=classroom_id).with_entities(
        AnemometerDatum.AnemometerReading).all())

    return result


@app.route("/")
def home():
    classrooms = Classroom.query.with_entities(
                    Classroom.ClassroomID).limit(6).all()

    giga_list = []
    for i in classrooms:
        print(i[0])
        # Classroom ID, this is technically creating a table in python
        giga_list.append(i)

        # Yep, we're doing this again
        loudness = LoudnessData.query.filter_by(
            ClassroomID=i[0]).with_entities(
            LoudnessData.LoudnessReading).first()
        giga_list.append(loudness)

        temperature = TemperatureHumidityDatum.query.filter_by(
            ClassroomID=i[0]).with_entities(
            TemperatureHumidityDatum.TemperatureReading).first()
        giga_list.append(temperature)

        humidity = TemperatureHumidityDatum.query.filter_by(
            ClassroomID=i[0]).with_entities(
            TemperatureHumidityDatum.HumidityReading).first()
        giga_list.append(humidity)

        wind_speed = AnemometerDatum.query.filter_by(
            ClassroomID=i[0]).with_entities(
            AnemometerDatum.AnemometerReading).first()
        giga_list.append(wind_speed)

    print(giga_list)
    return (render_template("pages/main.html", giga_list=giga_list))


@app.route("/classroom/<string:classroom_id>")
def analytics(classroom_id):
    data = kowalski_analyze(classroom_id)
    loudness = data[1]
    temperature = data[2]
    humidity = data[3]
    wind_speed = data[4]

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

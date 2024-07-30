from database import app, Classroom, LoudnessData, TemperatureHumidityDatum, AnemometerDatum
from flask import render_template


def tuple_to_list(content, convert_date):
    "Turn a SQLite query tuple into a list"
    result = []
    if convert_date:
        for i in content:
            temp_list = []
            date = i[0].split('-')
            new_date = f"new Date({date[0]}, {date[1]}, {date[2]})"
            temp_list.append(new_date)
            temp_list.append(i[1])
            result.append(temp_list)
    else:
        for i in content:
            result.append([*i])

    print(result)
    return result


def kowalski_analyze(classroom_id=str):
    "Get all data relevent to the specific classroom"
    result = []
    result.append(classroom_id)

    # Loudness
    result.append(
        tuple_to_list(
            LoudnessData.query.filter_by(
                ClassroomID=classroom_id).with_entities(
                    LoudnessData.DateRecorded, LoudnessData.LoudnessReading).order_by(
                        LoudnessData.DateRecorded.asc()
                        ).all(), True)
    )

    # Temperature / Humidity
    result.append(
        tuple_to_list(
            TemperatureHumidityDatum.query.filter_by(

                ClassroomID=classroom_id).with_entities(
                    TemperatureHumidityDatum.DateRecorded, TemperatureHumidityDatum.TemperatureReading).order_by(
                        TemperatureHumidityDatum.DateRecorded.asc()
                    ).all(), True)
    )

    result.append(
        tuple_to_list(TemperatureHumidityDatum.query.filter_by(
                ClassroomID=classroom_id).with_entities(
                    TemperatureHumidityDatum.DateRecorded, TemperatureHumidityDatum.HumidityReading).order_by(
                        TemperatureHumidityDatum.DateRecorded.asc()
                    ).all(), True)
    )

    # Wind speed
    result.append(
        tuple_to_list(AnemometerDatum.query.filter_by(
                ClassroomID=classroom_id).with_entities(
                    AnemometerDatum.DateRecorded, AnemometerDatum.AnemometerReading).order_by(
                        AnemometerDatum.DateRecorded.asc()
                    ).all(), True)
    )

    return result


@app.route("/")
def home():

    # This entire thing creates a list of all the data each classroom has.
    classrooms = Classroom.query.with_entities(
                    Classroom.ClassroomID).limit(6).all()

    giga_list = []

    for i in classrooms:
        temp_list = []
        print(i[0])
        # Classroom ID, this is technically creating a table in python
        temp_list.append(i[0])

        # Yep, we're doing this again
        temperature = TemperatureHumidityDatum.query.filter_by(
            ClassroomID=i[0]).with_entities(
            TemperatureHumidityDatum.TemperatureReading).first()
        if not temperature:
            temperature = (False,)
        temp_list.append(temperature[0])

        humidity = TemperatureHumidityDatum.query.filter_by(
            ClassroomID=i[0]).with_entities(
            TemperatureHumidityDatum.HumidityReading).first()
        if not humidity:
            humidity = (False,)
        temp_list.append(humidity[0])

        loudness = LoudnessData.query.filter_by(
            ClassroomID=i[0]).with_entities(
            LoudnessData.LoudnessReading).first()
        if not loudness:
            loudness = (False,)
        temp_list.append(loudness[0])

        wind_speed = AnemometerDatum.query.filter_by(
            ClassroomID=i[0]).with_entities(
            AnemometerDatum.AnemometerReading).first()
        if not wind_speed:
            wind_speed = (False,)
        temp_list.append(wind_speed[0])

        giga_list.append(temp_list)

    print(giga_list)
    return (render_template("pages/main.html", giga_list=giga_list))


@app.route("/classroom/<string:classroom_id>")
def analytics(classroom_id):
    data = kowalski_analyze(classroom_id)
    loudness = data[1]
    temperature = data[2]
    humidity = data[3]
    ventilation = data[4]

    return (render_template("pages/analytics.html",
                            classroom=classroom_id, loudness=loudness,
                            temperature=temperature, humidity=humidity,
                            ventilation=ventilation))


@app.route("/staff")
def staff():
    return (render_template("pages/staff.html"))


@app.route("/about")
def about():
    return (render_template("pages/about.html"))


if "__main__" == __name__:
    app.run(debug=True)

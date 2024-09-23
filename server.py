from database import app, Classroom, LoudnessData, TemperatureHumidityDatum, AnemometerDatum, db
from flask import render_template
from werkzeug.exceptions import HTTPException 
from datetime import datetime as dt


def get_classrooms():
    with app.app_context():
        result = Classroom.query.with_entities(Classroom.ClassroomID).all()
    return result

def tuple_to_list(content=tuple, convert_date=bool):
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

    complete_list = []

    for i in classrooms:
        temp_list = []
        # Classroom ID, this is technically creating a table in python
        temp_list.append(i[0])

        # Data queries: variable shows what's being queried
        temperature = TemperatureHumidityDatum.query.filter_by(
            ClassroomID=i[0]).with_entities(
            TemperatureHumidityDatum.TemperatureReading).order_by(
                TemperatureHumidityDatum.DateRecorded).first()
        if not temperature:
            temperature = (False,)
        temp_list.append(temperature[0])

        humidity = TemperatureHumidityDatum.query.filter_by(
            ClassroomID=i[0]).with_entities(
            TemperatureHumidityDatum.HumidityReading).order_by(
                TemperatureHumidityDatum.DateRecorded).first()
        if not humidity:
            humidity = (False,)
        temp_list.append(humidity[0])

        loudness = LoudnessData.query.filter_by(
            ClassroomID=i[0]).with_entities(
            LoudnessData.LoudnessReading).order_by(
                LoudnessData.DateRecorded).first()
        if not loudness:
            loudness = (False,)
        temp_list.append(loudness[0])

        wind_speed = AnemometerDatum.query.filter_by(
            ClassroomID=i[0]).with_entities(
            AnemometerDatum.AnemometerReading).order_by(
                AnemometerDatum.DateRecorded).first()
        if not wind_speed:
            wind_speed = (False,)
        temp_list.append(wind_speed[0])

        # This is for appending the latest date by searching through the entire database
        # Selects the DateRecorded column in all relevant tables
        wind_speed_date = db.select(AnemometerDatum.DateRecorded.label("DateRecorded")).where(
                AnemometerDatum.ClassroomID == i[0])

        loudness_date = db.select(LoudnessData.DateRecorded.label("DateRecorded")).where(
                LoudnessData.ClassroomID == i[0])

        temp_humid_date = db.select(TemperatureHumidityDatum.DateRecorded.label("DateRecorded")).where(
                TemperatureHumidityDatum.ClassroomID == i[0])

        # The UNION_ALL query
        union_date = db.union(
                wind_speed_date,
                loudness_date,
                temp_humid_date
            ).order_by(db.text('DateRecorded'))

        # Fixes some select issues in SQLAlchemy
        combined_query = union_date.subquery()
        print(str(combined_query) + " Chhecking")
 
        union_result = db.select(combined_query).order_by(
                combined_query.c.DateRecorded.desc())

        # This converts the current format in the SQL database (YYYY-MM-DD)
        # into the time used in the website (MM-DD-YY)
        result = db.session.execute(union_result).fetchone()
        print(str(result) + " CHECKING")
        datetime_convert = dt.strptime(str(result[0]), "%Y-%m-%d")
        temp_list.append(datetime_convert.strftime("%m/%d/%Y"))

        complete_list.append(temp_list)
    return (render_template("pages/main.html", giga_list=complete_list))


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

# Universal error handler.
@app.errorhandler(HTTPException)
def error(error_code):
    print(error_code)
    default_response = "Something went wrong!"
    default_code = 0
    # Gets the error code from the werkzeug HTTPException.
    match int(str(error_code).split()[0]):
        case 404:
            response = "This page cannot be found"
            response_code = 404
        case _:
            response = default_response
            response_code = default_code
    return (render_template("pages/error.html", response=response, response_code=response_code))

# This is for listing the classrooms in the sidebar.
app.jinja_env.globals.update({
  'classrooms': get_classrooms()
})


if "__main__" == __name__:
    app.run(debug=True)

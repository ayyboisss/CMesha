from database import app, Classroom, LoudnessData, TemperatureHumidityDatum, AnemometerDatum, db
from database import Users as DB_Users # In hindsight, this could've been named something else
from flask import render_template, abort, request, redirect, url_for, flash
from werkzeug.exceptions import HTTPException
from datetime import datetime as dt
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_login import current_user as logged_in_user # Currently conflicts with some local variables
from werkzeug.security import check_password_hash, generate_password_hash
from user_forms import LoginForm, RegisterForm, LogoutForm


# Flask Add-ons
login_manager = LoginManager()
login_manager.init_app(app)
csrf = CSRFProtect(app)


class User(UserMixin):
    "This is for creating the user so flask_login actually works"
    def __init__(self, id, username, password):
        self.id = str(id)
        self.username = username
        self.password = password

    def is_active(self):
        return self.is_active()

    def is_anonymous():
        return False

    def is_authenticated():
        return True

    def is_logged_in():
        return True

    def get_id(self):
        return self.id

    def get_name(self):
        return self.username


def get_classrooms():
    "Get every ClassroomID in the Classroom table"
    class_list = []
    with app.app_context():
        result = Classroom.query.with_entities(Classroom.ClassroomID).all()
        for i in result:
            class_list.append(i[0])
    return class_list


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


def classroom_data(classroom_id=str):
    """
    Get all data relevent to the specific classroom.
    Returns a list with the order: 
    (Loudness, LoudnessDate), (Temp, TempDate),
    (Humidity, HumidityDate), (WindSpd, WindSpdDate).
    """
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


# Login Manager
# This is for loading the user properly into the website
@login_manager.user_loader
def user_loader(user_id):
    """For initializing the user so @login_required works.
    This also verifies if the user exists in the database."""
    query_user = DB_Users.query.filter_by(
                    ID=user_id).with_entities(
                        DB_Users.ID, DB_Users.User, DB_Users.UserPassword).first()
    if query_user:
        return User(int(query_user[0]), query_user[1], query_user[2])
    else:
        return None


@login_manager.unauthorized_handler
def kick_user():
    """Returns the anonymous user to the login page when they access
    any page that requires logging in. """
    return redirect(url_for('login'))


@app.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    "Logout page, only available for logged in users."
    logout_form = LogoutForm()
    if logout_form.validate_on_submit():
        if logout_form.user_logout.data == "True":
            print(logout_form.user_logout.data)
            logout_user()
            return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))
    return render_template("pages/logout.html", logout_form=logout_form)


# Routes
@app.route("/login", methods=['POST', 'GET'])
def login():
    "Login page for anonymous users"
    if logged_in_user.is_active:
        return redirect(url_for("home"))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        database_users = DB_Users.query.filter_by(
            User=username).with_entities(
                DB_Users.ID, DB_Users.UserPassword).first()
        if database_users:
            current_user = user_loader(database_users[0])
            if check_password_hash(database_users[1], password):
                login_user(current_user)
                return redirect(url_for('home'))
            else:
                flash("Wrong Password")
        else:
            flash("This user does not exist")
    return render_template("pages/login.html", login_form=login_form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    "Register page for anonymous users"
    if  logged_in_user.is_active:
        return redirect(url_for("home"))
    
    register_form = RegisterForm()
    invalid_input = False
    if register_form.validate_on_submit():
        # Checks if the data provided doesn't already exist
        username = register_form.username.data
        password = register_form.password.data
        password_repeat = register_form.password_repeat.data
        existing_users = DB_Users.query.filter_by(
                            User=username).with_entities(
                                DB_Users.User).first()

        # Whitespace check, just to avoid some goofy things
        if username[0].isspace():
            # I'm too lazy to implement a CSS way to wrap text
            # without changing parent size. So, enjoy this wacky method.
            message = """Provide a valid username without starting
with a whitespace."""
            invalid_input = True
        if password[0].isspace():
            message = """Provide a valid password without
starting with a whitespace."""
            invalid_input = True

        if not register_form.password.errors and not invalid_input:
            print(password)
            print(password_repeat)
            if existing_users:
                flash("This username has already been taken")
            else:
                # Finally add the user to the database.
                insert_query = DB_Users(User=username, UserPassword=generate_password_hash(password))
                db.session.add(insert_query)
                db.session.commit()
                flash("Registered! Continue to the login page.")
        else: # This is part where we show errors
            print(register_form.password.errors)
            if register_form.password.errors:
                flash("The passwords do not match")
            if invalid_input:
                flash(message)
    return render_template('pages/register.html', register_form=register_form)

@app.route("/")
def home():
    """Home page, returns a list of all the latest classrooms that have the latest data in the """
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

        # This is for appending the latest date by searching through the entire database.
        # Selects the DateRecorded column in all relevant tables.
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

        union_result = db.select(combined_query).order_by(
                combined_query.c.DateRecorded.desc())

        # This converts the current format in the SQL database (YYYY-MM-DD)
        # into the time used in the website (MM-DD-YY)
        result = db.session.execute(union_result).fetchone()
        datetime_convert = dt.strptime(str(result[0]), "%Y-%m-%d")
        temp_list.append(datetime_convert.strftime("%m/%d/%Y"))

        # Finally, the big list is complete.
        complete_list.append(temp_list)
    return (render_template("pages/main.html", giga_list=complete_list))


@app.route("/classroom/<string:classroom_id>")
def analytics(classroom_id):
    "Analytics page, these return data to be used by Google Charts API."
    if classroom_id not in get_classrooms():
        abort(404)
    data = classroom_data(classroom_id)
    loudness = data[1]
    temperature = data[2]
    humidity = data[3]
    ventilation = data[4]

    return (render_template("pages/analytics.html",
                            classroom=classroom_id, loudness=loudness,
                            temperature=temperature, humidity=humidity,
                            ventilation=ventilation))


@app.route("/about")
def about():
    "Currently has nothing, should contain information as to what the website is about."
    return (render_template("pages/about.html"))


@app.route("/posts", methods=['POST'])
@csrf.exempt
def receiving_data():
    """This is for the measuring device as the website will receive the data from it.
    Only accepts JSON file format. Returns a 200 if data has been successfully received."""
    data = request.get_json()
    if data:
        print(f"Temperature is {data['temperature']}")
        print(f"Humidity is {data['humidity']}")
        print(f"Air Quality is {data['air_quality']}")
        print(f"Loudnessis {data['loudness']}")
    return f"Signal received from sensor!", 200


# Universal error handler.
@app.errorhandler(HTTPException)
def error(error_code):
    "Universal error handler"
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

# Runs the website.
if "__main__" == __name__:
    # csrf.init_app(app)
    app.run(debug=True, host="0.0.0.0")

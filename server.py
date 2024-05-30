from database import app, Classroom, LoudnessData
from flask import render_template


@app.route("/")
def home():
    classrooms = Classroom.query.with_entities(
                    Classroom.ClassroomID).all()
    return (render_template("pages/main.html", classrooms=classrooms))


@app.route("/classroom/<string:classroom_id>")
def analytics(classroom_id):
    print(classroom_id)
    loudness = LoudnessData.query.filter_by(
        ClassroomID=classroom_id).with_entities(
        LoudnessData.ClassroomID, LoudnessData.LoudnessReading).all()
    return (render_template("pages/analytics.html", classroom=classroom_id, loudness=loudness))

@app.route("/staff")
def staff():
    return (render_template("pages/staff.html"))

@app.route("/about")
def about():
    return (render_template("pages/about.html"))


if "__main__" == __name__:
    app.run(debug=True) 

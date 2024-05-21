from database import app, Classroom, LoudnessData
from flask import render_template

@app.route("/")
def home():
    print(LoudnessData.query.with_entities(LoudnessData.LoudnessReading, LoudnessData.ClassroomID).all())
    return(render_template("main.html"))

if "__main__" == __name__:
    app.run(debug=True) 

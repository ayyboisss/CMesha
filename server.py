from database import app, Classroom, LoudnessData
from flask import render_template

@app.route("/")
def home():
    the_page = LoudnessData.query.paginate(per_page=6)
    for i in the_page.items:
        print(i.ClassroomID, i.LoudnessReading)
    return(render_template("main.html"))


@app.route("/classroom/<string:classroom_id>")
def analytics(classroom_id):
    print(classroom_id)
    return(render_template("pages/analytics.html", classroom = classroom_id))

@app.route("/about")
def about():
    return(render_template("pages/about.html"))
if "__main__" == __name__:
    app.run(debug=True) 

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        if request.form.get("action1") == "VALUE1":
            pass  # do something
        elif request.form.get("action2") == "VALUE2":
            pass  # do something else
        else:
            pass  # unknown
    elif request.method == "GET":
        return render_template("hello.html", form=form)

    return render_template("hello.html")

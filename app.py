from flask import Flask
from flask import render_template
from flask import request
from model import predict

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route("/form", methods=["POST", "GET"])
def form():
	if request.method == "POST":
		result = request.form
		flat = [[result["Metai"], result["Plotas"], result["Kambariu sk"], result["Aukstas"], result["Pastato tipas"], result["Renovacijos metai"]]]
		RentPrediction  = predict(flat)
		return render_template("form.html", RentPrediction=RentPrediction, Metai=result["Metai"], Plotas=result["Plotas"], KambariuSk = result["Kambariu sk"], Aukstas=result["Aukstas"],RenovacijosMetai= result["Renovacijos metai"])
	else:
		return render_template("form.html")


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        result = request.form
        flat = [[result["Metai"], result["Plotas"], result["Kambariu sk"], result["Aukstas"], result["Pastato tipas"], result["Renovacijos metai"]]]
        return str(predict(flat))
    else:
        return "No result"


if __name__ == "__main__":
    app.run(debug=True)

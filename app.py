from flask import Flask
from flask import render_template
from flask import request
import model
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("recomendations.csv", delimiter=";", index_col ="Adresas")
df = df[df["district"]=="pilaiteje"]
df = df[["rent_price", "Predicted_price", "district"]]
@app.route("/", methods=['GET', 'POST'])
def index():    
    if request.method == 'POST':
        website = request.form["website"]
        prediction = model.predictPrice(website)
        modelPrediction = int(prediction[0])
        price = int(prediction[1].replace(" €",""))
        return render_template("index.html", modelPrediction = modelPrediction, website = website, price = price, diff = price - modelPrediction, tables=[df.to_html(classes='table')], titles=df.columns.values)
    else:
        return render_template("index.html", modelPrediction = 0)

# @app.route("/model")
# def model():
#     return "Will post info about the models"
    
if __name__ == "__main__":
    app.run(debug=True)

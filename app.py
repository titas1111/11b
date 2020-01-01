from flask import Flask
from flask import render_template
from flask import request
import model

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():    
    if request.method == 'POST':
        website = request.form["website"]
        # prediction = int(model.predictPrice(website))
        prediction = model.predictPrice(website)
        modelPrediction = int(prediction[0])
        price = prediction[1]
        return render_template("index.html", modelPrediction = modelPrediction, website = website, price = price)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

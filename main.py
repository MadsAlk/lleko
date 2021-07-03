import json
from flask import Flask, render_template, request


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods = ['POST'])
def webhook():
    req = request.get_json(force=True)
    print(json.dumps(req, indent=4, sort_keys=True))
    print(req["queryResult"]["intent"]["displayName"])
    intent = req["queryResult"]["intent"]["displayName"]
    if intent == "LED":
        print(req["queryResult"]["outputContexts"][0]["parameters"]["status"])
        status = req["queryResult"]["outputContexts"][0]["parameters"]["status"]
        return {
            "fulfillmentText":status
        }



    return {
        "fulfillmentText":"healoo from the other side"
    }



# @app.route('/dest.html', methods = ['POST', 'GET'])
# def dest():
#     if request.method == 'POST':
#         data = request.form                             # capture data submitted to form
#
#         return render_template('home.html', tick = True, val =f"{valueInDollar} USD = {newValue:.2f} {toCurrency}")
#     else:
#         return """<html><head>method of form = GET</head></html>"""




if __name__ == '__main__':
    app.run(debug=True, port=4500)


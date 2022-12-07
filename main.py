from flask import Flask, render_template, request
import logging 
import sys
import requests

app = Flask(__name__)

LOGGER = logging.getLogger(__name__)

@app.route('/', methods=["GET"])

def hello_world():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=UA-251033747-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-251033747-1');
    </script>
    """
    return prefix_google + render_template("index.html")

@app.route('/logger', methods = ['GET', 'POST'])
def logger():

    global user_input

    print('This is a back end log!', file=sys.stderr)
    logging.info("Test logging")
    value = request.form.get("textbox_input")

    return render_template("logger.html",text=value) 


@app.route('/cookies', methods = ['GET', 'POST'])
def get_cookies():       
    req = requests.get("https://www.google.com/")

    return req.cookies.get_dict()

@app.route('/ganalytics', methods = ['GET', 'POST'])
def get_analytics():       
    req = requests.get("https://analytics.google.com/analytics/web/#/report-home/a164062586w272485488p243020933")
    return req.text

if __name__ == "__main__":
    app.run(debug=True)
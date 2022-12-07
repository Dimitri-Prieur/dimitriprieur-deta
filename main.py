from flask import Flask, render_template
import logging 
import sys

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

@app.route('/logger', methods=["GET"])
def hello_world2():
    print('This is a back end log!', file=sys.stderr)
    logging.info("Test logging")
    script = """
    <script> console.log("This is a front end log!") </script>"""
    return "This is a test" + render_template("logger.html") + script
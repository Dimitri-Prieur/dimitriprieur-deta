from flask import Flask, render_template, request
import logging 
import sys
import requests
import os
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'digitaltracesapi-6e7d1ecf06d4.json'
VIEW_ID = os.getenv("View_ID")

def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:pageviews'}],
          'dimensions': []
          #'dimensions': [{'name': 'ga:country'}]
        }]
      }
  ).execute()


def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print(header + ': ', dimension)

      for i, values in enumerate(dateRangeValues):
        print('Date range:', str(i))
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          visitors = value
  return str(visitors)


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
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    nb_visitor = print_response(response)
    logging.info("Test gdx")

    return prefix_google + render_template('index.html', visitors=str(nb_visitor))

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

    mail = os.getenv("Google_mail")
    password = os.getenv("Google_password")

    payload = {'inUserName': mail, 'inUserPass': password}
    # url = 'http://www.example.com'
    other_url = "https://analytics.google.com/analytics/web/#/report-home/a164062586w272485488p243020933"
    r = requests.post(other_url, data=payload)
    req = requests.get(other_url, cookies=r.cookies)
    return req.text

@app.route('/test', methods = ['GET', 'POST'])
def get_test():

    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    nb_visitor = print_response(response)
    print("test visitor", nb_visitor)
    logging.info("Test gdx")
    return render_template('index.html', visitors=str(nb_visitor))

if __name__ == "__main__":
    app.run(debug=True)
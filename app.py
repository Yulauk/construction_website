from flask import Flask, url_for, render_template, make_response
import datetime
import requests


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', year_on_site=year_on_site())


@app.route('/about')
def base():
    return render_template('about.html', year_on_site=year_on_site())


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', year_on_site=year_on_site())


@app.route('/services')
def services():
    return render_template('services.html', year_on_site=year_on_site())


@app.errorhandler(404)
def not_found(error):
    return render_template("error_pages/404.html", year_on_site=year_on_site()), 404


def year_on_site():
    date_now = datetime.datetime.now()
    return date_now.year


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

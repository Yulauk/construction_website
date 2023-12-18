from flask import Flask, url_for, render_template, make_response


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def base():
    return render_template('about.html')

@app.errorhandler(404)
def not_found(error):
    return render_template("error_pages/404.html"), 404

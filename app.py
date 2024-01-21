from flask import (Flask, url_for, render_template, g,
                   request, redirect, session, jsonify, flash)
from flask_babel import Babel
import datetime
import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
babel = Babel(app)

# Configuration for Babel
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['LANGUAGES'] = ['en', 'uk', 'ru', 'es']
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')


def get_locale():
    return session.get('language', app.config['BABEL_DEFAULT_LOCALE'])


babel.init_app(app, locale_selector=get_locale)


def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME')
        )
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/sql')
def indexsql():
    cursor = get_db().cursor()
    try:
        cursor.execute("SELECT * FROM free_consult;")
        records = cursor.fetchall()
        return render_template('sql.html', data=records)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

@app.route('/set_language/<language_code>', methods=['POST'])
def set_language(language_code):
    session['language'] = language_code
    return jsonify({'status': 'success'})


@app.route('/')
def index():
    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
    return render_template('index.html', year_on_site=year_on_site(), language=language)


@app.route('/about')
def base():
    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
    return render_template('about.html', year_on_site=year_on_site(), language=language)


@app.route('/portfolio')
def portfolio():
    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
    return render_template('portfolio.html', year_on_site=year_on_site(), language=language)


@app.route('/services')
def services():
    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
    return render_template('services.html', year_on_site=year_on_site(), language=language)


@app.route('/blog')
def blog():
    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
    return render_template('blog.html', year_on_site=year_on_site(), language=language)


# for portfolio projects
@app.route('/project')
def project():
    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
    return render_template('project.html', year_on_site=year_on_site(), language=language)

@app.route('/project/home-cinema-5-person')
def project_cinema_5():
    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
    return render_template('home-cinema-5-person.html', year_on_site=year_on_site(), language=language)


@app.route('/project/renovation-in-the-varshavsky-residential-complex-in-kyiv')
def project_varshavsky():
    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
    return render_template('portfolio_templates/renovation-in-the-varshavsky-residential-complex-in-kyiv.html', year_on_site=year_on_site(), language=language)


@app.route('/project/estonian-academy-of-music-and-theater-in-tallinn-estonia')
def project_estonian_academy():
    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
    return render_template('portfolio_templates/estonian-academy-of-music-and-theater-in-tallinn-estonia.html', year_on_site=year_on_site(), language=language)


# @app.route('/project/<project_name>/')
# def project_temp(project_name):
#     return render_template('project.html', project_name=project_name, year_on_site=year_on_site())

@app.errorhandler(404)
def not_found(error):
    return render_template("error_pages/404.html", year_on_site=year_on_site()), 404


def year_on_site():
    date_now = datetime.datetime.now()
    return date_now.year


# submit_free_consultation is responsible for saving
# the entered data in the Get a Free Consultation form
@app.route('/submit_free_consultation', methods=['POST'])
def submit_free_consultation():
    if request.method == 'POST':
        username = request.form.get('name')
        contact = request.form.get('contact')
        comment = request.form.get('comment')

        cursor = get_db().cursor()
        try:
            cursor.execute("INSERT INTO free_consult (name, contact, comment) VALUES (%s, %s, %s)",
                           (username, contact, comment))
            get_db().commit()
            # Add a flash message
            flash('Your application has been successfully sent', 'success')

            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            get_db().rollback()
            flash(f'Error submitting form: {err}', 'error')
            return redirect(url_for('index'))
        finally:
            cursor.close()


# сontact is responsible for saving
# the entered data in the Contact Us form
@app.route('/submit_contact_us', methods=['POST'])
def submit_contact_us():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')
        address = request.form.get('address')
        budget = request.form.get('budget')
        time = request.form.get('time')
        source = request.form.get('source')
        project_ = request.form.get('project')

        cursor = get_db().cursor()
        try:
            cursor.executemany(
                "INSERT INTO contact (name, surname, email, phone, city, state, zip, address, budget, time, source, project) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                [(name, surname, email, phone, city, state, zip_code, address, budget, time, source, project_)])

            get_db().commit()
            # Add a flash message
            flash('Your application has been successfully sent', 'success')
            return redirect(url_for('index'))
        except mysql.connector.IntegrityError as integrity_err:
            get_db().rollback()
            flash(f'Error submitting form: {integrity_err}', 'error')
            return redirect(url_for('index'))
        finally:
            cursor.close()


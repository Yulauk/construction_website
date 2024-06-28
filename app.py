from flask import (Flask, url_for, render_template, g,
                   request, redirect, session, flash, send_from_directory)
from flask_babel import Babel
import datetime
import mysql.connector
import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse




load_dotenv()
app = Flask(__name__)

# Set your desired URI prefix here (e.g., http://192.168.18.9:5000/ru)
# URI_PREFIX = os.getenv('URI_PREFIX', 'http://192.168.18.9:5000')
# app.config['BASE_URI'] = URI_PREFIX


babel = Babel(app)

# Configuration for Babel
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
app.config['LANGUAGES'] = ['en', 'uk', 'ru', 'et']
app.config['SERVER_NAME'] = os.getenv('SERVER_NAME')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['BABEL_USE_BRACE'] = True




# Add this line to set the language based on the URL
app.config['LANGUAGES_MAP'] = {'ru': 'ru', 'en': 'en', 'uk': 'uk', 'et': 'et'}


RECAPTCHA_SITE_KEY = os.getenv('MY_RECAPTCHA_SITE_KEY')
MY_RECAPTCHA_SECRET_KEY = os.getenv('MY_RECAPTCHA_SECRET_KEY')
VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'




def url_parse(url):
    return urlparse(url)


def get_locale():
    lang_code = session.get('language')
    return app.config['LANGUAGES_MAP'].get(lang_code) or app.config['BABEL_DEFAULT_LOCALE']


@app.route('/set_language/<language_code>', methods=['GET', 'POST'])
def set_language(language_code):
    if language_code in app.config['LANGUAGES']:
        session['language'] = language_code
        next_url = request.args.get('next') or url_parse(request.referrer).path

        if 'about' in next_url:
            return redirect(url_for('base', setting_language=language_code))
        elif 'portfolio' in next_url:
            return redirect(url_for('portfolio', setting_language=language_code))
        elif 'services' in next_url:
            return redirect(url_for('services', setting_language=language_code))
        elif 'blog' in next_url:
            return redirect(url_for('blog', setting_language=language_code))
        elif 'home-cinema-5-person' in next_url:
            return redirect(url_for('project_cinema_5', setting_language=language_code))
        elif 'renovation-in-the-varshavsky-residential-complex-in-kyiv' in next_url:
            return redirect(url_for('project_varshavsky', setting_language=language_code))
        elif 'estonian-academy-of-music-and-theater-in-tallinn-estonia' in next_url:
            return redirect(url_for('project_estonian_academy', setting_language=language_code))
        elif 'building-creation' in next_url:
            return redirect(url_for('articles_building', setting_language=language_code))
        elif 'apartment-renovation' in next_url:
            return redirect(url_for('articles_renovation', setting_language=language_code))
        elif 'electrical-installation-for-apartment-renovation' in next_url:
            return redirect(url_for('electrical_installation', setting_language=language_code))
        elif 'stages-of-plumbing-work' in next_url:
            return redirect(url_for('plumbing_work', setting_language=language_code))
        elif 'shower-without-tray' in next_url:
            return redirect(url_for('articles_shower', setting_language=language_code))
        else:
            return redirect(next_url or '/')
    else:
        # If language_code is None or invalid, redirect to the default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language
        return redirect(url_for('index', set_language=default_language))


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


@app.route('/', methods=['GET', 'POST'])
@app.route('/<set_language>/', methods=['GET', 'POST'])
def index(set_language=None):
    if request.method == 'POST':
        return set_language(request.form['language_code'])

    if set_language is not None and set_language in app.config['LANGUAGES']:
        session['language'] = set_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
    return render_template('index.html', year_on_site=year_on_site(), language=language,
                           RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)

@app.route('/<setting_language>/about/', methods=['GET', 'POST'])
@app.route('/<setting_language>/about', methods=['GET', 'POST'])
@app.route('/about/', methods=['GET', 'POST'])
@app.route('/about', methods=['GET', 'POST'])
def base(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('about.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e


# set_language/ru/
@app.route('/<setting_language>/portfolio', methods=['GET', 'POST'])
@app.route('/<setting_language>/portfolio/', methods=['GET', 'POST'])
@app.route('/portfolio/', methods=['GET', 'POST'])
@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('portfolio.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e


@app.route('/<setting_language>/services/')
@app.route('/<setting_language>/services')
@app.route('/services/')
@app.route('/services')
def services(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('services.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e


@app.route('/<setting_language>/blog/')
@app.route('/<setting_language>/blog')
@app.route('/blog/')
@app.route('/blog')
def blog(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('blog.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e



# for portfolio projects
@app.route('/<setting_language>/project/')
@app.route('/<setting_language>/project')
def project(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('project.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e


@app.route('/<setting_language>/portfolio/project/home-cinema-5-person/')
@app.route('/<setting_language>/portfolio/project/home-cinema-5-person')
@app.route('/project/portfolio/home-cinema-5-person/')
@app.route('/project/portfolio/home-cinema-5-person')
@app.route('/portfolio/home-cinema-5-person/')
@app.route('/portfolio/home-cinema-5-person')
def project_cinema_5(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('home-cinema-5-person.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e


@app.route('/<setting_language>/portfolio/project/renovation-in-the-varshavsky-residential-complex-in-kyiv/')
@app.route('/<setting_language>/portfolio/project/renovation-in-the-varshavsky-residential-complex-in-kyiv')
def project_varshavsky(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('portfolio_templates/renovation-in-the-varshavsky-residential'
                               '-complex-in-kyiv.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e



@app.route('/<setting_language>/portfolio/project/estonian-academy-of-music-and-theater-in-tallinn-estonia/')
@app.route('/<setting_language>/portfolio/project/estonian-academy-of-music-and-theater-in-tallinn-estonia')
def project_estonian_academy(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('portfolio_templates/estonian-academy-of-music'
                               '-and-theater-in-tallinn-estonia.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e



# @app.route('/project/<project_name>/')
# def project_temp(project_name):
#     return render_template('project.html', project_name=project_name, year_on_site=year_on_site())

# BLOG
@app.route('/<setting_language>/articles/')
@app.route('/<setting_language>/articles')
def articles(setting_language):
    session['language'] = setting_language
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
        return render_template('blog_templates/articles.html', year_on_site=year_on_site(),
                               language=language, RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    else:
        language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
        return render_template("error_pages/404.html", year_on_site=year_on_site(),
                               language=language), 404


@app.route('/<setting_language>/articles/shower-without-tray/')
@app.route('/<setting_language>/articles/shower-without-tray')
@app.route('/articles/shower-without-tray/')
@app.route('/articles/shower-without-tray')
def articles_shower(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('blog_templates/shower-without-tray.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e


@app.route('/<setting_language>/articles/building-creation/')
@app.route('/<setting_language>/articles/building-creation')
@app.route('/articles/building-creation/')
@app.route('/articles/building-creation')
def articles_building(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('blog_templates/building-creation.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e


@app.route('/<setting_language>/articles/apartment-renovation/')
@app.route('/<setting_language>/articles/apartment-renovation')
@app.route('/articles/apartment-renovation/')
@app.route('/articles/apartment-renovation')
def articles_renovation(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('blog_templates/apartment-renovation.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e


@app.route('/<setting_language>/articles/electrical-installation-for-apartment-renovation/')
@app.route('/<setting_language>/articles/electrical-installation-for-apartment-renovation')
@app.route('/articles/electrical-installation-for-apartment-renovation/')
@app.route('/articles/electrical-installation-for-apartment-renovation')
def electrical_installation(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('blog_templates/electrical-installation-for'
                               '-apartment-renovation.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e


# /Users/macbook/PycharmProjects/construction_site/templates/blog_templates/stages-of-plumbing-work.html
@app.route('/<setting_language>/articles/stages-of-plumbing-work/')
@app.route('/<setting_language>/articles/stages-of-plumbing-work')
@app.route('/articles/stages-of-plumbing-work/')
@app.route('/articles/stages-of-plumbing-work')
def plumbing_work(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('blog_templates/stages-of-plumbing-work.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e



@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml')

def year_on_site():
    date_now = datetime.datetime.now()
    return date_now.year


# submit_free_consultation is responsible for saving
# the entered data in the Get a Free Consultation form
@app.route('/submit_free_consultation', methods=['POST'])
def submit_free_consultation():
    if request.method == 'POST':
        secret_response = request.form['g-recaptcha-response']
        # print(request.form)
        verify_response = requests.post(url=f'{VERIFY_URL}?secret={MY_RECAPTCHA_SECRET_KEY}&response={secret_response}').json()
        # print(verify_response)

        if verify_response['success']:
            if verify_response['score'] > 0.4:
                username = request.form.get('name-free-consult')
                contact = request.form.get('contact-free-consult')
                comment = request.form.get('comment-free-consult')

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
            else:
                flash(f'Error submitting form: CAPTCHA score too low', 'error')
                return redirect(url_for('index'))
        else:
            flash(f'Error submitting form: capcha no verify', 'error')
            return redirect(url_for('index'))


def delete_selenium_tst_free_consult():
    cursor = get_db().cursor()
    cursor.execute('DELETE FROM free_consult WHERE name="Selenium_tst"')
    get_db().commit()
    cursor.close()

def delete_selenium_tst_contact():
    cursor = get_db().cursor()
    cursor.execute('DELETE FROM contact WHERE name="aa"')
    get_db().commit()
    cursor.close()



# сontact is responsible for saving
# the entered data in the Contact Us form
@app.route('/submit_contact_us', methods=['POST'])
def submit_contact_us():
    if request.method == 'POST':
        name = request.form.get('name-contact-us')
        surname = request.form.get('surname-contact-us')
        email = request.form.get('email-contact-us')
        phone = request.form.get('phone-contact-us')
        city = request.form.get('city-contact-us')
        state = request.form.get('state-contact-us')
        zip_code = request.form.get('zip-contact-us')
        address = request.form.get('address-contact-us')
        budget = request.form.get('budget-contact-us')
        time = request.form.get('time-contact-us')
        source = request.form.get('source-contact-us')
        project_ = request.form.get('project-contact-us')

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


@app.errorhandler(404)
def not_found(error):
    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
    return render_template("error_pages/404.html", year_on_site=year_on_site(), language=language), 404
from flask import (Flask, url_for, render_template, g,
                   request, redirect, session, flash, send_from_directory)
from flask_babel import Babel
import datetime
import mysql.connector
import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse

from blog_settings import get_blog_posts, get_total_posts, get_video_posts, get_news_posts


load_dotenv()
app = Flask(__name__)


babel = Babel(app)

# Configuration for Babel
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['LANGUAGES'] = ['en', 'uk', 'ru', 'et', 'es']
app.config['SERVER_NAME'] = os.getenv('SERVER_NAME')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['BABEL_USE_BRACE'] = True




# Add this line to set the language based on the URL
app.config['LANGUAGES_MAP'] = {'ru': 'ru', 'en': 'en', 'uk': 'uk', 'et': 'et', 'es': 'es'}


RECAPTCHA_SITE_KEY = os.getenv('MY_RECAPTCHA_SITE_KEY')
MY_RECAPTCHA_SECRET_KEY = os.getenv('MY_RECAPTCHA_SECRET_KEY')
VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'




def url_parse(url):
    return urlparse(url)


def get_locale():
    lang_code = session.get('language')
    return app.config['LANGUAGES_MAP'].get(lang_code) or app.config['BABEL_DEFAULT_LOCALE']


@app.route('/setting_language/<language_code>', methods=['GET', 'POST'])
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
        elif 'bathroom-in-amsterdam-march' in next_url:
            return redirect(url_for('bathroom_in_amsterdam_march', setting_language=language_code))
        elif 'bathroom-in-a-private-house-in-estonia' in next_url:
            return redirect(url_for('bathroom_in_a_private_house_in_estonia', setting_language=language_code))
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
        elif 'roofing-works' in next_url:
            return redirect(url_for('roofing_works', setting_language=language_code))
        elif 'recreation-complex-nova-estonia' in next_url:
            return redirect(url_for('recreation_complex_nova_estonia', setting_language=language_code))
        elif 'renovation-for-a-newly-built-apartment-in-kyiv' in next_url:
            return redirect(url_for('renovation_for_a_newly_built_apartment_in_kyiv', setting_language=language_code))
        else:
            return redirect(url_for('index', setting_language=language_code))
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
@app.route('/<setting_language>/', methods=['GET', 'POST'])
def index(setting_language=None):
    # Handle POST request to change language
    if request.method == 'POST':
        return setting_language(request.form['language_code'])

    # Handle language selection or default to the one in the session
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If no language is set, use the default language from the session or config
        if 'language' not in session:
            default_language = app.config['BABEL_DEFAULT_LOCALE']
            session['language'] = default_language

    # Get the current language from the session
    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    # Define the table based on the language
    table_map = {
        'en': 'blog_posts_en',
        'et': 'blog_posts_et',
        'uk': 'blog_posts_uk',
        'ru': 'blog_posts_ru'
    }
    table_name = table_map.get(language, 'blog_posts_en')  # Default to English table if language is not in the map
    # print('>>>',table_name,'<<<')
    # Get the two latest video posts for the selected language
    posts_video = get_video_posts(table_name)
    post_news = get_news_posts(table_name)

    # Render the 'index.html' template with the year, language, RECAPTCHA key, and video posts
    return render_template('index.html', year_on_site=year_on_site(), language=language,
                           RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY, posts_video=posts_video, post_news=post_news)




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
    # Якщо мова передана в URL, використовуємо її, інакше залишаємо попередню мову з сесії
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # Якщо мова не передана, перевіряємо, чи вже була встановлена мова в сесії
        if 'language' not in session:
            default_language = app.config['BABEL_DEFAULT_LOCALE']
            session['language'] = default_language

    # Отримуємо мову з сесії (вона повинна бути встановлена або з параметра URL, або залишатися незмінною)
    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    # Визначаємо назву таблиці на основі вибраної мови
    table_map = {
        'en': 'blog_posts_en',
        'et': 'blog_posts_et',
        'uk': 'blog_posts_uk',
        'ru': 'blog_posts_ru'
    }

    # Вибираємо таблицю відповідно до поточної мови
    table_name = table_map.get(language, 'blog_posts_en')  # За замовчуванням англійська таблиця

    # Визначаємо теги для поточної мови
    tags = {
        'en': {
            'renovation': 'Renovation',
            'construction': 'Construction',
            'plumbing': 'Plumbing',
            'electrical': 'Electrical',
            'landscaping': 'Landscaping',
            'videos':'Videos',
            'news': 'News',
        },
        'et': {
            'renovation': 'Renoveerimine',
            'construction': 'Ehitus',
            'plumbing': 'Torusüsteemid',
            'electrical': 'Elektritööd',
            'landscaping': 'Maastikukujundus',
            'videos' : 'Videod',
            'news': 'Uudised',
        },
        'uk': {
            'renovation': 'Реновація',
            'construction': 'Будівництво',
            'plumbing': 'Водопостачання',
            'electrical': 'Електрика',
            'landscaping': 'Ландшафтний дизайн',
            'videos': 'Відео',
            'news': 'Новини',
        },
        'ru': {
            'renovation': 'Ремонт',
            'construction': 'Строительство',
            'plumbing': 'Сантехника',
            'electrical': 'Электромонтаж',
            'landscaping': 'Благоустройство',
            'videos': 'Видео',
            'news': 'Новости',
        }
    }

    # Отримуємо теги для поточної мови
    current_tags = tags.get(language, tags['en'])

    page = request.args.get('page', 1, type=int)  # Отримуємо номер сторінки з параметрів URL
    per_page = 9  # Кількість постів на одній сторінці
    tag = request.args.get('tag')

    # Отримуємо пости і загальну кількість постів із відповідної таблиці
    posts = get_blog_posts(table_name, page, per_page, tag)
    total_posts = get_total_posts(table_name, tag)
    total_pages = (total_posts + per_page - 1) // per_page  # Округлення в більшу сторону

    # Генеруємо URL для наступної та попередньої сторінок
    next_url = url_for('blog', tag=tag, page=page + 1) if page < total_pages else None
    prev_url = url_for('blog', tag=tag, page=page - 1) if page > 1 else None

    # Video post for index.html
    # Get the two latest video posts
    posts_video = get_video_posts('blog_posts_en')

    return render_template('blog.html', year_on_site=year_on_site(), language=language,
                           RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY, posts=posts, tag=tag,
                           page=page, total_pages=total_pages, next_url=next_url, prev_url=prev_url,
                           current_tags=current_tags, posts_video=posts_video)


@app.route('/<setting_language>/roofing-works/')
@app.route('/<setting_language>/roofing-works')
@app.route('/roofing-works/')
@app.route('/roofing-works')
def roofing_works(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('/new_blog_pages/roofing-works.html', year_on_site=year_on_site(),
                               language=language,
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

# renovation-for-a-newly-built-apartment-in-kyiv.html
@app.route('/<setting_language>/portfolio/renovation-for-a-newly-built-apartment-in-kyiv/')
@app.route('/<setting_language>/portfolio/renovation-for-a-newly-built-apartment-in-kyiv')
@app.route('/portfolio/renovation-for-a-newly-built-apartment-in-kyiv/')
@app.route('/portfolio/renovation-for-a-newly-built-apartment-in-kyiv')
def renovation_for_a_newly_built_apartment_in_kyiv(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('renovation-for-a-newly-built-apartment-in-kyiv.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e


# recreation-complex-nova-estonia.html
@app.route('/<setting_language>/portfolio/recreation-complex-nova-estonia/')
@app.route('/<setting_language>/portfolio/recreation-complex-nova-estonia')
@app.route('/portfolio/recreation-complex-nova-estonia/')
@app.route('/portfolio/recreation-complex-nova-estonia')
def recreation_complex_nova_estonia(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('recreation-complex-nova-estonia.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e


# bathroom-in-amsterdam-march.html
@app.route('/<setting_language>/portfolio/bathroom-in-amsterdam-march/')
@app.route('/<setting_language>/portfolio/bathroom-in-amsterdam-march')
@app.route('/portfolio/bathroom-in-amsterdam-march/')
@app.route('/portfolio/bathroom-in-amsterdam-march')
def bathroom_in_amsterdam_march(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('bathroom-in-amsterdam-march.html', year_on_site=year_on_site(), language=language,
                               RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)
    except Exception as e:
        # Log or handle the 404 error here
        app.logger.error(f"404 Not Found: {request.url}")
        raise e


# bathroom-in-a-private-house-in-estonia.html
@app.route('/<setting_language>/portfolio/bathroom-in-a-private-house-in-estonia/')
@app.route('/<setting_language>/portfolio/bathroom-in-a-private-house-in-estonia')
@app.route('/portfolio/bathroom-in-a-private-house-in-estonian/')
@app.route('/portfolio/bathroom-in-a-private-house-in-estonia')
def bathroom_in_a_private_house_in_estonia(setting_language=None):
    if setting_language is not None and setting_language in app.config['LANGUAGES']:
        session['language'] = setting_language
    else:
        # If setting_language is None or invalid, set default language
        default_language = app.config['BABEL_DEFAULT_LOCALE']
        session['language'] = default_language

    language = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    try:
        return render_template('bathroom-in-a-private-house-in-estonia.html', year_on_site=year_on_site(), language=language,
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



@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    language = 'en'  # Определите язык по вашему выбору
    urls = [
        {'loc': url_for('index', _external=True, setting_language=language), 'changefreq': 'daily', 'priority': '1.0'},
        {'loc': url_for('about', _external=True, setting_language=language), 'changefreq': 'monthly', 'priority': '0.8'},
        {'loc': url_for('services', _external=True, setting_language=language), 'changefreq': 'monthly', 'priority': '0.9'},
        {'loc': url_for('blog', _external=True, setting_language=language), 'changefreq': 'weekly', 'priority': '0.7'},
    ]
    return render_template('sitemap.xml', urls=urls), {'Content-Type': 'application/xml'}

def year_on_site():
    date_now = datetime.datetime.now()
    return date_now.year


# submit_free_consultation is responsible for saving
# the entered data in the Get a Free Consultation form
@app.route('/submit_free_consultation', methods=['POST'])
def submit_free_consultation():
    # Получаем данные из формы
    username = request.form.get('name-free-consult')
    contact = request.form.get('contact')
    comment = request.form.get('comment')
    print(username, contact, comment)

    # Проверяем, что все данные переданы
    if username and contact and comment:
        cursor = get_db().cursor()
        try:
            cursor.execute("INSERT INTO free_consult (name, contact, comment) VALUES (%s, %s, %s)",
                           (username, contact, comment))
            get_db().commit()
            flash('Your application has been successfully sent', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            get_db().rollback()
            app.logger.error(f"Database Error: {e}")
            flash(f'Error: {e}', 'error')
            return redirect(url_for('index'))
        finally:
            cursor.close()
    else:
        flash('Please fill in all fields', 'error')
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
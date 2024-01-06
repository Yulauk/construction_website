from flask import Flask, url_for, render_template, g, request, redirect
import datetime
import mysql.connector
# MySQL Server Connection Details
# import config
import os
# from dotenv import load_dotenv



# load_dotenv()
app = Flask(__name__)


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
        cursor.execute("SELECT * FROM contact;")
        records = cursor.fetchall()
        return render_template('sql.html', data=records)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()


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
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            get_db().rollback()
            print(f"Error: {err}")
            return "Error submitting form: {}".format(err)
        finally:
            cursor.close()
            return redirect(request.referrer or url_for('index'))


#сontact is responsible for saving
# the entered data in the Contact Us form
@app.route('/submit_сontact_us', methods=['POST'])
def submit_contact_us():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')
        budget = request.form.get('budget')
        time = request.form.get('time')
        source = request.form.get('source')
        project = request.form.get('project')

        cursor = get_db().cursor()
        try:
            cursor.executemany(
                "INSERT INTO contact (name, surname, email, phone, city, state, zip, budget, time, source, project) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                [(name, surname, email, phone, city, state, zip_code, budget, time, source, project)])

            get_db().commit()
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            get_db().rollback()
            print(f"Error: {err}")
            return "Error submitting form: {}".format(err)
        finally:
            cursor.close()
            return redirect(request.referrer or url_for('index'))


from flask import *
import os
import pymysql
from icecream import ic  # Icecream for debugging, alternative to print()
from dotenv import dotenv_values, load_dotenv

# Load environment variables
load_dotenv()
config = dotenv_values(".env")

app = Flask(__name__)
app.secret_key = "ads24fb8fb82bfcf82bwdr54vdvfschsf3bf"  # Change this key to your own secret key
app.url_map.strict_slashes = False  # Disable strict slashes in URLs

# Database configuration using environment variables
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DB'),
        cursorclass=pymysql.cursors.DictCursor  # Converts results to a JSON-like dictionary
    )

# Index Page
@app.route("/")
def index():
    return render_template("Templates/welcome.html")

# Navigation Page
@app.route("/navigate")
def navigate():
    return render_template("Templates/navigate.html")

# Get all list of Countries
@app.route("/get_all_country_list", methods=["GET"])
def get_all_country_list():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            columns = 'name, Code'
            cursor.execute('SELECT ' + columns + ' FROM world.country ORDER BY name ASC')
            data = cursor.fetchall()
    finally:
        connection.close()

    response_data = {"error": False, "data": data}
    return jsonify(response_data)

# Get all list of States by country_code
@app.route("/get_state_list", methods=["GET"])
def get_state_list():
    country_code = request.args.get('country_code')

    if not country_code:
        return jsonify({"error": True, "msg": "parameter is missing, country_code is required"})

    query = "SELECT * FROM india.states ORDER BY name ASC"

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
    finally:
        connection.close()

    response_data = {"error": False, "data": data}
    return jsonify(response_data)

# Get all districts list by state_code or country_code
@app.route("/get_district_list", methods=["GET"])
def get_district_list():
    country_code = request.args.get('country_code')
    state_code = request.args.get('state_code')

    if not country_code and not state_code:
        return jsonify({"error": True, "msg": "parameter is missing, country_code or state_code is required"})

    query = "SELECT * FROM india.district"

    if state_code:
        query += f" WHERE state_code = '{state_code}'"
    query += " ORDER BY name ASC"

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
    finally:
        connection.close()

    response_data = {"error": False, "data": data}
    return jsonify(response_data)

# Get all city list by state_code or country_code
@app.route("/get_city_list", methods=["GET"])
def get_city_list():
    country_code = request.args.get('country_code')
    state_code = request.args.get('state_code')
    district_code = request.args.get('district_code')

    if not country_code and not state_code and not district_code:
        return jsonify({"error": True, "msg": "parameter is missing, country_code or state_code or district_code is required"})

    query = "SELECT * FROM india.city"

    if district_code:
        query += f" WHERE district_id = '{district_code}'"
    elif state_code:
        query += f" WHERE state_code = '{state_code}'"
    query += " ORDER BY name ASC"

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
    finally:
        connection.close()

    response_data = {"error": False, "data": data}
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)

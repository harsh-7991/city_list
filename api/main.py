from flask import *
import os
import sqlite3
from icecream import ic
# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()

app = Flask(__name__)
app.secret_key = "ads2cf82bwdr54vdvfschsf3bf"
app.url_map.strict_slashes = False

DATABASE = "/db/india.db"  # Path to the SQLite database file
# DATABASE = "D:/Projects/Z Project/World_api/api/india.db"  # Full path to the SQLite database file

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATABASE = os.path.join(BASE_DIR, "db/india.db")
# print(DATABASE)

# Database configuration
def get_db_connection():
    # print(DATABASE)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Rows can be accessed as dictionaries
    return conn

# Index Page
@app.route("/")
def index():
    return render_template("index.html")

# Navigation Page
@app.route("/navigate")
def navigate():
    return render_template("navigate.html")

# Get all list of Countries
@app.route("/get_all_country_list", methods=["GET"])
def get_all_country_list():
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        columns = 'name, country_code'
        cursor.execute(f'SELECT {columns} FROM country ORDER BY name ASC')


        data = [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


    response_data = {"error": False, "data": data}
    return jsonify(response_data)

# Get all list of States by country_code
@app.route("/get_state_list", methods=["GET"])
def get_state_list():
    country_code = request.args.get('country_code')

    if not country_code:
        return jsonify({"error": True, "msg": "parameter is missing, country_code is required"})

    # query = f"SELECT * FROM states WHERE country_code = '{country_code}' ORDER BY name ASC"
    query = f"SELECT * FROM states ORDER BY name ASC"


    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        data = [dict(row) for row in cursor.fetchall()]
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

    query = "SELECT * FROM district"

    if state_code:
        query += " WHERE state_code = ?"
        params = (state_code,)
    else:
        params = ()

    query += " ORDER BY name ASC"

    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        data = [dict(row) for row in cursor.fetchall()]
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

    query = "SELECT * FROM city"

    if district_code:
        query += " WHERE district_id = ?"
        params = (district_code,)
    elif state_code:
        query += " WHERE state_code = ?"
        params = (state_code,)
    else:
        params = ()

    query += " ORDER BY name ASC"

    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        data = [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()

    response_data = {"error": False, "data": data}
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)

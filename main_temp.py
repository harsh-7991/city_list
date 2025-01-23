from flask import *
import os
# import pymysql
from flask_mysqldb import MySQL	# <-- MySQL is used to connect with mysql database, it's alternative of sqlite3
from icecream import ic # <-- icecream as ic is used for printing data in console, its alternative of print() function, just use ic(data_variable_here)
from dotenv import dotenv_values, load_dotenv

# pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.secret_key = "ads24fb8fb82bfcf82bwdr54vdvfschsf3bf" # chaneg this key to your own secret key
app.url_map.strict_slashes = False # <-- This is used to remove trailing slash from the url, if you want to keep it then remove this line (--> not recommended to remove, removing this line will cause problem in get_district_list() and may be in other @app.route() <--).

load_dotenv()
config = dotenv_values(".env")


# # Database Configuration
# app.config['MYSQL_HOST'] = 'localhost'	# <-- change this to your mysql server host
# app.config['MYSQL_USER'] = 'root'	# <-- change this to your mysql server username
# app.config['MYSQL_PASSWORD'] = 'mysql_server_root'	# <-- change this to your mysql server password
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"	# <-- this will convert mysql results to json key value pair, so you can directly use it in jsonify() function

# Database / Schema names intialization
# app.config['MYSQL_DB'] = 'india' # no need to specify database we can specify databse in sql query as follow -> "SELECT * FROM database_name.table_name"



# MySQL configurations
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_CURSORCLASS'] = os.getenv('MYSQL_CURSORCLASS')





mysql_db = MySQL(app)	# <-- this will initialize mysql connection with the app, so we can use it in our functions (it's global variable)





# Converts Mysql results to json key value pair NOTE: no need to use this function if you mentioned following configuration above "app.config["MYSQL_CURSORCLASS"] = "DictCursor"
def fetch_key_value_pair(cursor):
    """
    Converts Mysql results to json key value pair\n
    NOTE: no need to use this function if you mentioned following configuration above\n
    "app.config["MYSQL_CURSORCLASS"] = "DictCursor"
    """
    # Fetching all rows from the table
    rows = cursor.fetchall()
    # Fetching column names
    column_names = [desc[0] for desc in cursor.description]
    # Formatting data as a list of dictionaries
    return [dict(zip(column_names, row)) for row in rows]




# Index Page have links examples please visit index page
@app.route("/")
def index():
    return render_template("index.html")


# Index Page have links examples please visit index page
@app.route("/navigate")
def navigate():
    return render_template("navigate.html")





# Get all list of Countries
@app.route("/get_all_country_list", methods=["GET"])
def get_all_country_list():

    cursor = mysql_db.connection.cursor()
    columns = 'name, Code'
    cursor.execute('SELECT '+columns+' FROM world.country ORDER BY name ASC')
    data = cursor.fetchall()
    # data = fetch_key_value_pair(cursor)
    cursor.close()

    response_data = {"error": False,
                     "data": data}

    return jsonify(response_data)




# Get all list of States by country_code
@app.route("/get_state_list", methods=["GET"])
def get_state_list():


	cc = request.args.get('country_code')
	# print(cc)

	query =""


	# india specific only
	if cc != None:
		query = "SELECT * FROM india.states ORDER BY name ASC"

	elif cc == None:
		response_data = {"error": True,
						"msg": "parameter is missing, country_code is required"}

		return jsonify(response_data)

	else:
		query = "SELECT * FROM india.states ORDER BY name ASC"


	cursor = mysql_db.connection.cursor()
	cursor.execute(query)
	data = cursor.fetchall()
	# data = fetch_key_value_pair(cursor)
	cursor.close()

	response_data = {"error": False,
						"data": data}

	return jsonify(response_data)





# Get all districts list by state_code or country_code
@app.route("/get_district_list", methods=["GET"])
def get_district_list():

	cc = request.args.get('country_code')
	sc = request.args.get('state_code')

	query =""

	# india specific only
	if cc != None and sc == None:
		query = "SELECT * FROM india.district ORDER BY name ASC"

	elif sc != None and cc == None:
		query = "SELECT * FROM india.district WHERE state_code = '" + sc + "' ORDER BY name ASC"

	elif sc != None and cc != None:
		query = "SELECT * FROM india.district WHERE state_code = '" + sc + "' ORDER BY name ASC"

	elif sc == None and cc == None:
		response_data = {"error": True,
						"msg": "parameter is missing, country_code or state_code is required"}

		return jsonify(response_data)

	else:
		query = "SELECT * FROM india.district ORDER BY name ASC"


	# print(query)

	cursor = mysql_db.connection.cursor()
	cursor.execute(query)

	# cursor.execute('SELECT * FROM india.district WHERE state_code = %s', (state_code,))
	data = cursor.fetchall()
	# data = fetch_key_value_pair(cursor)
	cursor.close()

	response_data = {"error": False,
					"data": data}

	return jsonify(response_data)



# Get all city list by state_code or country_code
@app.route("/get_city_list", methods=["GET"])
def get_city_list():

	cc = request.args.get('country_code')
	sc = request.args.get('state_code')
	dc = request.args.get('district_code')


	query =""

	# india specific only
	if sc == None and cc != None and dc == None:	# only country code is provided
		query = "SELECT * FROM india.city ORDER BY name ASC"

	elif sc != None and cc == None and dc == None:	# only state code is provided
		query = "SELECT * FROM india.city WHERE state_code = '" + sc + "' ORDER BY name ASC"

	elif sc == None and cc == None and dc != None:	# only district code is provided
		query = "SELECT * FROM india.city WHERE district_id = '" + dc + "' ORDER BY name ASC"

	elif sc != None and cc != None and dc == None:	# country and state code is provided
		query = "SELECT * FROM india.city WHERE state_code = '" + sc + "' ORDER BY name ASC"

	elif sc == None and cc != None and dc != None:	# country and district code is provided
		query = "SELECT * FROM india.city WHERE district_id = '" + dc + "' ORDER BY name ASC"

	elif sc != None and cc == None and dc != None:	# state and district code is provided
		query = "SELECT * FROM india.city WHERE district_id = '" + dc + "' ORDER BY name ASC"

	elif sc != None and cc != None and dc != None:	# all codes are provided
		query = "SELECT * FROM india.city WHERE district_id = '" + dc + "' ORDER BY name ASC"

	elif sc == None and cc == None and dc == None:	# no code is provided
		response_data = {
							"error": True,
							"msg": "parameter is missing, country_code or state_code or district_code is required",
						}
		return jsonify(response_data)

	else:
		query = "SELECT * FROM india.city  ORDER BY name ASC"

	# print(query)


	cursor = mysql_db.connection.cursor()
	cursor.execute(query)

    # cursor.execute('SELECT * FROM india.city WHERE state_code = %s', (state_code,))
	data = cursor.fetchall()
	# data = fetch_key_value_pair(cursor)
	cursor.close()

	response_data = {"error": False,
						"data": data}

	return jsonify(response_data)







if __name__ == "__main__":
    # app.debug = True
    # app.run()
    # app.run(host='0.0.0.0', port=4440, debug=True)
    app.run(debug=True)


	# host = '0.0.0.0 -> This will make your server publically accessible (on local network like WiFi, LAN, etc)
	# port = 4440 -> this will run your server on port 4440
	# debug = True -> this will enable debug mode, so you can see errors and logs in your terminal





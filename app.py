from flask import Flask, render_template, request, redirect, flash
from flask import jsonify
import oracledb
 
app = Flask(__name__)
 
d = r"C:\oracle\instantclient_21_12"
oracledb.init_oracle_client(lib_dir=d)
print(oracledb.clientversion())
 
def get_db_connection():
    dsn_t = oracledb.makedsn('navydb.artg.arizona.edu', 1521, 'ORCL')
    connection = oracledb.connect(user="mis531groupS1H", password="A4.PRp@:r5HFA/X", dsn=dsn_t, disable_oob=True)
    return connection

   
@app.route('/')
def index():
    print('Works')
    return render_template('index.html', loginStatus = False)

@app.route('/login')
def indloginex():
    print('Works')
    return render_template('login.html')
 
@app.route('/loginAuth', methods=['POST'])
def loginAuth():
    connection = get_db_connection()
    userID = request.form['userID']
    password = request.form['password']

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM AUTHENTICATION where AUTHID = :userID and PASSWORD = :password", userID = userID, password = password)
        authDetails = cursor.fetchall()
        # return jsonify(authDetails)
    finally:
        # Close the cursor and connection in a finally block
        cursor.close()
        connection.close()

    if len(authDetails) > 0:
        return render_template('index.html', loginStatus = True)

    return render_template('login.html', alert = 'Invalid Credentials')

@app.route('/scenarios')
def scenarios():
    return render_template('scenario.html')

       
@app.route('/frontend', methods=['GET'])
def get_clients():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM frontend")
        clients = cursor.fetchall()
        return jsonify(clients)
    finally:
        # Close the cursor and connection in a finally block
        cursor.close()
        connection.close()
 
if __name__ == '__main__':
    app.run(debug=True)
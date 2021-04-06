from flask import Flask, jsonify, abort, request
import mysql.connector as mysql


app = Flask(__name__)
print('Server started')

@app.route('/flask_app/')
def index():
    return "Hello, World from flask server!"

@app.route('/jokes/get_rand_joke', methods=['GET'])
def get():
    cnx = mysql.connect(host = "db", user = "root", passwd = "root", db = "db")
    cursor = cnx.cursor(prepared=True)
    query = 'select title from joke order by rand() limit 1;'
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return jsonify(result)

@app.route('/jokes/get_all', methods=['GET'])
def get_all():
    cnx = mysql.connect(host = "db", user = "root", passwd = "root", db = "db")
    cursor = cnx.cursor(prepared=True)
    query = 'select * from joke;'
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    return jsonify(result)

@app.route('/jokes/', methods=['POST'])
def post():
    joke = request.json
    print(joke)
    cnx = mysql.connect(host = "db", user = "root", passwd = "root", db = "db")
    cursor = cnx.cursor(prepared=True)
    create_query = 'create table if not exists joke(id int NOT NULL AUTO_INCREMENT, title VARCHAR(500), PRIMARY KEY (id));'
    joke_query = 'insert into joke (title) values(%s);'
    cursor.execute(create_query)
    cursor.execute(joke_query,(joke,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify("Succesfully saved joke: " + joke)


if __name__ == '__main__':
    app.run(debug=True)
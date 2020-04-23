import os

from flask import Flask, g, render_template, url_for
import mysql.connector

config = {
    "database": {
        "user": "user",
        "password": os.environ.get("MYSQL_PASSWORD"),
        "host": "db",
        "database": "science",
    },
}

app = Flask(__name__)

@app.before_first_request
def before_first_request():
    connection = create_connection(**config["database"])
    try:
        cursor = connection.cursor()
        cursor.execute("create table data (name varchar(20) not null, filename varchar(24) not null)")
        cursor.execute("insert into data (name, filename) values ('RMJ133520.1+410004.1', 'rmj133520.1+410004.1.png')")
        cursor.execute("insert into data (name, filename) values ('RMJ094951.8+170710.6', 'rmj094951.8+170710.6.png')")
        cursor.execute("insert into data (name, filename) values ('RMJ111514.8+531954.6', 'rmj111514.8+531954.6.png')")
        cursor.execute("insert into data (name, filename) values ('RMJ222842.7+083924.4', 'rmj222842.7+083924.4.png')")
        cursor.execute("insert into data (name, filename) values ('RMJ090912.2+105824.9', 'rmj090912.2+105824.9.png')")
        cursor.execute("insert into data (name, filename) values ('RMJ015949.3-084958.9', 'rmj015949.3-084958.9.png')")
        cursor.execute("insert into data (name, filename) values ('RMJ110608.5+333339.7', 'rmj110608.5+333339.7.png')")
        cursor.execute("insert into data (name, filename) values ('RMJ221145.9-034944.5', 'rmj221145.9-034944.5.png')")
        cursor.execute("insert into data (name, filename) values ('RMJ012542.3-063442.3', 'rmj012542.3-063442.3.png')")
        cursor.execute("insert into data (name, filename) values ('RMJ121218.5+273255.1', 'rmj121218.5+273255.1.png')")
        connection.commit()
    except:
        pass
    else:
        cursor.close()
    connection.close()

@app.before_request
def before_request():
    g.connection = create_connection(**config["database"])
    g.cursor = g.connection.cursor()

@app.after_request
def after_request(response):
    g.cursor.close()
    g.connection.close()
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/clusters/")
@app.route("/clusters/<name>")
def clusters(name=None):
    g.cursor.execute("select name, filename from data")
    results = [dict(name=name, filename=filename) for (name, filename) in g.cursor]
    if name:
        try:
            result = next(r for r in results if r["name"] == name)
        except StopIteration:
            return render_template("error.html")
        else:
            return render_template("cluster_by_name.html", **result)
    else:
        banner_message = os.environ.get("BANNER_MESSAGE", "Generic Banner Message")
        return render_template("cluster_list.html",
                banner_message=banner_message, clusters=results)

def create_connection(host=None, user=None, password=None, database=None):
    return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database)

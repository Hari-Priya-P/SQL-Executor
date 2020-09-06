from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import psycopg2


app = Flask(__name__,template_folder="Templates")
app.secret_key = 'many random bytes'


#MySQL Config

app.config['MYSQL_HOST'] = 'instacart1.cwoddzeg20lc.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'awsuser123'
app.config['MYSQL_DB'] = 'Instacart'
mysql = MySQL(app)

#PostgreSQL Config
psql = psycopg2.connect(dbname="dev", host="redshift-cluster-1.cykw6wpmjgki.us-east-2.redshift.amazonaws.com",
                        port=5439, user="awsuser", password="Awsuser123")


@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/query', methods = ['GET'])
def query():
    if request.method == "GET":
        which_server = request.args["server"]
        query = request.args['query']
        try:
            if which_server == "rds" :
                cur = mysql.connection.cursor()
            elif which_server == "redshift":
                cur = psql.cursor()
            cur.execute(query)
            data = cur.fetchall()
            mysql.connection.commit()
            tables = []
            for a in cur.description :
                tables.append(a[0])
            return render_template('index.html', data=data, messages=True, tables=tables)
        except Exception as e :
            flash(str(e))
            return render_template("index.html")


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80, debug = True)



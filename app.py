from flask import Flask, render_template
import mysql.connector


app = Flask(__name__, template_folder='templates')

mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '1234',
        database = 'mysql'
    )

@app.route('/details', methods=['GET'])
def api_details():
        cursor = mydb.cursor()
        cursor.execute('Select Source, title, PublishedDate, unique_id from test1')
        data = cursor.fetchall()
        return render_template('display.html', data = data)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True, port = 5000)


## we have to use database data to display the records 
## as using one after another times api calling is expensive as 
## it can exhaust your limit of using.
## use mysql code to display data
## then make a dropdown for different data and a fetch button
## that fetches data from database 
## any format mein show kr skte ho 
## can tabular, or any.

## one thing to remember to add filter options like
## 1. by 1 day
## 2. by that date
## or something like that. so at last pls maintain option for that.
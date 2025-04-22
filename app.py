from flask import Flask, render_template, request
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
        
        filter_type = request.args.get('filter')
        filter_value = request.args.get('value')

        cursor = mydb.cursor()
        query = 'Select Source, title, PublishedDate, unique_id from test1'
        values = []

        if filter_type  and filter_value:
              if filter_type == 'data':
                    query += 'Where PublishedDate = %s'
                    values.apped(filter.value)
              elif filter_type == 'source':
                    query += 'Where Source = %s'
                    values.append(filter_value)
        
        cursor.execute(query, tuple(values))
        data = cursor.fetchall()
        return render_template('display.html', data = data, selected_filter = filter_type, filter_value = filter_value)




if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True, port = 5000)


## one thing to remember to add filter options like
## 1. by 1 day
## 2. by that date
## or something like that. 
# so at last pls maintain option for that.
# render_template('display.html', data = data)
from flask import Flask, render_template, request
import mysql.connector


app = Flask(__name__, template_folder='templates')

mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '1234',
        database = 'mysql'
    )

def Filter_by_date(filter_value):
      cursor = mydb.cursor()
      query = 'Select Source, title, PublishedDate, unique_id from test1 WHERE PublishedDate = %s'
      cursor.execute(query, (filter_value,))
      return cursor.fetchall()

def filter_by_source(filter_value):
      cursor = mydb.cursor()
      query = 'Select Source, title, PublishedDate, unique_id from test1 WHERE Source = %s'
      cursor.execute(query, (filter_value, ))
      return cursor.fetchall()

@app.route('/details', methods=['GET', 'POST'])
def api_details():
        
        filter_type = request.form.get('filter') if request.method == 'POST' else request.args.get('filter')
        filter_value = request.form.get('value') if request.method == 'POST' else request.args.get('value')

        cursor = mydb.cursor()
        query = 'Select Source, title, PublishedDate, unique_id from test1'
        values = []

        if filter_type and filter_value:
                    if filter_type == 'data':
                            query += 'WHERE PublishedDate = %s'
                            values.append(filter_value)
                    elif filter_type == 'source':
                        query += 'WHERE Source = %s'
                        values.append(filter_value)
                    else:
                        return "Invalid filter type", 400
        
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
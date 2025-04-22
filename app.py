from flask import Flask, render_template, request
import mysql.connector


app = Flask(__name__, template_folder='templates')

mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '1234',
        database = 'mysql'
    )

def filter_by_date(filter_value):
      cursor = mydb.cursor()
      query = 'Select Source, title, PublishedDate, unique_id from test1 WHERE PublishedDate = %s'
      cursor.execute(query, (filter_value,))
      data = cursor.fetchall()
      print('Data fetched by date filter: ', data)
      return data

def filter_by_source(filter_value):
      cursor = mydb.cursor()
      query = 'Select Source, title, PublishedDate, unique_id from test1 WHERE Source = %s'
      cursor.execute(query, (filter_value, ))
      data = cursor.fetchall()
      print('Data fetched by source filter: ', data)
      return data

@app.route('/details', methods=['GET', 'POST'])
def api_details():
     filter_type = None
     filter_value = None
     data = []

     if request.method == 'POST':
          filter_type = request.form.get('filter')
          filter_value = request.form.get('value')

         # print(f'Filter Type: {filter_type}, Filter value: {filter_value}')

     if filter_type == 'date' and filter_value:
          data = filter_by_date(filter_value)

     elif filter_type == 'source' and filter_value:
          data = filter_by_source(filter_value)

     elif not filter_type or not filter_value:
          cursor = mydb.cursor()
          cursor.execute('SELECT Source, title, PublishedDate, unique_id from test1')
          data = cursor.fetchall()
     else:
          return "Invalid filter type", 400
     
     if not data:
          print('No data returned for the filter criteria.')
        
     return render_template('display.html', data=data, selected_filter=filter_type,filter_value=filter_value)


if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True, port = 5000)


## one thing to remember to add filter options like
## 1. by 1 day
## 2. by that date
## or something like that. 
# so at last pls maintain option for that.
# render_template('display.html', data = data)


#note: try to implement 2 functions like fetch() and display()
# fetch fetches the data from data like the one you did.
# and display is what you are doing right now. i.e just showing or displaying.
# in fetch() you can show that whether is fetching the data or not. for only one time.
# one more thing while using fetching function it should display the latestly added data or than 
# the ones which you added earlier. so this is the difference you've to keep in mind.
# display is like showing the whole database entries while fetch will only show me the latest one added.

# then lastly add a filter options 
# 1. by keywords => it should fetches some data according to that. and same should apply for all filter options.
# 2. by date
# 3. by timestamp
# 4. by source if required.
from flask import Flask, render_template, request
import mysql.connector
import requests
from newsapi import NewsApiClient



app = Flask(__name__, template_folder='templates')


mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '1234',
        database = 'mysql'
    )
mycursor = mydb.cursor()

def unique_id_exist(unique_id):   # it is used to test so no duplication is there
     try:
          mycursor.execute('select 1 from test1 WHERE unique_id = %s LIMIT 1', (unique_id,))
          return mycursor.fetchone() is not None
     except mysql.connector.Error as err:
          print(f'Error checking unique ID existence: {err}')
          return False

@app.route('/details', methods=['GET','POST'])

def home():
     inserted_data = []
     message = None
     latest_records = []


     if request.method == 'POST' and 'fetch_data' in request.form:
          try:
               def nyt_api():
                    requestUrl = "https://api.nytimes.com/svc/news/v3/content/all/'business'.json?limit=20&api-key=NIYJ7DwbZDKjtgBI4xKGUPGim572tRKi"
                    response = requests.get(requestUrl)
                    return response.json()

               a1 = nyt_api()
               for x in range(2,6):
                    first_var = a1['results'][x]
                    title = first_var['title']
                    source = first_var['source']
                    PublishedDate = first_var['published_date']
                    unique_id = first_var['url']

                    if not unique_id_exist(unique_id):
                         sql = "INSERT INTO test1(source, title, PublishedDate, unique_id) VALUES (%s, %s, %s, %s)"
                         val = (source, title, PublishedDate, unique_id)
                         try:
                              mycursor.execute(sql,val)
                              latest_records.append((source, title, PublishedDate, unique_id))
                         except mysql.connector.Error as err:
                              print(f'Error inserting record into database: {err}')
                    else:
                         message = 'some records already exist. Showing latest fetched records.'
                         
                    

               def yahoo_api():
                    url = "https://yahoo-finance15.p.rapidapi.com/api/v2/markets/news"
                    querystring = {"tickets":"AAPL", "type": "ALL"}
                    headers = {"x-rapidapi-key":"65d7cf85b0msh88f548ccee39fe9p121f4ejsnafcc4d564117", "x-rapidapi-host": "yahoo-finance15.p.rapidapi.com" }
                    response = requests.get(url, headers = headers, params = querystring )
                    return response.json()

               a2 = yahoo_api()
               for x in range(1,20):
                    second_var = a2['body'][x]
                    title = second_var['title']
                    source = second_var['source']
                    PublishedDate = second_var['time']
                    unique_id = second_var['url']

                    if not unique_id_exist(unique_id):
                         sql = "INSERT INTO test1(source, title, PublishedDate, unique_id) VALUES (%s, %s, %s, %s)"
                         val = (source, title, PublishedDate, unique_id)
                         try:
                              mycursor.execute(sql,val)
                              latest_records.append((source, title, PublishedDate, unique_id))
                         except mysql.connector.Error as err:
                              print(f'Error inserting record into database: {err}')
                    else:
                         message = 'some records already exist. Showing latest fetched records.'
                         
                    

               def cnbc_api():
                    url = "https://cnbc.p.rapidapi.com/news/v2/list-trending"
                    query = {"tag":"Articles","count":"30"}
                    headers = {"x-rapidapi-key":"65d7cf85b0msh88f548ccee39fe9p121f4ejsnafcc4d564117","x-rapidapi-host":"cnbc.p.rapidapi.com"}
                    response = requests.get(url, headers = headers, params = query)
                    return response.json()

               a3 = cnbc_api()
               for x in range(1,20):
                    third_var = a3['data']['mostPopularEntries']['assets'][x]
                    title = third_var['headline']
                    source = 'CNBC'
                    PublishedDate = third_var['shortDateFirstPublished']
                    unique_id = third_var['id']

                    if not unique_id_exist(unique_id):
                         sql = "INSERT INTO test1(source, title, PublishedDate, unique_id) VALUES (%s, %s, %s, %s)"
                         val = (source, title, PublishedDate, unique_id)
                         try:
                              mycursor.execute(sql,val)
                              latest_records.append((source, title, PublishedDate, unique_id))
                         except mysql.connector.Error as err:
                              print(f'Error inserting record into database: {err}')
                    else:
                         message = 'some records already exist. Showing latest fetched records.'
                         
                    

               def Theguardian_api():
                    url = "http://content.guardianapis.com/world?from-date=2021-01-01&page = 1"
                    payload = {"api-key":"70254526-e859-472f-bbdc-e820dc781b6e", "show-fields":"all"}
                    response = requests.get(url, params = payload)
                    return response.json()

               a4 = Theguardian_api()
               for x in range(1,10):
                    fourth_var = a4['response']['results'][x]
                    title = fourth_var['webTitle']
                    source = fourth_var['fields']['publication']
                    PublishedDate = fourth_var['fields']['firstPublicationDate']
                    unique_id = fourth_var['webUrl']
    
                    if not unique_id_exist(unique_id):
                         sql = "INSERT INTO test1(source, title, PublishedDate, unique_id) VALUES (%s, %s, %s, %s)"
                         val = (source, title, PublishedDate, unique_id)
                         try:
                              mycursor.execute(sql,val)
                              latest_records.append((source, title, PublishedDate, unique_id))
                         except mysql.connector.Error as err:
                              print(f'Error inserting record into database: {err}')
                    else:
                         message = 'some records already exist. Showing latest fetched records.'
                         
                    

               def news_api_content(): 
                    newsapi = NewsApiClient(api_key = "c15034b58ee244fc843bb4906e71e8bd")
                    top_headlines = newsapi.get_top_headlines(language = 'en',sources = 'cnn', page = 1)
                    return top_headlines

               a5 = news_api_content()
               for x in range(1,10):
                    fifth_var = a5['articles'][x]
                    title = fifth_var['title']
                    source = fifth_var['source']['name']
                    PublishedDate = fifth_var['publishedAt']
                    unique_id = fifth_var['url']

                    if not unique_id_exist(unique_id):
                         sql = "INSERT INTO test1(source, title, PublishedDate, unique_id) VALUES (%s, %s, %s, %s)"
                         val = (source, title, PublishedDate, unique_id)
                         try:
                              mycursor.execute(sql,val)
                              latest_records.append((source, title, PublishedDate, unique_id))
                         except mysql.connector.Error as err:
                              print(f'Error inserting records from database: {err}')
                    else:
                         message = 'some records already exist. Showing latest fetched records.'
                         
                    
               mydb.commit()

          except requests.exceptions.RequestException as e:
               message = f'API Request Error: {e}'
          except mysql.connector.Error as err:
               message = f'Database Error: {err}'

     elif request.method == 'POST' and 'display_data' in request.form:
          try:
               mycursor.execute('select * from test1 ')
               inserted_data = mycursor.fetchall()
          except mysql.connector.Error as err:
               print(f'Error fetching Data: {err}')

     elif request.method =='POST' and 'filter_data' in request.form:
          filter_type = request.form.get('filter_type')
          filter_input = request.form.get('filter_input')

          if filter_type and filter_input:
               try:
                    if filter_type == 'source':
                         mycursor.execute('select * from test1 where source = %s', (filter_input,))
               

                    elif filter_type == 'date':
                         mycursor.execute('select * from test1 where PublishedDate LIKE %s', (f'%{filter_input}%',))
               
                    elif filter_type == 'keywords':
                         keyword = f'%{filter_input}%'
                         mycursor.execute('''
                         select * from test1 
                         where title LIKE %s
                         OR source LIKE %s 
                         OR PublishedDate LIKE %s
                         OR unique_id LIKE %s  
                         ''', (keyword, keyword, keyword, keyword))
               
                    inserted_data = mycursor.fetchall()
                    message = f"No results found for '{filter_input}'." if not inserted_data else f"Showing results for '{filter_input}'."
               except mysql.connector.Error as err:
                    message = f'Database Error: {err}'

     elif request.method == 'POST' and 'filter_combined' in request.form:
                    filter_combo = request.form.get('filter_combo')
                    val1 = request.form.get('value1')
                    val2 = request.form.get('value2')

                    if filter_combo and val1 and val2:
                         try:
                              if filter_combo == 'keyword_source':
                                   mycursor.execute('Select * from test1 where title LIKE %s AND source LIKE %s', (f'%{val1}%', f'%{val2}%'))

                              elif filter_combo == 'source_date':
                                   mycursor.execute('select * from test1 where source LIKE %s AND PublishedDate LIKE %s', (f'%{val1}%', f'%{val2}%'))

                              elif filter_combo == 'date_keyword':
                                   mycursor.execute('select * from test1 where PublishedDate LIKE %s AND title LIKE %s', (f'%{val1}%', f'%{val2}%'))

                              inserted_data = mycursor.fetchall()
                              message = f"Showing results for combined Filter '{filter_combo}'" if inserted_data else 'No results found for combined filter.'    
                         except mysql.connector.Error as err:
                              message = f'Database Error: {err}'

                    else:
                         inserted_data = []
                         message = "Please fill both fields in the combined filter."

     if latest_records:
          return render_template('display.html', data = latest_records, message = message)
     
     elif inserted_data:
          return render_template('display.html', data = inserted_data, message = message)
     
     else:
          return render_template('display.html', data = [], message = 'No data available.')

mycursor.close()
mydb.close()


if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True, port = 5000)
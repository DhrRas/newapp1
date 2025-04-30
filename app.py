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

     elif request.method == 'POST' and 'apply_filters' in request.form:
                    filter_type1 = request.form.get('filter_type')
                    filter_input1 = request.form.get('filter_input')
                    filter_type2 = request.form.get('second_filter_type')
                    filter_input2 = request.form.get('second_filter_input')

                    filters = []
                    params = []

                    if filter_type1 and filter_input1:
                              if filter_type1 == 'source':
                                   filters.append('source LIKE %s')
                                   params.append(f'%{filter_input1}%')

                              elif filter_type == 'date':
                                   filters.append('PublishedDate LIKE %s')
                                   params.append(f'%{filter_input1}%')

                              elif filter_type1 == 'keywords':
                                   filters.append('(title LIKE %s OR source LIKE %s OR PublishedDate LIKE %s OR unique_id LIKE %s)')
                                   params.extend([f'%{filter_input1}%'] * 4)
                              
                    if filter_type2 and filter_input2:
                         if filter_type2 == 'source':
                              filters.append('source LIKE %s')
                              params.append(f'%{filter_input2}%')
                         
                         elif filter_type2 == 'date':
                              filters.append('PublishedDate LIKE %s')
                              params.append(f'%{filter_input2}%')
                         
                         elif filter_type2 == 'keywords':
                              filters.append('(title LIKE %s OR source LIKE %s OR PublishedDate LIKE %s OR unique_id LIKE %s)')
                              params.extend([f'%{filter_input2}%'] * 4)

                    if filters:
                              query = "select * from test1 where " + " AND".join(filters)
                              try:
                                   mycursor.execute(query, tuple(params))
                                   inserted_data = mycursor.fetchall()
                                   message = 'Showing results for combined filters.' if inserted_data else 'No results found for combined filters.'
                              except mysql.connector.Error as err:
                                   message =f'Database Error: {err}'
                    else:
                         inserted_data = []
                         message = "Please select valid filters before applying. "

     if latest_records:
          return render_template('display.html', data = latest_records, message = message)
     
     elif inserted_data:
          return render_template('display.html', data = inserted_data, message = message)
     
     else:
          return render_template('display.html', data = [], message = 'No data available.')



if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True, port = 5000)

mycursor.close()
mydb.close()


# note to change one. thing
# just show normal filter option 
# if user wants to search it with another options  then he click on add filter option where again shows filter option and then by using those selected options 
# it should display the results based on that.


# Optional:  it's upto you that if you need to add a hover effect that user hover over url then it should actually see the url 
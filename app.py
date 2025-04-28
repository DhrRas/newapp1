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
     mycursor.execute('select 1 from test1 WHERE unique_id = %s LIMIT 1', (unique_id,))
     return mycursor.fetchone() is not None

@app.route('/details', methods=['GET','POST'])

def home():
     inserted_data = []
     message = None
     latest_records = []


     if request.method == 'POST' and 'fetch_data' in request.form:
          #if count == 0:
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
                         mycursor.execute(sql,val)
                         latest_records.append((source, title, PublishedDate, unique_id))
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
                         mycursor.execute(sql,val)
                         latest_records.append((source, title, PublishedDate, unique_id))
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
                         mycursor.execute(sql,val)
                         latest_records.append((source, title, PublishedDate, unique_id))
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
                         mycursor.execute(sql,val)
                         latest_records.append((source, title, PublishedDate, unique_id))
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
                         mycursor.execute(sql,val)
                         latest_records.append((source, title, PublishedDate, unique_id))
                    else:
                         message = 'some records already exist. Showing latest fetched records.'
                         
                    
               mydb.commit()

     elif request.method == 'POST' and 'display_data' in request.form:
          mycursor.execute('select * from test1 ')
          inserted_data = mycursor.fetchall()

     elif request.method =='POST' and 'filter_data' in request.form:
          filter_type = request.form.get('filter_type')
          filter_input = request.form.get('filter_input')

          if filter_type and filter_input:
               if filter_type == 'source':
                    query = 'select * from test1 where source = %s'
                    mycursor.execute(query, (filter_input,))
               elif filter_type == 'date':
                    query = 'select * from test1 where PublishedDate LIKE %s'
                    mycursor.execute(query, (f'%{filter_input}%',))
               elif filter_type == 'keywords':
                    query = '''
                         select * from test1 
                         where title LIKE %s
                         OR source LIKE %s 
                         OR PublishedDate LIKE %s
                         OR unique_id LIKE %s  
                         '''
                    keyword = f'%{filter_input}%'
                    mycursor.execute(query, (keyword, keyword, keyword, keyword))
               
               inserted_data = mycursor.fetchall()
               if not inserted_data:
                    message = f"No results found for '{filter_input}'. Try another keyword."
               else:
                    message = f"Showing results for '{filter_input}'" 

     if latest_records:
          return render_template('display.html', data = latest_records, message = message)
     
     elif inserted_data:
          return render_template('display.html', data = inserted_data, message = None)
     
     else:
          return render_template('display.html', data = [], message = 'No data available.')



if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True, port = 5000)

mycursor.close()
mydb.close()


# then lastly add a filter options 
# 1. by keywords => it should fetches some data according to that. and same should apply for all filter options.
# 2. by date
# 3. by timestamp
# 4. by source if required.
# 5. create a dropdwon button like that and display all 
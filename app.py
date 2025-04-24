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

def unique_id_exist(unique_id):
     mycursor.execute('select 1 from test1 WHERE unique_id = %s LIMIT 1', (unique_id,))
     return mycursor.fetchone() is not None

@app.route('/details', methods=['GET','POST'])

def home():
     inserted_data = []
     message = None
     latest_records = []


     #mycursor.execute('select count(*) from test1')
     #count = mycursor.fetchone()[0]

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
                         latest_records.append((source, title, PublishedDate, unique_id))
                    

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
                         latest_records.append((source, title, PublishedDate, unique_id))
                    

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
                         latest_records.append((source, title, PublishedDate, unique_id))
                    

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
                         latest_records.append((source, title, PublishedDate, unique_id))
                    

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
                         latest_records.append((source,title, PublishedDate, unique_id))
                    


               mydb.commit()

     elif request.method == 'POST' and 'display_data' in request.form:
          mycursor.execute('select * from test1 ')
          inserted_data = mycursor.fetchall()
          

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
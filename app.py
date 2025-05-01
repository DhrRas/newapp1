from flask import Flask, render_template, request
import mysql.connector
import requests
from newsapi import NewsApiClient
import os  # For environment variables

app = Flask(__name__, template_folder='templates')

def get_db_connection():
    """Establishes and returns a MySQL database connection."""
    try:
        mydb = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', '1234'),
            database=os.environ.get('DB_DATABASE', 'mysql')
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def unique_id_exist(mycursor, unique_id):
    """Checks if a unique ID already exists in the database."""
    try:
        mycursor.execute('SELECT 1 FROM test1 WHERE unique_id = %s LIMIT 1', (unique_id,))
        return mycursor.fetchone() is not None
    except mysql.connector.Error as err:
        print(f'Error checking unique ID existence: {err}')
        return False

@app.route('/details', methods=['GET', 'POST'])
def home():
    inserted_data = []
    message = None
    latest_records = []
    mydb = None
    mycursor = None
    filter1_results = None
    filter2_results = None
    filter1_message = None
    filter2_message = None

    try:
        mydb = get_db_connection()
        if mydb:
            mycursor = mydb.cursor()

            if request.method == 'POST' and 'fetch_data' in request.form:
                try:
                    def nyt_api():
                        requestUrl = "https://api.nytimes.com/svc/news/v3/content/all/'business'.json?limit=20&api-key=NIYJ7DwbZDKjtgBI4xKGUPGim572tRKi"
                        response = requests.get(requestUrl)
                        response.raise_for_status()  # Raise an exception for bad status codes
                        return response.json()

                    a1 = nyt_api()
                    for x in range(2, 6):
                        try:
                            first_var = a1['results'][x]
                            title = first_var['title']
                            source = first_var['source']
                            PublishedDate = first_var['published_date']
                            unique_id = first_var['url']
                            if not unique_id_exist(mycursor, unique_id):
                                sql = "INSERT INTO test1(source, title, PublishedDate, unique_id) VALUES (%s, %s, %s, %s)"
                                val = (source, title, PublishedDate, unique_id)
                                mycursor.execute(sql, val)
                                latest_records.append((source, title, PublishedDate, unique_id))
                            else:
                                message = 'Some records already exist. Showing latest fetched records.'
                        except (TypeError, KeyError, IndexError) as e:
                            print(f'Error processing NYT data: {e}')

                    def yahoo_api():
                        url = "https://yahoo-finance15.p.rapidapi.com/api/v2/markets/news"
                        querystring = {"tickers":"AAPL","type":"ALL"}
                        headers = { "x-rapidapi-key": "65d7cf85b0msh88f548ccee39fe9p121f4ejsnafcc4d564117", "x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"  }
                        response = requests.get(url, headers=headers, params=querystring)
                        response.raise_for_status()
                        return response.json()

                    a2 = yahoo_api()
                    for x in range(1, 20):
                        try:
                            second_var = a2['body'][x]
                            title = second_var['title']
                            source = second_var['source']
                            PublishedDate = second_var['time']
                            unique_id = second_var['url']
                            if not unique_id_exist(mycursor, unique_id):
                                sql = "INSERT INTO test1(source, title, PublishedDate, unique_id) VALUES (%s, %s, %s, %s)"
                                val = (source, title, PublishedDate, unique_id)
                                mycursor.execute(sql, val)
                                latest_records.append((source, title, PublishedDate, unique_id))
                            else:
                                message = 'Some records already exist. Showing latest fetched records.'
                        except (TypeError, KeyError, IndexError) as e:
                            print(f'Error processing Yahoo data: {e}')

                    def cnbc_api():
                        url = "https://cnbc.p.rapidapi.com/news/v2/list-trending"
                        query = {"tag":"Articles","count":"30"}
                        headers = {"x-rapidapi-key":"65d7cf85b0msh88f548ccee39fe9p121f4ejsnafcc4d564117","x-rapidapi-host":"cnbc.p.rapidapi.com"}
                        response = requests.get(url, headers = headers , params= query)
                        response.raise_for_status()
                        return response.json()

                    a3 = cnbc_api()
                    for x in range(1, 20):
                        try:
                            third_var = a3['data']['mostPopularEntries']['assets'][x]
                            title = third_var['headline']
                            source = 'CNBC'
                            PublishedDate = third_var['shortDateFirstPublished']
                            unique_id = third_var['id']
                            if not unique_id_exist(mycursor, unique_id):
                                sql = "INSERT INTO test1(source, title, PublishedDate, unique_id) VALUES (%s, %s, %s, %s)"
                                val = (source, title, PublishedDate, unique_id)
                                mycursor.execute(sql, val)
                                latest_records.append((source, title, PublishedDate, unique_id))
                            else:
                                message = 'Some records already exist. Showing latest fetched records.'
                        except (TypeError, KeyError, IndexError) as e:
                            print(f'Error processing CNBC data: {e}')

                    def Theguardian_api():
                        url = "http://content.guardianapis.com/world?from-date=2021-01-01&page=1"
                        payload = {"api-key":"70254526-e859-472f-bbdc-e820dc781b6e", "show-fields":"all"}
                        response = requests.get(url, params = payload)
                        response.raise_for_status()
                        return response.json()

                    a4 = Theguardian_api()
                    for x in range(1, 10):
                        try:
                            fourth_var = a4['response']['results'][x]
                            title = fourth_var['webTitle']
                            source = fourth_var['fields']['publication']
                            PublishedDate = fourth_var['fields']['firstPublicationDate']
                            unique_id = fourth_var['webUrl']
                            if not unique_id_exist(mycursor, unique_id):
                                sql = "INSERT INTO test1(source, title, PublishedDate, unique_id) VALUES (%s, %s, %s, %s)"
                                val = (source, title, PublishedDate, unique_id)
                                mycursor.execute(sql, val)
                                latest_records.append((source, title, PublishedDate, unique_id))
                            else:
                                message = 'Some records already exist. Showing latest fetched records.'
                        except (TypeError, KeyError, IndexError) as e:
                            print(f'Error processing The Guardian data: {e}')

                    def news_api_content():
                        newsapi = NewsApiClient(api_key = "c15034b58ee244fc843bb4906e71e8bd")
                        top_headlines = newsapi.get_top_headlines(language='en', sources = 'cnn', page = 1)
                        return top_headlines

                    a5 = news_api_content()
                    for x in range(1, 10):
                        try:
                            fifth_var = a5['articles'][x]
                            title = fifth_var['title']
                            source = fifth_var['source']['name']
                            PublishedDate = fifth_var['publishedAt']
                            unique_id = fifth_var['url']
                            if not unique_id_exist(mycursor, unique_id):
                                sql = "INSERT INTO test1(source, title, PublishedDate, unique_id) VALUES (%s, %s, %s, %s)"
                                val = (source, title, PublishedDate, unique_id)
                                mycursor.execute(sql, val)
                                latest_records.append((source, title, PublishedDate, unique_id))
                            else:
                                message = 'Some records already exist. Showing latest fetched records.'
                        except (TypeError, KeyError, IndexError) as e:
                            print(f'Error processing NewsAPI data: {e}')
                    

                    mydb.commit()

                    if message == 'Some records already exist. Showing latest fetched records.':
                # Fetch the latest records from the database
                        mycursor.execute("SELECT source, title, PublishedDate, unique_id FROM test1 ORDER BY PublishedDate DESC LIMIT 20")
                        latest_records = mycursor.fetchall()
                        inserted_data = latest_records # Assign the latest records to inserted_data
                    elif not message: # If new records were fetched and inserted
                        mycursor.execute("SELECT source, title, PublishedDate, unique_id FROM test1 ORDER BY PublishedDate DESC LIMIT 20")
                        inserted_data = mycursor.fetchall()
                    else:
                        inserted_data = [] 

                except requests.exceptions.RequestException as e:
                    message = f'API Request Error: {e}'
                except mysql.connector.Error as err:
                    message = f'Database Error during fetch: {err}'

                return render_template('display.html', data=inserted_data, message= message)

            elif request.method == 'POST' and 'display_data' in request.form:
                try:
                    mycursor.execute('SELECT * FROM test1')
                    inserted_data = mycursor.fetchall()
                except mysql.connector.Error as err:
                    message = f'Error fetching Data: {err}'

            elif request.method == 'POST' and 'filter_data' in request.form:
                filter_type = request.form.get('filter_type')
                filter_input = request.form.get('filter_input')
                filter_keyword = None  # Initialize filter_keyword here

                if filter_type and filter_input:
                    filter_keyword = filter_input # Assign only if it has a value
                    try:
                        query = 'SELECT * FROM test1 WHERE '
                        if filter_type == 'source':
                            query += 'source LIKE %s'
                            params = (f'%{filter_input}%',)
                        elif filter_type == 'date':
                            query += 'PublishedDate LIKE %s'
                            params = (f'%{filter_input}%',)
                        elif filter_type == 'keywords':
                            query += '(title LIKE %s OR source LIKE %s OR PublishedDate LIKE %s OR unique_id LIKE %s)'
                            params = (f'%{filter_input}%',) * 4
                        else:
                            message = 'Invalid filter type.'
                            inserted_data = []
                            params = ()

                        if not message:
                            mycursor.execute(query, params)
                            inserted_data = mycursor.fetchall()
                            message = f"No results found for '{filter_input}'." if not inserted_data else f"Showing results for '{filter_input}'."
                    except mysql.connector.Error as err:
                        message = f'Database Error during filter: {err}'
                else:
                    inserted_data = []
                    message = "Please select a filter type and enter a value."

                filter1_results = None
                filter2_results = None

                return render_template('display.html', data=inserted_data, message=message,
                               filter1_status=None, filter2_status=None,
                               filter1_message=None, filter2_message=None,
                               filter_keyword=filter_keyword) # Use the initialized filter_keyword

            elif request.method == 'POST' and 'apply_filters' in request.form:
                filter_type1 = request.form.get('filter_type')
                filter_input1 = request.form.get('filter_input')
                filter_type2 = request.form.get('second_filter_type')
                filter_input2 = request.form.get('second_filter_input')

                filters = []
                params = []
                filter1_results = False
                filter2_results = False
                filter1_message = None
                filter2_message = None

                def apply_single_filter(filter_type, filter_input):
                    if not filter_type or not filter_input:
                        return None, None, None
                    query_part, param = add_filter_condition(filter_type, filter_input)
                    if query_part:
                        query = f"SELECT * FROM test1 WHERE {query_part}"
                        try:
                            mycursor.execute(query, param if isinstance(param, tuple) else (param,))
                            results = mycursor.fetchall()
                            if results:
                                return query_part, param, True
                            else:
                                return query_part, param, False
                        except mysql.connector.Error as err:
                            print(f"Database error during single filter: {err}")
                            return None, None, None
                    return None, None, None

                def add_filter_condition(filter_type, filter_input):
                    if filter_type == 'source':
                        return 'source LIKE %s', f'%{filter_input}%'
                    elif filter_type == 'date':
                        return 'PublishedDate LIKE %s', f'%{filter_input}%'
                    elif filter_type == 'keywords':
                        return '(title LIKE %s OR source LIKE %s OR PublishedDate LIKE %s OR unique_id LIKE %s)', [f'%{filter_input}%'] * 4
                    return None, None

                if filter_type1 and filter_input1:
                    condition1, param1, filter1_success = apply_single_filter(filter_type1, filter_input1)
                    if condition1:
                        filters.append(condition1)
                        if isinstance(param1, list):
                            params.extend(param1)
                        else:
                            params.append(param1)
                        filter1_results = filter1_success
                        filter1_message = f'Showing results for {filter_type1}: "{filter_input1}"' if filter1_success else f'No results for {filter_type1}: "{filter_input1}"'

                if filter_type2 and filter_input2:
                    condition2, param2, filter2_success = apply_single_filter(filter_type2, filter_input2)
                    if condition2:
                        if filters:
                            filters.append("AND " + condition2)
                        else:
                            filters.append(condition2)
                        if isinstance(param2, list):
                            params.extend(param2)
                        else:
                            params.append(param2)
                        filter2_results = filter2_success
                        filter2_message = f'Showing results for {filter_type2}: "{filter_input2}"' if filter2_success else f'No results for {filter_type2}: "{filter_input2}"'

                if filters:
                    query = "SELECT * FROM test1 WHERE " + " ".join(filters)
                    try:
                        mycursor.execute(query, tuple(params))
                        inserted_data = mycursor.fetchall()
                        if not inserted_data and not filter1_results and not filter2_results:
                            message = "No results found for the applied filters."
                        else:
                            message = "Results based on applied filters:"
                    except mysql.connector.Error as err:
                        message = f'Database Error during apply filters: {err}'
                else:
                    inserted_data = []
                    message = "Please select at least one filter before applying."
                    filter1_results = False
                    filter2_results = False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        message = f"An unexpected error occurred: {e}"
    finally:
        if mydb and mydb.is_connected():
            mycursor.close()
            mydb.close()

    return render_template('display.html', data=inserted_data, message=message,
                           filter1_status=filter1_results, filter2_status=filter2_results,
                           filter1_message=filter1_message, filter2_message=filter2_message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)

import urllib2
from bs4 import BeautifulSoup
import threading
import json

result = [] # List of dictionaries containing final output to be appended in file.

"""fetch_data fetches the relevant data as key:value pairs(dictionary) given a url(wikipedia).
Then appends the data fetched to result.""" 
def fetch_data(url):
    # try fetching a response, in case of exception raise error
    try:
        response = urllib2.urlopen(url)
        soup = BeautifulSoup(response.read(),'html.parser') #For parsing
        response.close()
    except urllib2.HTTPError as e:
        print url
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except urllib2.URLError as e:
        print url
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    else:
        # everything is fine
        # extract the relevant data
        data = {}
        table = soup.find('table', attrs={'class':'infobox vcard'})

        try:
            rows = table.find_all('tr')
        except:
            print url
            return

        for row in rows:
            th = row.find('th')
            td = row.find('td')
            if th is not None and td is not None:
                key = th.get_text().strip().encode('utf8')
                val = td.get_text().strip().encode('utf8')
                data[key] = val
            else:
                print url

        result.append(data) # append relevant data to the final result

# creating wikipedia urls
baseUrl = "https://en.wikipedia.org"
urls = []
try:
    response = urllib2.urlopen("https://en.wikipedia.org/wiki/List_of_companies_of_the_United_States") # US companies
    soup = BeautifulSoup(response.read(),'html.parser') #For parsing
    response.close()
except urllib2.HTTPError as e:
    print url
    print 'The server couldn\'t fulfill the request.'
    print 'Error code: ', e.code
except urllib2.URLError as e:
    print url
    print 'We failed to reach a server.'
    print 'Reason: ', e.reason
else:
    categories = soup.find_all('div', attrs={'class':"div-col columns column-width", 
        'style':"-moz-column-width: 30em; -webkit-column-width: 30em; column-width: 30em;"})
    for category in categories:
        companies = category.find_all('a',href=True)
        for company in companies:
            urls.append(baseUrl + company['href'])

# creating threads for fetching data in parallel (limiting amount of concurrent thread to 100)
print len(urls)

f = open('output.json','a')

i = 0
while(i+100<len(urls)):
    threads = [threading.Thread(target=fetch_data, args=(url,)) for url in urls[i:i+100]]
    i += 100
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print len(result)
    
    # writing to file in json format which is in sync with mongoDB data format
    for row in result:
        f.write(json.dumps(row, sort_keys=True, 
            indent=4, separators=(',', ': ')))
        f.write('\n')
    result = []

threads = [threading.Thread(target=fetch_data, args=(url,)) for url in urls[i:len(urls)]]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print len(result)

# writing to file in json format which is in sync with mongoDB data format
for row in result:
    f.write(json.dumps(row, sort_keys=True, 
        indent=4, separators=(',', ': ')))
    f.write('\n')

f.close()
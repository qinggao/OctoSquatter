import requests
import bs4

import datetime
import time
import calendar
import dateutil.parser


root_url = 'https://github.com/search?type=Repositories&utf8=%E2%9C%93'

# query_string = '&q=' + 'python'
# lang = '&l=' + 'python'

query_string = '&q=' + input("Search: ")

while query_string == '&q=':
    print ("Search string cannot be empty!")
    query_string = '&q=' + input("Search: ")
    
lang = '&l=' + input("Language: ")

if lang == '&l=':
    lang = ''

pages = int(input("How many pages to parse: "))

def get_repos(page):

    index_url = root_url + lang + query_string + "&p=" + repr(page)

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text).select('li.repo-list-item')

    if len(soup) != 0:
        for x in soup:
            project_title = x.select('h3.repo-list-name')[0].a['href']
            project_description = x.select('p.repo-list-description')
            if project_description != []:
                project_description = project_description[0].get_text().strip()
            last_update_time = calendar.timegm(datetime.datetime.strptime(x.time['datetime'], "%Y-%m-%dT%H:%M:%SZ").timetuple())
            time_diff = calendar.timegm((datetime.datetime.utcnow() - datetime.timedelta(weeks=20)).utctimetuple())
            if last_update_time < time_diff:
                print (project_title)
                print (project_description)
                print (datetime.datetime.strptime(x.time['datetime'], "%Y-%m-%dT%H:%M:%SZ"))
    else:
        return 404

for x in range(100,pages):
    if get_repos(x) == 404:
        print (x, 404)
        break
    print ("Page number", x)


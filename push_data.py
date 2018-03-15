'''
THIS FILE PUSHES FILTERED DATA FROM HACKER NEWS TO FIREBASE DATABASE
AUTHOR: ANDY COUTO
'''

import requests
from html.parser import HTMLParser
import sys
from firebase import firebase
from geograpy import extraction
from geopy.geocoders import Nominatim


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# TODO make filter variables like points = 100; points_query = f'hitsPerPage={points}'
# then pass points_query inside filter_for_object_query
def establish_web_response(search_query):
    web_response = requests.get(search_query)
    if web_response.status_code == 200:
        return web_response
    else:
        return print("Error getting web response: %s", web_response.status_code)


def get_json_hits(web_response):
    json_data = web_response.json()
    json_hits = json_data['hits']  # looks at only the first dictionary with the data we want
    return json_hits


def extract_info(json_hits):
    title_id = {}
    list_of_valid_hits = []  # store the valid objectIds
    for hits in json_hits:
        if hits['title'] is not None and hits['points'] > 100:
            title = hits['title']
            title = title[title.find("(") + 1:title.find(")")]  # get only the month and year
            title_id[hits['objectID']] = title  # add month year and id to dict
            list_of_valid_hits.append(hits['objectID'])
    return title_id, list_of_valid_hits


def update_languages(cleaned_comment, languages, keys):
    for i in keys:
        if i in cleaned_comment:
            languages[i] += 1


def remove_values(unfiltered_list, value):
    while value in unfiltered_list:
        unfiltered_list.remove(value)


def main():
    HN_database = firebase.FirebaseApplication('https://hackernewsgraphs.firebaseio.com/', None)
    response = establish_web_response('https://hn.algolia.com/api/v1/search_by_date?query=%22Ask%20HN%20:%20Who%20is%20hiring%3F%22&hitsPerPage=100&numericFilters=created_at_i>1454338862')
    json_hits = get_json_hits(response)
    titles, ids = extract_info(json_hits)
    get_url = 'http://hn.algolia.com/api/v1/items/'
    # geolocator = Nominatim()
    this_yr_locations = []
    last_yr_locations = []

    HN_database.delete('', '')

    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    states_1 = {"AL": 0, "AK": 0, "AZ": 0, "AR": 0, "CA": 0, "CO": 0, "CT": 0, "DC": 0, "DE": 0, "FL": 0, "GA": 0,
              "HI": 0, "ID": 0, "IL": 0, "IN": 0, "IA": 0, "KS": 0, "KY": 0, "LA": 0, "ME": 0, "MD": 0,
              "MA": 0, "MI": 0, "MN": 0, "MS": 0, "MO": 0, "MT": 0, "NE": 0, "NV": 0, "NH": 0, "NJ": 0,
              "NM": 0, "NY": 0, "NC": 0, "ND": 0, "OH": 0, "OK": 0, "OR": 0, "PA": 0, "RI": 0, "SC": 0,
              "SD": 0, "TN": 0, "TX": 0, "UT": 0, "VT": 0, "VA": 0, "WA": 0, "WV": 0, "WI": 0, "WY": 0}

    states_2 = {"AL": 0, "AK": 0, "AZ": 0, "AR": 0, "CA": 0, "CO": 0, "CT": 0, "DC": 0, "DE": 0, "FL": 0, "GA": 0,
              "HI": 0, "ID": 0, "IL": 0, "IN": 0, "IA": 0, "KS": 0, "KY": 0, "LA": 0, "ME": 0, "MD": 0,
              "MA": 0, "MI": 0, "MN": 0, "MS": 0, "MO": 0, "MT": 0, "NE": 0, "NV": 0, "NH": 0, "NJ": 0,
              "NM": 0, "NY": 0, "NC": 0, "ND": 0, "OH": 0, "OK": 0, "OR": 0, "PA": 0, "RI": 0, "SC": 0,
              "SD": 0, "TN": 0, "TX": 0, "UT": 0, "VT": 0, "VA": 0, "WA": 0, "WV": 0, "WI": 0, "WY": 0}

    for i in range(len(ids)):
        month_url = requests.get(get_url + str(ids[i])).json()
        month_title = titles[str(month_url['id'])]
        get_coord = False
        this_year = 'March 2018'
        last_year = 'March 2017'
        if month_title == this_year or month_title == last_year:
            get_coord = True
        children = month_url['children']
        languages = {
            'python': 0,
            ' c ': 0,
            ' c, ': 0,
            ' java ': 0,
            ' java, ': 0,
            ' java. ': 0,
            'c++': 0,
            'c#': 0,
            ' r ': 0,
            ' r, ': 0,
            'javascript': 0,
            'php': 0,
            ' go ': 0,
            ' go, ': 0,
            'swift': 0
        }
        keys = languages.keys()
        num_comments = 0
        onsite = 0
        remote = 0
        for comment in children:
            if comment is not None and comment['parent_id'] == month_url['id']:
                if comment['text'] is not None:
                    if get_coord:
                        e = extraction.Extractor(comment['text'])
                        e.find_entities()
                        entities = e.places[:5]  # if location not in first few entities drop it
                        place_found = False
                        for entity in entities:
                            if not place_found:
                                for state in states:
                                    if state in entity:
                                        # location = geolocator.geocode(state)
                                        # if location is not None:
                                            # point = (location.latitude, location.longitude)
                                            if month_title == this_year:
                                                this_yr_locations.append(state)
                                            elif month_title == last_year:
                                                last_yr_locations.append(state)
                                            place_found = True
                    cleaned_comment = strip_tags(comment['text'].lower())
                    if 'onsite' or 'on-site' in cleaned_comment:
                        onsite += 1
                    if 'remote' in cleaned_comment:
                        remote += 1
                    num_comments += 1
                    update_languages(cleaned_comment, languages, keys)

        percent = ((i+1)/len(ids))*100
        sys.stdout.write("\rUploading: %d%% complete" % percent)
        sys.stdout.flush()

        HN_database.post('/num_comments', {month_title: num_comments})

        HN_database.post('/onsite', {month_title: onsite})
        HN_database.post('/remote', {month_title: remote})

        HN_database.post('/python', {month_title: languages['python']})
        c = languages[' c '] + languages[' c, ']
        HN_database.post('/c', {month_title: c})
        java = languages[' java '] + languages[' java, '] + languages[' java. ']
        HN_database.post('/java', {month_title: java})
        HN_database.post('/cplusplus', {month_title: languages['c++']})
        HN_database.post('/csharp', {month_title: languages['c#']})
        r = languages[' r '] + languages[' r, ']
        HN_database.post('/r', {month_title: r})
        HN_database.post('/javascript', {month_title: languages['javascript']})
        HN_database.post('/php', {month_title: languages['php']})
        go = languages[' go '] + languages[' go, ']
        HN_database.post('/go', {month_title: go})
        HN_database.post('/swift', {month_title: languages['swift']})

    for state in states:
        states_1[state] = this_yr_locations.count(state)
        states_2[state] = last_yr_locations.count(state)

    file = open("location_data.csv", "w")
    file.write("state,year1,year2\n")
    for state in states:
        file.write(state + "," + str(states_1[state]) + "," + str(states_2[state]) + "\n")
    file.close()


if __name__ == '__main__':
    main()
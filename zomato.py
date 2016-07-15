import urllib2
import urllib
import json
import pymongo
from pymongo import MongoClient
# client = MongoClient("mongodb://43.252.89.89:27017")
# db = client.test_main
#
try:
    list_of_params = {"q": "vivanta by",
                      "lat": "19.913114", "lon": "75.347048"}
    url_string = urllib.urlencode(list_of_params)
    # print url_string
    req = urllib2.Request(
        "https://developers.zomato.com/api/v2.1/search?%s" % (url_string))
    req.add_header("user-key", "<API-KEY>")
    response = urllib2.urlopen(req)
    # print response
    json_data = json.load(response)
# res_id = json_data["results_found"]

    res_id = json_data["restaurants"][0]["restaurant"]["R"]["res_id"]
    aggregate_rating = json_data["restaurants"][0][
        "restaurant"]["user_rating"]["aggregate_rating"]
    # print aggregate_rating
    list_of_params = {"res_id": res_id, "start": 0, "count": 20}
    url_string = urllib.urlencode(list_of_params)
    req = urllib2.Request(
        "https://developers.zomato.com/api/v2.1/reviews?%s" % (url_string))
    req.add_header("user-key", "<API-KEY>")
    response = urllib2.urlopen(req)
# print response
    json_data = json.load(response)
except:
    pass
# res_id = json_data["results_found"]
try:
    reviews_count = json_data["reviews_count"]
except:
    reviews_count = 0


class zomato(object):
    """zamato object having all properties"""

    def __init__(self, rating, review_text, user_name, source):
        self.rating = rating
        self.review_text = review_text
        self.user_name = user_name
        self.source = source


ALL = []
for i in range(reviews_count):
    try:
        rating = json_data["user_reviews"][i]["review"]["rating"]
    except:
        rating = " "
    try:
        review_text = json_data["user_reviews"][i]["review"]["review_text"]
    except:
        review_text = " "
    try:
        user_name = json_data["user_reviews"][i]["review"]["user"]["name"]
    except:
        user_name = " "
    source = "www.zomato.com"
    z = zomato(rating=rating, review_text=review_text,
               user_name=user_name, source=source)
    ALL.append(z)

# print reviews


# Enter the api keys before running


for i in ALL:
    print i.__dict__

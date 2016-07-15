from flask import Flask
import urllib2
import urllib
import json

app = Flask(__name__)

@app.route('/zomato/<title>')
def api(title=None):
	try:
	    list_of_params = {"q": title} #, "lat": "19.913114", "lon": "75.347048"}
	    url_string = urllib.urlencode(list_of_params)
	    url = "https://developers.zomato.com/api/v2.1/search?%s" % (url_string)
	    req = urllib2.Request(url)
	    req.add_header("user-key", "3a5ad6e553a4fcfeae795494f51c2f76")
	    response = urllib2.urlopen(req)
	    print response.read()
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
	    req.add_header("user-key", "3a5ad6e553a4fcfeae795494f51c2f76")
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

	for i in ALL:
	    return json.dumps(i.__dict__)

if __name__ == '__main__':
	app.debug = True
	app.run()

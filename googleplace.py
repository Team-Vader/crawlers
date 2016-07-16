from googleplaces import GooglePlaces, types, lang
from pprint import pprint

YOUR_API_KEY = 'AIzaSyCLTwL7ffZJ1KPd8TqYVuCYN9qD7VwuZII'

google_places = GooglePlaces(YOUR_API_KEY)

# You may prefer to use the text_search API, instead.
query_result = google_places.nearby_search(location='London, England', keyword='Fish and Chips',
    radius=20000, types=[types.TYPE_FOOD])

if query_result.has_attributions:
    # print "hello\n\n\n"
    print query_result.html_attributions



ALL = []


for place in query_result.places:
    # Returned places from a query are place summaries.
    name = place.name
    geo = place.geo_location
    # id = place.place_id
    # print pprint(place.__dict__)
    # print "\n\n\n\nlkasjdklj\n\n\n"
    # The following method has to make a further API call.
    # pprint(place.get_details())
    # Referencing any of the attributes below, prior to making a call to
    place.get_details()# will raise a googleplaces.GooglePlacesAttributeError.
    details = place.details # A dict matching the JSON response from Google.
    phone = place.local_phone_number
    international_phone = place.international_phone_number
    website = place.website
    url = place.url

    place_obj = place.__dict__
    # Getting place photos
    place_obj['mime'] = []
    place_obj['img_url'] = []
    place_obj['filename'] = []
    place_obj['raw_img'] = []

    for photo in place.photos:
        # 'maxheight' or 'maxwidth' is required
        photo.get(maxheight=500, maxwidth=500)
        # MIME-type, e.g. 'image/jpeg'
        mime = photo.mimetype
        # Image URL
        img_url = photo.url
        # Original filename (optional)
        filename = photo.filename
        # Raw image data
        raw_img = photo.data
        place_obj['mime'].append(mime)
        place_obj['img_url'].append(img_url)
        place_obj['filename'].append(filename)
        place_obj['raw_img'].append(raw_img)

    place_obj['_query_instance'] = None
    place_obj['raw_img'] = None
    place_obj['_query_instance'] = None
    place_obj['_query_instance'] = None
    pprint(place_obj)
    # print "\n\n\n\n"

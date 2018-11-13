import flickrapi
import urllib
import os

api_key = 'f2dde0fc40550083e8c8ccd08d1d0a6e'
api_secret = 'f680d9cb8a600510'

# instantiating flickrapi with api key and secret and response form for data
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# group_id shortlisted to create a dummy environment
groups = ["4522828@N24", "2740203@N20", "1986740@N21", "56407608@N00", "535624@N24"]

# create an images directory where images will be stored
if not os.path.exists("images"):
	os.makedirs("images")

for group in groups:
	# make a directory for each group
	if not os.path.exists("images/" + group):
		os.makedirs("images/"+group)

	# fetch 30 photos from each group and store it locally and make its entry in database
	photos = flickr.photos.search(group_id=group, per_page='30').get("photos")
	for photo in photos.get("photo"):
		image = "https://farm{0}.staticflickr.com/{1}/{2}_{3}_q.jpg".format(photo["farm"],
			photo["server"], photo["id"], photo["secret"])
		target = "images/{0}/{1}.jpg".format(group, photo["id"])
		urllib.urlretrieve(image, target)

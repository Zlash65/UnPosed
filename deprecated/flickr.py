import flickrapi, os, urllib
from database import PhotoDB
from random import randint

api_key = 'f2dde0fc40550083e8c8ccd08d1d0a6e'
api_secret = 'f680d9cb8a600510'

# instantiating flickrapi with api key and secret and response form for data
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
photo_db = PhotoDB() #establish connection with database

def setup():
	# group_id shortlisted to create a dummy environment
	groups = ["4522828@N24", "2740203@N20", "1986740@N21",
		"56407608@N00", "535624@N24", "3007017@N22"]
	# groups = ["56407608@N00"]

	# create an images directory where images will be stored
	if not os.path.exists("images"):
		os.makedirs("images")

	for group in groups:
		# make a directory for each group
		if not os.path.exists("images/" + group):
			os.makedirs("images/"+group)

		# fetch 30 photos from each group and store it locally and make its entry in database
		random = randint(20,30)
		photos = flickr.photos.search(group_id=group, per_page=random).get("photos")
		# photos = flickr.photos.search(group_id=group, per_page=3).get("photos")
		no_of_photos = 0

		for photo in photos.get("photo"):
			image = "https://farm{0}.staticflickr.com/{1}/{2}_{3}_q.jpg".format(photo.get("farm"),
				photo.get("server"), photo.get("id"), photo.get("secret"))
			target = "images/{0}/{1}.jpg".format(group, photo.get("id"))

			ph = get_photo_info(photo.get("id"))
			ph.update({"url": target, "group_id": group})

			if insert_photo(ph):
				no_of_photos += 1
				urllib.urlretrieve(image, target)

		insert_group(group, no_of_photos)

def insert_group(group, total_photos):
	''' insert group data in db '''
	group = get_group_info(group)
	group.update({'total_photos': total_photos})
	return photo_db.insert_group(group)

def insert_photo(photo):
	''' insert photo data in db '''
	return photo_db.insert_photo(photo)

def search_group_by_text(txt, per_page=5):
	''' fetches list of groups based on the text provided'''
	if not txt: raise "No text provided to search for groups"

	groups = flickr.groups.search(text=txt, per_page=per_page).get("groups").get("group")

	return groups

def get_group_info(group_id):
	''' fetches detail of a group '''
	if not group_id: return False

	group = flickr.groups.getInfo(group_id=group_id).get("group")

	return {
		"name": group.get("name").get("_content"),
		"group_id": group.get("nsid"),
		# "description": group.get("description").get("_content"),
		# "topic_count":  group.get("topic_count").get("_content"),
		"iconserver":  group.get("iconserver"),
		"privacy":  group.get("privacy").get("_content"),
		# "members":  group.get("members").get("_content"),
		# "total_photos":  group.get("pool_count").get("_content"),
		"iconfarm":  group.get("iconfarm")
	}

def get_photo_info(photo_id):
	''' fetches detail of a photo '''
	if not photo_id: return False

	photo = flickr.photos.getInfo(photo_id=photo_id).get("photo")

	tags = []
	for tag in photo.get("tags").get("tag"):
		tags.append(tag.get("_content"))

	return {
		"photo_id": photo.get("id"),
		"title": photo.get("title").get("_content"),
		# "description": photo.get("description").get("_content"),
		# "views": photo.get("views"),
		"dateuploaded": photo.get("dateuploaded"),
		"datetaken": photo.get("dates").get("taken"),
		"originalformat":  photo.get("originalformat"),
		"iconserver":  photo.get("owner").get("iconserver"),
		"location":  photo.get("owner").get("location"),
		"iconfarm":  photo.get("owner").get("iconfarm"),
		"nsid": photo.get("owner").get("nsid"),
		"tags": tags
	}

if __name__ == "__main__":
	setup()

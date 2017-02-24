#!/usr/bin/python

__app_id__ = '1111111'

import os
import datetime
import sys
import argparse
import time
from getpass import getpass

try:
	import requests
except ImportError:
	print("Cannot find requests module. Please install it and try again.")
	print("Try execute command '# pip install requests'")
	sys.exit(0)

try:
	import vk
except ImportError:
	print("Cannot find vk module. Please install it and try again.")
	print("Try execute command '# pip install vk'")
	sys.exit(0)

def connect(username, password):
	print("Connect to vk.com as: %s" % username)
	session = vk.AuthSession(app_id=__app_id__, user_login=username, user_password=password)
	api = vk.API(session)
	return api

def get_photos(connection, owner_id, album_id):
	return connection.photos.get(owner_id=owner_id, album_id=album_id)

def download_photos(photos, path_to_store):
	print("Downloading...")
	photo_counts = 0
	for photo in photos:
		print(photo['src_xxbig'] or photo['src_xbig'] or photo['src_big'])
		url = photo['src_xxbig'] or photo['src_xbig'] or photo['src_big']
		r = requests.get(url)
		title = photo['pid']
		with open(os.path.join(path_to_store, '%s.jpg' % title), 'wb') as f:
			for buf in r.iter_content(1024):
				if buf:
					f.write(buf)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('username', help = 'vk.com username')
	parser.add_argument('owner_id', help = 'owner id')
	parser.add_argument('album_id', help = 'album id')
	parser.add_argument('-p', '--path', help = 'path to store photos',
		default = os.path.abspath(os.path.join(os.path.dirname(__file__), 'exported')))
	

	args = parser.parse_args()

	if args.path.startswith('~'):
		args.path = os.path.expanduser(args.output)

	start_time = datetime.datetime.now()

	try:
		password = getpass("Password: ")

		connection = connect(args.username, password)

		photos = get_photos(connection, args.owner_id, args.album_id)

		if not os.path.exists(args.path):
			os.makedirs(args.path)

		download_photos(photos, args.path)

	except Exception as e:
		print(e)
		sys.exit(1)

	except KeyboardInterrupt:
		print('vk_photos_downloader stopped by keyboard')
		sys.exit(0)

	finally:
		print("Done in %s" % (datetime.datetime.now() - start_time))


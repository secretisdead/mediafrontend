import os

from flask import request, abort, url_for

from media import MediumStatus, MediumProtection, MediumSearchability

def md5_to_id(md5):
	import base64
	return base64.urlsafe_b64encode(md5).decode().strip('=')

def id_to_md5(id):
	from base64_url_repad import base64_url_repad
	import base64
	try:
		md5 = base64.urlsafe_b64decode(
			base64_url_repad(id)
		)
	except ValueError:
		return None

	return md5

def uuid_to_id(uuid):
	import base64
	return base64.urlsafe_b64encode(uuid.bytes).decode().strip('=')

def id_to_uuid(id):
	from base64_url_repad import base64_url_repad
	import base64
	try:
		uuid_bytes = base64.urlsafe_b64decode(
			base64_url_repad(id)
		)
	except ValueError:
		return None

	from uuid import UUID
	try:
		uuid = UUID(bytes=uuid_bytes)
	except ValueError:
		return None

	return uuid

def populate_id(object):
	if hasattr(object, 'uuid'):
		object.id = uuid_to_id(object.uuid)
	if hasattr(object, 'md5'):
		object.id = md5_to_id(object.md5)

def mime_to_extension(mime):
	mimes_to_extensions = {
		# application
		'application/x-dosexec': 'exe',
		'application/x-shockwave-flash': 'swf',
		'application/pdf': 'pdf',
		# application special mimetype?
		'application/x-msdownload': 'exe',

		# audio
		'audio/mpeg': 'mp3',
		'audio/x-wav': 'wav',
		'audio/x-flac': 'flac',
		'audio/midi': 'mid',
		'audio/x-mod': 'mod',
		# audio special mimetype?
		'audio/mp3': 'mp3',
		'audio/x-ms-wma': 'wma',
		'audio/ogg': 'oga',
		'audio/webm': 'weba',
		'audio/3gpp': '3gp',
		'audio/3gpp2': '3g2',
		'audio/aac': 'aac',
		'audio/ac3': 'ac3',
		'audio/x-aiff': 'aif',
		'audio/aiff': 'aif',

		# archive
		'application/zip': 'zip',
		'application/x-gzip': 'gz',
		'application/x-tar': 'tar',
		'application/x-7z-compressed': '7z',
		'application/x-rar': 'rar',
		'application/x-bzip': 'bz',
		'application/x-bzip2': 'bz2',
		# archive special mimetype?
		'application/x-rar-compressed': 'rar',
		'application/gzip': 'gz',
		'application/x-zip': 'zip',
		'application/x-zip-compressed': 'zip',
		'application/s-compressed': 'zip',
		'multipart/x-zip': 'zip',
		'application/x-gtar': 'gtar',
		'application/x-gzip-compressed': 'tgz',

		# image
		'image/png': 'png',
		'image/jpeg': 'jpg',
		'image/gif': 'gif',
		'image/svg+xml': 'svg',
		# image special mimetype?
		'image/webp': 'webp',

		# text
		'text/plain': 'txt',
		'text/x-c++': 'txt',
		# text special mimetype?
		'text/srt': 'srt',
		'text/vtt': 'vtt',

		# video
		'video/mp4': 'mp4',
		'application/ogg': 'ogg',
		'video/x-ms-asf': 'wmv',
		'video/x-flv': 'flv',
		'video/x-msvideo': 'avi',
		'video/webm': 'webm',
		'video/quicktime': 'mov',
		'video/3gpp': '3gp',
		# video special mimetype?
		'video/3gpp2': '3g2',
		'video/ogg': 'ogv',
		'video/x-matroska': 'mkv',
		'video/x-ms-wmv': 'wmv',
		'video/avi': 'avi',
		'application/x-troff-msvideo': 'avi',
		'video/mpeg': 'mpg',
	}

	if mime not in mimes_to_extensions:
		return 'unknown'

	return mimes_to_extensions[mime]

def mime_to_category(mime):
	mimes_to_categories = {
		'application':	[
			'application/x-dosexec',
			'application/x-shockwave-flash',
			'application/pdf',
			# application special mimetype?
			'application/x-msdownload',
		],
		'audio':	[
			'audio/mpeg',
			'audio/x-wav',
			'audio/x-flac',
			'audio/midi',
			'audio/x-mod',
			# audio special mimetype?
			'audio/mp3',
			'audio/x-ms-wma',
			'audio/ogg',
			'audio/webm',
			'audio/3gpp',
			'audio/3gpp2',
			'audio/aac',
			'audio/ac3',
			'audio/x-aiff',
			'audio/aiff',
		],
		'archive':	[
			'application/zip',
			'application/x-gzip',
			'application/x-tar',
			'application/x-7z-compressed',
			'application/x-rar',
			'application/x-bzip',
			'application/x-bzip2',
			# archive special mimetype?
			'application/x-rar-compressed',
			'application/gzip',
			'application/x-zip',
			'application/x-zip-compressed',
			'application/s-compressed',
			'multipart/x-zip',
			'application/x-gtar',
			'application/x-gzip-compressed',
		],
		'image': [
			'image/png',
			'image/jpeg',
			'image/gif',
			'image/svg+xml',
			# image special mimetype?
			'image/webp',
		],
		'text':	[
			'text/plain',
			'text/x-c++',
			# text special mimetype?
			'text/srt',
			'text/vtt',
		],
		'video':	[
			'video/webm',
			'video/mp4',
			'application/ogg',
			'video/x-ms-asf',
			'video/x-flv',
			'video/x-msvideo',
			'video/quicktime',
			'video/3gpp',
			# video special mimetype?
			'video/ogg',
			'video/mpeg',
			'video/3gpp2',
			'video/x-matroska',
			'video/x-ms-wmv',
			'video/avi',
			'application/x-troff-msvideo',
		],
	}

	for category in mimes_to_categories:
		if mime in mimes_to_categories[category]:
			return category

	return 'unknown'

def populate_category(medium):
	if medium:
		medium.category = mime_to_category(medium.mime)

def populate_categories(media):
	for medium in media:
		medium.category = mime_to_category(medium.mime)

def get_file_size(file_path):
	return os.path.getsize(file_path)

def get_file_mime(file_path):
	import magic
	mime = magic.Magic(mime=True)
	return mime.from_file(file_path)

def get_file_md5(file_path):
	chunk_size = 4096

	import hashlib
	hash_algo = hashlib.md5()

	with open(file_path, 'rb') as f:
		for chunk in iter(lambda: f.read(chunk_size), b''):
			hash_algo.update(chunk)
	return hash_algo.digest()

def rgb_average_from_image(image):
	from PIL import Image

	small_image = image.copy()
	small_image.thumbnail((256, 256), Image.BICUBIC)
	data = list(small_image.getdata())
	total_pixels = len(data)
	r = 0
	g = 0
	b = 0
	for pixel in data:
		#TODO gif breaks this for some reason
		if isinstance(pixel, int):
			return 0, 0, 0
		if 4 == len(pixel):
			pr, pg, pb, pa = pixel
			if 0 == pa:
				total_pixels -= 1
				continue
		elif 3 == len(pixel):
			(pr, pg, pb) = pixel
		else:
			return 0, 0, 0
		r += pr
		g += pg
		b += pb
	r = round(r / total_pixels)
	g = round(g / total_pixels)
	b = round(b / total_pixels)
	return r, g, b

def hsv_average_from_image(image):
	import colorsys
	return colorsys.rgb_to_hsv(*rgb_average_from_image(image))

def hsv_to_int(h, s, v):
	import math

	if isinstance(h, float):
		h = math.floor(h * 255)
	if isinstance(s, float):
		s = math.floor(s * 255)
	if isinstance(v, float):
		v = math.floor(v * 255)

	# store in 3 bytes
	h = h << 16
	s = s << 8

	return (h + s + v)

def int_to_hsv(hsv_int):
	h = hsv_int >> 16
	hsv_int -= h << 16
	s = hsv_int >> 8
	v = hsv_int - (s << 8)
	return h, s, v

def hsv_int_to_rgb(hsv_int):
	import colorsys
	import math

	h, s, v = int_to_hsv(hsv_int)
	r, g, b = colorsys.hsv_to_rgb(h / 255, s / 255, v / 255)

	return math.floor(r * 255), math.floor(g * 255), math.floor(b * 255)

def is_websafe_video(mime):
	if (
			'video/mp4' == mime
			or 'video/mpeg' == mime
			or 'video/webm' == mime
			or 'application/ogg' == mime
			or 'video/ogg' == mime
		):
		return True
	return False

class MediaArchive:
	def __init__(self, config, media, accounts, access_log=None):
		self.config = config
		self.media = media
		self.accounts = accounts
		self.access_log = access_log

		# media archive package required groups
		self.accounts.users.populate_groups()
		if 'contributor' not in self.accounts.users.available_groups:
			self.accounts.users.create_group('contributor')
			self.accounts.users.protect_group('contributor')

		if 'contributor' not in self.accounts.users.available_groups:
			self.accounts.users.create_group('taxonomist')
			self.accounts.users.protect_group('taxonomist')

		self.accounts.users.populate_groups()

		self.callbacks = {}

	def add_callback(self, event, f):
		if event not in self.callbacks:
			self.callbacks[event] = []
		self.callbacks[event].append(f)

	def add_log(self, scope, subject_uuid=None, object_uuid=None):
		if not self.access_log:
			return

		params = {}
		if subject_uuid:
			params['subject_uuid'] = subject_uuid
		if object_uuid:
			params['object_uuid'] = object_uuid

		self.access_log.create_log(
			request.remote_addr,
			scope,
			**params
		)

	def create_temp_medium_file(self, file_contents):
		import uuid
		file_path = os.path.join(self.config['temp_path'], 'temp_medium_' + str(uuid.uuid4()))
		f = open(file_path, 'w+b')
		f.write(file_contents)
		f.close()
		return file_path

	def get_medium_file_path(self, medium):
		if MediumProtection.NONE != medium.protection:
			protection_path = 'protected'
		else:
			protection_path = 'nonprotected'

		file_path = os.path.join(
			self.config['media_path'],
			protection_path,
			medium.id + '.' + mime_to_extension(medium.mime)
		)
		if os.path.exists(file_path):
			return file_path
		return ''

	def export_media(self, filter={}):
		import time
		import json
		import uuid
		import hashlib

		nonce = str(uuid.uuid4())

		media_data = []
		media_files = []
		temp_files = []
		signature_input = ''
		media = self.search_media(filter=filter, sort='upload_time')
		for medium in media:
			medium_filename = medium.id + '.' + mime_to_extension(medium.mime)
			current_data = {
				'md5': str(hashlib.md5(medium.md5).hexdigest()),
				'id': str(medium.id),
				'uploader_remote_origin': str(medium.uploader_remote_origin.exploded),
				'upload_time': int(medium.upload_time.timestamp()),
				'creation_time': int(medium.creation_time.timestamp()),
				'touch_time': int(medium.touch_time.timestamp()),
				'uploader_uuid': str(medium.uploader_uuid),
				'owner_uuid': str(medium.owner_uuid),
				'status': str(medium.status),
				'protection': str(medium.protection),
				'searchability': str(medium.searchability),
				'group_bits': int.from_bytes(medium.group_bits, 'big'),
				'mime': medium.mime,
				'size': medium.size,
				'data1': medium.data1,
				'data2': medium.data2,
				'data3': medium.data3,
				'data4': medium.data4,
				'data5': medium.data5,
				'data6': medium.data6,
				'tags': medium.tags,
				'filename': medium_filename,
				'original_file': False,
			}

			medium_file_path = self.get_medium_file_path(medium)
			if medium_file_path:
				media_files.append((medium_file_path, os.path.join('media', medium_filename)))
				current_data['original_file'] = True

			media_data.append(current_data)

			for key in current_data:
				signature_input += str(current_data[key])

		# generate signature
		signature = md5_to_id(hashlib.md5(signature_input.encode('utf-8')).digest())

		# generate temp data.json
		data_file_path = os.path.join(self.config['temp_path'], 'data_' + nonce + '.json')
		with open(data_file_path, 'w') as f:
			f.write(json.dumps(media_data))
		temp_files.append((data_file_path, 'data.json'))

		# generate temp information file with version/time/requested by uuid/filter
		info_file_path = os.path.join(self.config['temp_path'], 'info_' + nonce + '.json')
		#TODO parse filter to convert non-string and non-numeric values to strings
		with open(info_file_path, 'w') as f:
			f.write(json.dumps({
				'version': '0.0.1',
				'export_time': int(time.time()),
				'requested_by_uuid': str(self.accounts.current_user.uuid),
				#TODO add filter directly to info json
				'filter': str(filter),
				'signature': signature,
			}))
		temp_files.append((info_file_path, 'info.json'))

		# generate temp files from callbacks
		if 'export' in self.callbacks:
			for f in self.callbacks['export']:
				# result of callback must be a tuple of (name, arcname)
				# name will be deleted by this script after being added to the export archive
				temp_files.append(f(media))

		import tarfile

		export_file_path = os.path.join(self.config['temp_path'], 'media.export.' + signature + '.tar.gz')
		if not os.path.exists(export_file_path):
			export_archive = tarfile.open(export_file_path, 'w:gz')

			# add media files
			for name, arcname in media_files:
				export_archive.add(name, arcname)

			# add temp files
			for name, arcname in temp_files:
				export_archive.add(name, arcname)

			export_archive.close()

		# delete temp files
		for name, arcname in temp_files:
			os.remove(name)

		# send export archive
		from flask import send_from_directory

		#TODO delete export after sending
		#TODO maybe send with a generator reading out chunks of the file for large files
		#TODO or leave it like this but set up regular clearing of tmp directory
		r = send_from_directory(
			os.path.join(self.config['temp_path']),
			'media.export.' + signature + '.tar.gz',
			mimetype='application/gzip',
			as_attachment=True,
		)
		return r

	def get_import_archive_info(self, import_archive):
		import json
		import uuid
		from datetime import datetime, timezone

		info_file = import_archive.extractfile('info.json')

		if not info_file:
			abort(400, {'message': 'import_archive_missing_info'})
		try:
			info = json.load(info_file)
		except json.decoder.JSONDecodeError:
			abort(400, {'message': 'malformed_import_archive_info'})

		if -1 != info['signature'].find('..') or '/' == info['signature'][0]:
			abort(400, {'message': 'import_archive_invalid_signature'})

		info['requested_by'] = self.accounts.get_user(uuid.UUID(info['requested_by_uuid']))
		info['export_time'] = datetime.fromtimestamp(info['export_time'], timezone.utc)

		return info

	def get_import_archive_data(self, import_archive):
		import json
		import uuid
		from datetime import datetime, timezone

		data_file = import_archive.extractfile('data.json')
		if not data_file:
			abort(400, {'message': 'import_archive_missing_data'})
		try:
			data = json.load(data_file)
		except json.decoder.JSONDecodeError:
			abort(400, {'message': 'malformed_import_archive_data'})

		# get users for uploaders and owners in data
		user_uuids = []
		for medium in data:
			if -1 != medium['filename'].find('..') or '/' == medium['filename'][0]:
				abort(400, {'message': 'import_archive_invalid_medium_filename'})
			user_uuids.append(uuid.UUID(medium['uploader_uuid']))
			user_uuids.append(uuid.UUID(medium['uploader_uuid']))

		users = self.accounts.users.users_dictionary(
			self.accounts.search_users(filter={'user_uuids': user_uuids})
		)

		md5s = []
		for medium in data:
			medium['md5'] = id_to_md5(medium['id'])
			md5s.append(medium['md5'])
			
		existing_media = self.media.media_dictionary(self.search_media(filter={'md5s': md5s}))

		for medium in data:
			medium['already_exists'] = False
			if medium['md5'] in existing_media:
				medium['already_exists'] = True
				medium['medium'] = existing_media[medium['md5']]
			medium['upload_time'] = datetime.fromtimestamp(medium['upload_time'], timezone.utc)
			medium['creation_time'] = datetime.fromtimestamp(medium['creation_time'], timezone.utc)
			medium['touch_time'] = datetime.fromtimestamp(medium['touch_time'], timezone.utc)

			medium['uploader'] = None
			medium['owner'] = None

			uploader_uuid = uuid.UUID(medium['uploader_uuid'])
			if uploader_uuid in users:
				medium['uploader'] = users[uploader_uuid]

			owner_uuid = uuid.UUID(medium['uploader_uuid'])
			if owner_uuid in users:
				medium['owner'] = users[owner_uuid]

		return data

	def analyze_import_file(self, import_archive_object):
		import tarfile
		import uuid

		#TODO catch exception here for invalid tar gz
		import_archive = tarfile.open(mode='r:gz', fileobj=import_archive_object)
		info = self.get_import_archive_info(import_archive)
		data = self.get_import_archive_data(import_archive)
		
		#TODO check for signature mismatch

		total_media_files = 0
		other_files = []
		for tarinfo in import_archive:
			if -1 != tarinfo.name.find('..'):
				abort(400, {'message': 'import_archive_invalid_path' + tarinfo.name})
			elif 'media/' == tarinfo.name[:6]:
				total_media_files += 1
			elif 'info.json' != tarinfo.name and 'data.json' != tarinfo.name:
				other_file = {
					'name': tarinfo.name,
					'size': tarinfo.size,
				}
				if tarinfo.isreg():
					other_file['type'] = 'regular'
				elif tarinfo.isdir():
					other_file['type'] = 'directory'
				else:
					other_file['type'] = 'other'
				other_files.append(other_file)
		return info, data, other_files

	def import_media(self, import_archive_object, generate_summaries=False):
		import tarfile
		import uuid
		from datetime import datetime, timezone

		from media import Medium

		#TODO catch exception here for invalid tar gz
		import_archive = tarfile.open(mode='r:gz', fileobj=import_archive_object)
		info = self.get_import_archive_info(import_archive)
		data = self.get_import_archive_data(import_archive)

		#TODO check for signature mismatch

		temp_media_directory = os.path.join(
			self.config['temp_path'],
			'import.' + info['signature'] + '.' + str(uuid.uuid4())
		)

		updated_medium_md5s = []
		for medium in data:
			print('importing media ' + medium['id'])
			if medium['original_file']:
				if 'media/' + medium['filename'] not in import_archive.getnames():
					#TODO warning log of original file expected but missing from archive
					continue
			if medium['already_exists']:
				self.remove_medium(medium['medium'])

			current_medium = Medium(
				medium['md5'],
				medium['uploader_remote_origin'],
				medium['upload_time'].timestamp(),
				medium['creation_time'].timestamp(),
				medium['touch_time'].timestamp(),
				uuid.UUID(medium['uploader_uuid']),
				uuid.UUID(medium['owner_uuid']),
				medium['status'],
				medium['protection'],
				medium['searchability'],
				medium['group_bits'],
				medium['mime'],
				medium['size'],
				medium['data1'],
				medium['data2'],
				medium['data3'],
				medium['data4'],
				medium['data5'],
				medium['data6'],
			)
			try:
				self.media.create_medium(
					current_medium.md5,
					current_medium.uploader_remote_origin,
					current_medium.uploader_uuid,
					current_medium.owner_uuid,
					current_medium.mime,
					current_medium.size,
					current_medium.upload_time.timestamp()
				)
			except ValueError:
				pass
			# update
			self.media.update_medium(
				current_medium,
				creation_time=current_medium.creation_time.timestamp(),
				touch_time=current_medium.touch_time.timestamp(),
				status=str(current_medium.status),
				protection=str(current_medium.protection),
				searchability=str(current_medium.searchability),
				group_bits=current_medium.group_bits,
				mime=current_medium.mime,
				size=current_medium.size,
				data1=current_medium.data1,
				data2=current_medium.data2,
				data3=current_medium.data3,
				data4=current_medium.data4,
				data5=current_medium.data5,
				data6=current_medium.data6,
			)
			# set tags
			self.media.remove_tags(current_medium)
			self.media.add_tags(current_medium, medium['tags'])
			if medium['original_file']:
				# extract associated medium file to protected path
				member = import_archive.getmember('media/' + medium['filename'])
				import_archive.extract(member, temp_media_directory)
				os.rename(
					os.path.join(temp_media_directory, 'media', medium['filename']),
					os.path.join(
						self.config['media_path'],
						'protected',
						md5_to_id(current_medium.md5) + '.' + mime_to_extension(current_medium.mime)
					)
				)
				# add to list of medium to re-fetch, place, and generate summaries
				updated_medium_md5s.append(current_medium.md5)

		# remove temp media directory
		import shutil

		shutil.rmtree(temp_media_directory)

		if 'import' in self.callbacks:
			for f in self.callbacks['import']:
				# callbacks to import data related to media (e.g. comments, sticker placements)
				f(import_archive, info, data)

		import_archive.close()

		if updated_medium_md5s:
			media = self.search_media(filter={'md5s': updated_medium_md5s})
			for medium in media:
				self.place_medium_file(medium)
				if generate_summaries:
					self.generate_medium_summaries(medium)

	def populate_uris(self, medium):
		if self.config['api_uri']:
			fetch_uri = self.config['api_uri'].format('fetch/{}')
		else:
			fetch_uri = url_for(
				'media_archive.api_fetch_medium',
				medium_filename='MEDIUM_FILENAME'
			).replace('MEDIUM_FILENAME', '{}')

		if not self.config['medium_file_uri']:
			self.config['medium_file_uri'] = url_for(
				'media_archive.medium_file',
				medium_filename='MEDIUM_FILENAME'
			).replace('MEDIUM_FILENAME', '{}')

		if MediumProtection.NONE != medium.protection:
			protection_path = 'protected'
			media_uri = fetch_uri
		else:
			protection_path = 'nonprotected'
			media_uri = self.config['medium_file_uri']

		medium.uris = {
			'original': '',
			'static': {},
			'fallback': {},
			'reencoded': {},
		}

		medium_file = medium.id + '.' + mime_to_extension(medium.mime)
		if os.path.exists(os.path.join(self.config['media_path'], protection_path, medium_file)):
			medium.uris['original'] = media_uri.format(medium_file)

		summary_path = os.path.join(self.config['summaries_path'], protection_path)
		for edge in self.config['summary_edges']:
			summary_file = medium.id + '.' + str(edge)
			if 'image' == medium.category:
				if os.path.exists(os.path.join(summary_path, summary_file + '.webp')):
					medium.uris['static'][edge] = media_uri.format(summary_file + '.webp')
				if os.path.exists(os.path.join(summary_path, summary_file + '.png')):
					medium.uris['fallback'][edge] = media_uri.format(summary_file + '.png')
				if (
						'image/gif' == medium.mime
						and 1 < medium.data4
						and os.path.exists(os.path.join(summary_path, summary_file + '.gif'))
					):
					medium.uris['reencoded'][edge] = media_uri.format(summary_file + '.gif')
			elif 'video' == medium.category:
				if os.path.exists(os.path.join(summary_path, summary_file + '.png')):
					medium.uris['static'][edge] = media_uri.format(summary_file + '.png')
				if os.path.exists(os.path.join(summary_path, summary_file + '.png')):
					medium.uris['fallback'][edge] = media_uri.format(summary_file + '.webp')

			elif medium.category in ['audio', 'archive']:
				if os.path.exists(os.path.join(summary_path, summary_file + '.webp')):
					medium.uris['static'][edge] = media_uri.format(summary_file + '.webp')
				if os.path.exists(os.path.join(summary_path, summary_file + '.png')):
					medium.uris['fallback'][edge] = media_uri.format(summary_file + '.png')
		if 'video' == medium.category:
			if os.path.exists(os.path.join(summary_path,  medium.id + '.clip.webm')):
				medium.uris['reencoded']['clip'] = media_uri.format(medium.id + '.clip.webm')
			if os.path.exists(os.path.join(summary_path,  medium.id + '.slideshow.webp')):
				medium.uris['static']['slideshow'] = media_uri.format(medium.id + '.slideshow.webp')
			if os.path.exists(os.path.join(summary_path,  medium.id + '.slideshow.png')):
				medium.uris['fallback']['slideshow'] = media_uri.format(medium.id + '.slideshow.png')
			if (
					not is_websafe_video(medium.mime)
					and os.path.exists(os.path.join(summary_path, medium.id + '.reencoded.webm'))
				):
				medium.uris['reencoded']['original'] = media_uri.format(medium.id + '.reencoded.webm')

	def populate_groups(self, medium):
		medium.groups = []
		for group in self.config['requirable_groups']:
			group_bit = self.accounts.users.group_name_to_bit(group)
			if self.accounts.users.contains_all_group_bits(medium.group_bits, group_bit):
				medium.groups.append(group)

	def populate_medium_properties(self, medium):
		populate_id(medium)
		populate_category(medium)
		self.populate_uris(medium)
		self.populate_groups(medium)
		medium.uploader_id = uuid_to_id(medium.uploader_uuid)
		medium.owner_id = uuid_to_id(medium.owner_uuid)
		if medium.category in ['image', 'video'] and medium.data3:
			r, g, b = hsv_int_to_rgb(medium.data3)
			medium.rgb = {
				'r': r,
				'g': g,
				'b': b,
			}

	def get_medium(self, medium_md5):
		medium = self.media.get_medium(medium_md5)
		if medium:
			self.populate_medium_properties(medium)
			self.media.populate_medium_tags(medium)
		return medium

	def search_media(self, **kwargs):
		if 'filter' in kwargs and 'ids' in kwargs['filter']:
			if 'md5s' not in kwargs['filter']:
				kwargs['filter']['md5s'] = []
			for id in kwargs['filter']['ids']:
				kwargs['filter']['md5s'].append(id_to_md5(id))
			del kwargs['filter']['ids']
		media = self.media.search_media(**kwargs)
		for medium in media:
			self.populate_medium_properties(medium)
		media_dictionary = self.media.media_dictionary(media)
		self.media.populate_media_tags(media_dictionary)
		return media

	def get_adjacent_media(self, medium, filter={}, sort=''):
		prev_medium, next_medium = self.media.get_adjacent_media(medium, filter, sort)

		prev_medium_id = ''
		next_medium_id = ''

		if prev_medium:
			self.populate_medium_properties(prev_medium)
			prev_medium_id = prev_medium.id

		if next_medium:
			self.populate_medium_properties(next_medium)
			next_medium_id = next_medium.id

		return prev_medium_id, next_medium_id

	def require_medium(self, medium_md5):
		medium = self.get_medium(medium_md5)
		if not medium:
			abort(404, {'message': 'medium_not_found'})
		return medium

	def encode_tag(self, tag):
		for needle, replacement in self.config['tag_encode_replacements']:
			tag = tag.replace(needle, replacement)

		return tag

	def place_medium_file(self, medium, source_file_path=None):
		medium_file = medium.id + '.' + mime_to_extension(medium.mime)

		protected_path = os.path.join(self.config['media_path'], 'protected')
		nonprotected_path = os.path.join(self.config['media_path'], 'nonprotected')

		if MediumProtection.NONE != medium.protection:
			source_path = nonprotected_path
			destination_path = protected_path
		else:
			source_path = protected_path
			destination_path = nonprotected_path

		if source_file_path:
			source = source_file_path
		else:
			source = os.path.join(source_path, medium_file)

		if os.path.exists(source):
			os.rename(
				source,
				os.path.join(destination_path, medium_file)
			)

	def remove_medium_file(self, medium):
		medium_file = medium.id + '.' + mime_to_extension(medium.mime)

		for protection_path in ['protected', 'nonprotected']:
			file_path = os.path.join(self.config['media_path'], protection_path, medium_file)
			if os.path.exists(file_path):
				os.remove(file_path)

	def iterate_medium_summaries(self, medium, cb):
		for protection_path in ['protected', 'nonprotected']:
			for edge in self.config['summary_edges']:
				summary_path = os.path.join(
					self.config['summaries_path'],
					protection_path
				)
				summary_file_template = medium.id + '.' + str(edge) + '.'

				extensions = []
				if 'image' == medium.category:
					# static, fallback, reencode
					extensions = ['webp', 'png', 'gif']
				elif 'video' == medium.category:
					# static, fallback
					extensions = ['webp', 'png']
				elif medium.category in ['audio', 'archive']:
					# static, fallback
					extensions = ['webp', 'png']
					
				for extension in extensions:
					summary_file =  summary_file_template + extension
					if os.path.exists(os.path.join(summary_path, summary_file)):
						cb(summary_path, summary_file)
			if 'video' == medium.category:
				# clip
				extensions.append('clip.webm')
				# slideshow strips
				extensions = ['slideshow.webp', 'slideshow.png']
				# reencode
				if not is_websafe_video(medium.mime):
					extensions.append('reencoded.webm')
				for extension in extensions:
					summary_file = medium.id + '.' + extension
					if os.path.exists(os.path.join(summary_path, summary_file)):
						cb(summary_path, summary_file)

	def place_medium_summaries(self, medium):
		protected_path = os.path.join(self.config['summaries_path'], 'protected')
		nonprotected_path = os.path.join(self.config['summaries_path'], 'nonprotected')

		if MediumProtection.NONE != medium.protection:
			source_path = nonprotected_path
			destination_path = protected_path
		else:
			source_path = protected_path
			destination_path = nonprotected_path

		self.iterate_medium_summaries(
			medium,
			lambda summary_path, summary_file: (
				os.rename(
					os.path.join(summary_path, summary_file),
					os.path.join(destination_path, summary_file)
				)
			)
		)

	def remove_medium_summaries(self, medium):
		self.iterate_medium_summaries(
			medium,
			lambda summary_path, summary_file: (
				os.remove(os.path.join(summary_path, summary_file))
			)
		)

	def summaries_from_image(self, image, summary_path):
		from PIL import Image

		for edge in self.config['summary_edges']:
			thumbnail = image.copy()
			thumbnail.thumbnail((edge, edge), Image.BICUBIC)

			# static
			thumbnail_path = summary_path.format(str(edge) + '.webp')
			thumbnail.save(thumbnail_path, 'WebP', lossless=True)

			# fallback
			thumbnail_path = summary_path.format(str(edge) + '.png')
			thumbnail.save(thumbnail_path, 'PNG', optimize=True)

	def generate_video_snapshots(self, file_path, duration_s):
		import uuid
		import math
		import subprocess

		from PIL import Image

		# space the snapshot intervals out with the intention to skip first and last
		interval_s = math.floor(duration_s) / (self.config['video_snapshots'] + 2)

		snapshots = []
		for i in range(1, self.config['video_snapshots']):
			snapshot_path = os.path.join(self.config['temp_path'], 'temp_snapshot_' + str(uuid.uuid4()) + '.png')

			ffmpeg_call = [
				self.config['ffmpeg_path'],
				'-i',
				file_path,
				'-ss',
				str(i * interval_s),
				'-frames:v',
				'1',
			]
			if (
					self.config['ffmpeg_thread_limit']
					and isinstance(self.config['ffmpeg_thread_limit'], int)
					and 0 < self.config['ffmpeg_thread_limit']
				):
				ffmpeg_call += [
					'-threads',
					str(self.config['ffmpeg_thread_limit']),
				]
			ffmpeg_call += [
				snapshot_path,
			]
			subprocess.run(ffmpeg_call)

			snapshot = Image.open(snapshot_path)
			snapshots.append((snapshot_path, snapshot))

			if 1 == i:
				#TODO for now only generate the one static summary, do slideshow later
				break
		return snapshots

	def reencode_video(
			self,
			file_path,
			output_path,
			width,
			height,
			edge,
			start_ms=0,
			end_ms=0,
			muted=False
		):
		import subprocess

		if (
				0 > edge
				or not width
				or not height
			):
			return

		# using libvpx instead of libx264, so maybe the divisible by 2 requirement isn't needed?
		if width < height:
			resize_width = -1
			resize_height = edge
		else:
			resize_width = edge
			resize_height = -1

		ffmpeg_call = [
			self.config['ffmpeg_path'],
		]
		if (
				0 < end_ms
				and start_ms < end_ms
			):
			start_s = start_ms / 1000
			end_s = end_ms / 1000
			ffmpeg_call += [
				'-ss',
				str(start_s),
				'-i',
				file_path,
				'-t',
				str(end_s - start_s)
				#'-ss',
				#str(end_s),
			]
		else:
			ffmpeg_call += [
				'-i',
				file_path,
			]
		ffmpeg_call += [
			'-vcodec',
			'libvpx',
			'-quality',
			'good',
			'-cpu-used',
			'5',
			'-vf',
			'scale=' + str(resize_width) + ':' + str(resize_height),
			'-y',
		]
		if muted:
			ffmpeg_call += [
				'-an'
			]
		if (
				self.config['ffmpeg_thread_limit']
				and isinstance(self.config['ffmpeg_thread_limit'], int)
				and 0 < self.config['ffmpeg_thread_limit']
			):
			ffmpeg_call += [
				'-threads',
				str(self.config['ffmpeg_thread_limit']),
			]
		ffmpeg_call += [
			output_path,
		]
		subprocess.run(ffmpeg_call)

	def get_video_info(self, file_path):
		import subprocess
		import json

		width = 0
		height = 0
		duration_s = 0
		audio_codec = ''
		video_codec = ''

		probe_json = subprocess.getoutput([
			self.config['ffprobe_path'],
			'-v',
			'quiet',
			'-print_format',
			'json',
			'-show_streams',
			'-i',
			file_path,
		])
		probe = json.loads(probe_json)

		if 'streams' in probe:
			for stream in probe['streams']:
				for key, value in stream.items():
					if 'width' == key or 'coded_width' == key:
						width = int(value)
					elif 'height' == key or 'coded_height' == key:
						height = int(value)
					elif 'duration' == key:
						duration_s = float(value)
			if (
					'codec_type' in stream
					and 'codec_name' in stream
				):
				codec_name = stream['codec_name']
				if 'audio' == stream['codec_type']:
					audio_codec = codec_name
				elif 'video' == stream['codec_type']:
					video_codec = codec_name

		# missing duration after streams probe, do packets probe
		if not duration_s:
			probe_json = subprocess.getoutput([
				self.config['ffprobe_path'],
				'-v',
				'quiet',
				'-print_format',
				'json',
				'-show_packets',
				'-i',
				file_path,
			])
			probe = json.loads(probe_json)

			last_frame = probe['packets'].pop()
			if 'dts_time' in last_frame:
				duration_s = float(last_frame['dts_time'])
			elif 'pts_time' in last_frame:
				duration_s = float(last_frame['pts_time'])

		# still missing duration after packets probe
		if not duration_s:
			#TODO attempt to estimate duration by seeking last keyframe from end
			# and doing some math based on frame length
			#try:
			#	fh = fopen(file_path, 'rb')
			#	fseek(fh, -4, SEEK_END)
			#	r = unpack('N', fread(fh, 4))
			#	last_tag_offset = r[1]
			#	fseek(fh, -(last_tag_offset + 4), SEEK_END)
			#	fseek(fh, 4, SEEK_CUR)
			#	t0 = fread(fh, 3)
			#	t1 = fread(fh, 1)
			#	r = unpack('N', t1 . t0)
			#	duration_ms = r[1]
			#	duration_s = duration_ms / 1000
			pass

		return width, height, duration_s, audio_codec, video_codec

	def generate_medium_summaries(self, medium):
		self.remove_medium_summaries(medium)

		protection_path = 'nonprotected'
		if MediumProtection.NONE != medium.protection:
			protection_path = 'protected'

		file_path = os.path.join(
			self.config['media_path'],
			protection_path,
			medium.id + '.' + mime_to_extension(medium.mime)
		)
		summary_path = os.path.join(
			self.config['summaries_path'],
			protection_path,
			medium.id + '.{}'
		)

		if not os.path.exists(file_path):
			abort(500, {'message': 'original_file_not_found'})

		updates = {}
		if 'image' == medium.category:
			from PIL import Image

			img = Image.open(file_path)
			self.summaries_from_image(img, summary_path)

			updates['data1'] = img.width
			updates['data2'] = img.height
			updates['data3'] = hsv_to_int(*hsv_average_from_image(img))

			if 'image/gif' == medium.mime:
				frames = 1
				try:
					while True:
						img.seek(img.tell() + 1)
						frames += 1
				except EOFError:
					pass
				if 1 < frames:
					updates['data4'] = frames
					if self.config['ffmpeg_path']:
						import subprocess

						portrait = (img.width < img.height)
						for edge in self.config['summary_edges']:
							if portrait:
								width = -1
								height = min(edge, img.height)
							else:
								width = min(edge, img.width)
								height = -1

							ffmpeg_call = [
								self.config['ffmpeg_path'],
								'-i',
								file_path,
								'-vf',
								'scale=' + str(width) + ':' + str(height),
							]
							if (
									self.config['ffmpeg_thread_limit']
									and isinstance(self.config['ffmpeg_thread_limit'], int)
									and 0 < self.config['ffmpeg_thread_limit']
								):
								ffmpeg_call += [
									'-threads',
									str(self.config['ffmpeg_thread_limit']),
								]
							ffmpeg_call += [
								summary_path.format(str(edge) + '.gif'),
							]
							subprocess.run(ffmpeg_call)
		elif 'video' == medium.category:
			if self.config['ffprobe_path'] and self.config['ffmpeg_path']:
				width, height, duration_s, audio_codec, video_codec = self.get_video_info(file_path)

				if duration_s:
					import math

					# duration ms
					duration_ms = int(math.floor(duration_s * 1000))
					updates['data5'] = duration_ms

					snapshots = self.generate_video_snapshots(file_path, duration_s)

					# use snapshot dimensions if dimensions are missing
					first_snapshot_path, first_snapshot = snapshots[0]
					if not width:
						width = first_snapshot.width
					if not height:
						height = first_snapshot.height

					# static summaries from first snapshot
					self.summaries_from_image(first_snapshot, summary_path)
					updates['data3'] = hsv_to_int(*hsv_average_from_image(first_snapshot))

					#TODO create slideshow strip from snapshots
					#for path, snapshot in snapshots
						#snapshot.thumbnail(self.config['video_slideshow_edge'])
					#TODO save slideshow strip with .slideshow.webp and .slideshow.png
					#TODO remove snapshots
					for snapshot_path, snapshot in snapshots:
						snapshot.close()
						os.remove(snapshot_path)

					if 0 < self.config['video_clip_duration_ms']:
						if duration_ms <= self.config['video_clip_duration_ms']:
							start_ms = 0
							end_ms = duration_ms
						else:
							midpoint_ms = duration_ms / 2
							half_video_clip_duration_ms = self.config['video_clip_duration_ms'] / 2
							start_ms = midpoint_ms - half_video_clip_duration_ms
							end_ms = start_ms + self.config['video_clip_duration_ms']
						self.reencode_video(
							file_path,
							summary_path.format('clip.webm'),
							width,
							height,
							self.config['video_clip_edge'],
							start_ms=start_ms,
							end_ms=end_ms,
							muted=True
						)
				# reencode non-websafe video for the view page
				if not is_websafe_video(medium.mime):
					self.reencode_video(
						file_path,
						summary_path.format('reencoded.webm'),
						width,
						height,
						self.config['video_reencode_edge']
					)
				if width:
					updates['data1'] = width
				if height:
					updates['data2'] = height
				tags = []
				if audio_codec:
					tags.append('audio codec:' + audio_codec)
				if video_codec:
					tags.append('video codec:' + video_codec)
				if 0 < len(tags):
					#TODO auto-add tags
					pass

		elif 'audio':
			if 'audio/mpeg' == medium.mime:
				#TODO get id3 info for mp3
				#TODO add #title:, #tracknum:, #album:, and #author: based on id3?

				#TODO if id3 cover image is present then get image resource from it
				if False:
					from PIL import Image

					#img = Image.open(cover_path)
					#self.summaries_from_image(img)
					#os.remove(cover_path)
					pass
			else:
				#TODO nothing for other audio types yet
				pass
		elif 'application':
			if 'application/x-shockwave-flash' == medium.mime:
				#TODO parse flash headers, maybe hexagonit-swfheader, or implementing from scratch
				if False:
					header = {
						'width': 0,
						'height': 0,
						'frames': 0,
						'fps': 0,
						'version': 0,
					}
					updates['data1'] = header['width']
					updates['data2'] = header['height']
					updates['data4'] = header['frames']
					updates['data5'] = header['fps']
					updates['data6'] = header['version']
		elif 'archive':
			#TODO no archive summary yet
			#TODO check for cbr/cbz and get cover summary
			#TODO check for smgez and get cover summary
			pass
		if 0 < len(updates):
			self.media.update_medium(medium, **updates)

	def multiupload(self):
		#TODO do groups/properties/tag processing once
		#TODO loop through uploads and apply processed groups/properties/tags to each
		pass

	def tag_string_to_list(self, tag_string):
		return tag_string.split('#')

	def parse_search_tags(self, tags=[], manage=False):
		groups = []
		without_groups = []
		filter = {}
		for tag in tags:
			if not tag or ('-' == tag[0] and 2 > len(tag)):
				continue

			# pagination
			if 'sort:' == tag[:5]:
				sort = tag[5:]
				if 'color' == sort:
					sort = 'data3'
				elif 'creation' == sort:
					sort = 'creation_time'
				elif 'upload' == sort:
					sort = 'upload_time'
				elif 'modify' == sort:
					sort = 'touch_time'
				filter['sort'] = sort
			elif 'order:' == tag[:6]:
				if 'desc' != tag[6:]:
					filter['order'] = 'asc'
			elif 'perpage:' == tag[:8]:
				perpage = tag[8:]
				try:
					filter['perpage'] = int(perpage)
				except ValueError:
					pass
			# properties
			elif 'group:' == tag[:6]:
				groups.append(tag[6:])
			elif '-group:' == tag[:7]:
				without_groups.append(tag[7:])
			elif 'uploaded after:' == tag[:15]:
				import dateutil.parser
				try:
					uploaded_after = dateutil.parser.parse(tag[15:]).timestamp()
				except ValueError:
					pass
				else:
					if 'uploaded_afters' not in filter:
						filter['uploaded_afters'] = []
					filter['uploaded_befores'].append(uploaded_before)
			elif 'uploaded before:' == tag[:16]:
				import dateutil.parser
				try:
					uploaded_before = dateutil.parser.parse(tag[16:]).timestamp()
				except ValueError:
					pass
				else:
					if 'uploaded_befores' not in filter:
						filter['uploaded_befores'] = []
					filter['uploaded_befores'].append(uploaded_before)
			elif 'created after:' == tag[:14]:
				import dateutil.parser
				try:
					created_after = dateutil.parser.parse(tag[14:]).timestamp()
				except ValueError:
					pass
				else:
					if 'created_afters' not in filter:
						filter['created_afters'] = []
					filter['created_afters'].append(created_after)
			elif 'created before:' == tag[:15]:
				import dateutil.parser
				try:
					created_before = dateutil.parser.parse(tag[15:]).timestamp()
				except ValueError:
					pass
				else:
					if 'created_befores' not in filter:
						filter['created_befores'] = []
					filter['created_befores'].append(created_before)
			elif 'modified after:' == tag[:15]:
				import dateutil.parser
				try:
					modified_after = dateutil.parser.parse(tag[15:]).timestamp()
				except ValueError:
					pass
				else:
					if 'touched_afters' not in filter:
						filter['touched_afters'] = []
					filter['touched_afters'].append(modified_after)
			elif 'modified before:' == tag[:16]:
				import dateutil.parser
				try:
					modified_before = dateutil.parser.parse(tag[16:]).timestamp()
				except ValueError:
					pass
				else:
					if 'touched_befores' not in filter:
						filter['touched_befores'] = []
					filter['touched_befores'].append(modified_before)
			elif 'mimetype:' == tag[:9]:
				filter['mime'] = tag[9:]
			elif '-mimetype:' == tag[:10]:
				if 'without_mimes' not in filter:
					filter['without_mimes'] = []
				filter['without_mimes'].append(tag[10:])
			elif 'smaller than:' == tag[:13]:
				filter['smaller_than'] = tag[13:]
			elif 'larger than:' == tag[:12]:
				filter['larger_than'] = tag[12:]
			elif 'data' == tag[:4]:
				for i in range(1, 7):
					data = 'data' + str(i)
					if data + ' less than:' == tag[:16]:
						filter[data + '_less_than'] = tag[:16]
					if data + ' more than:' == tag[:16]:
						filter[data + '_more_than'] = tag[:16]
			elif 'protection:' == tag[:11]:
				filter['protection'] = tag[11:].upper()
			elif '-protection:' == tag[:12]:
				if 'without_protections' not in filter:
					filter['without_protections'] = []
				filter['without_protections'].append(tag[12:].upper())
			elif 'searchability:' == tag[:14]:
				filter['searchability'] = tag[14:].upper()
			elif '-searchability:' == tag[:15]:
				if 'without_searchabilities' not in filter:
					filter['without_searchabilities'] = []
				filter['without_searchabilities'].append(tag[15:].upper())
			# management tags
			elif 'id:' == tag[:3] and manage:
				if 'md5s' not in filter:
					filter['md5s'] = []
				filter['md5s'].append(id_to_md5(tag[3:]))
			elif 'origin:' == tag[:7] and manage:
				if 'uploader_remote_origins' not in filter:
					filter['uploader_remote_origins'] = []
				filter['uploader_remote_origins'].append(tag[7:])
			elif 'uploader:' == tag[:9] and manage:
				if not 'uploader_uuids' in filter:
					filter['uploader_uuids'] = []
				filter['uploader_uuids'].append(id_to_uuid(tag[9:]))
			elif 'owner:' == tag[:6] and manage:
				if not 'owner_uuids' in filter:
					filter['owner_uuids'] = []
				filter['owner_uuids'].append(id_to_uuid(tag[6:]))
			elif 'status:' == tag[:7] and manage:
				filter['status'] = tag[7:].upper()
			elif '-status:' == tag[:8] and manage:
				if 'without_statuses' not in filter:
					filter['without_statuses'] = []
				filter['without_statuses'].append(tag[8:].upper())
			#TODO without tags like escaping
			#elif '-~' == tag[:2] and 2 < len(tag):
			#	if 'without_tags_like' not in filter:
			#		filter['without_tags_like'] = []
			#	filter['without_tags_like'].append(tag[2:])
			elif '-' == tag[:1]:
				if 'without_tags' not in filter:
					filter['without_tags'] = []
				filter['without_tags'].append(tag[1:])
			#TODO with tags like escaping
			#elif '~' == tag[:1] and 1 < len(tag):
			#	if 'with_tags_like' not in filter:
			#		filter['with_tags_like'] = []
			#	filter['with_tags_like'].append(tag[1:])
			else:
				if 'with_tags' not in filter:
					filter['with_tags'] = []
				filter['with_tags'].append(tag)

		if groups:
			filter['with_group_bits'] = self.accounts.users.combine_groups(names=groups)
		if without_groups:
			filter['without_group_bits'] = self.accounts.users.combine_groups(names=without_groups)

		return filter

	def remove_medium(self, medium):
		if 'remove_medium' in self.callbacks:
			for f in self.callbacks['remove_medium']:
				f(medium)
		self.remove_medium_file(medium)
		self.remove_medium_summaries(medium)
		self.media.remove_tags(medium)
		self.media.remove_medium(medium)

	def get_slideshow(self, medium):
		slideshow = None

		if 'tags' not in request.args or not request.args['tags']:
			return slideshow

		slideshow_tags = self.tag_string_to_list(request.args['tags'])
		#TODO get slideshow adjacent using specified medium and tags
		slideshow_next = None
		slideshow_prev = None
		slideshow = {
			'tags': slideshow_tags,
			'prev': slideshow_prev,
			'next': slideshow_next,
		}
		return slideshow

	def get_tag_suggestion_lists(self, manage=False, search=False):
		tag_suggestion_lists = []
		if not self.config['tags_uri']:
			self.config['tags_uri'] = url_for(
				'media_archive.tags_file',
				tags_filename='TAGS_FILENAME'
			).replace('TAGS_FILENAME', '{}')
		tag_suggestion_lists.append(self.config['tags_uri'].format('public.json'))
		#if self.accounts.current_user:
		#	tag_suggestion_lists.append(self.config['tags_uri'].format('signed_in.json'))
		#	if manage:
		#		tag_suggestion_lists.append(self.config['tags_uri'].format('manage.json'))
		if search:
			tag_suggestion_lists.append(self.config['tags_uri'].format('search.json'))
		return tag_suggestion_lists

	def build_tag_suggestion_lists(self):
		import json

		#TODO this seems like it's going to end up heavier than persephone's build tag lists
		#TODO maybe add some lighter tag and mimetype retrieval methods to the media module

		suggestions = []
		for group in self.config['requirable_groups']:
			suggestions.append('group:' + group)
		for searchability in MediumSearchability:
			suggestions.append('searchability:' + str(searchability).lower())
		for protection in MediumProtection:
			suggestions.append('protection:' + str(protection).lower())
		mimes = self.media.get_mimes()
		for mime in mimes:
			suggestions.append('mimetype:' + mime)
		suggestions.append('sort:creation');
		suggestions.append('sort:upload');
		suggestions.append('sort:color');
		suggestions.append('sort:random');

		f = open(os.path.join(self.config['tags_path'], 'search.json'), 'w')
		f.write(json.dumps(suggestions))
		f.close()

		#TODO more granular lists
		#TODO public with tags from searchability:public and protection:none
		#TODO signed_in with tags from searchability:groups and protection:groups
		#TODO manage with tags from searchability:hidden and protection:private

		suggestions = []
		tags = self.media.search_tags(group=True)
		for tag in tags:
			suggestions.append(tag.tag)

		f = open(os.path.join(self.config['tags_path'], 'public.json'), 'w')
		f.write(json.dumps(suggestions))
		f.close()

	def contains_premium_group(self, haystack_group_bits):
		premium_groups = []
		for premium_group in self.config['premium_groups']:
			premium_group_bit = self.accounts.users.group_name_to_bit(premium_group)
			if self.accounts.users.contains_all_group_bits(
					haystack_group_bits,
					premium_group_bit
				):
				if not self.accounts.has_global_group(
						self.accounts.current_user,
						premium_group
					):
					premium_groups.append(premium_group)
		return premium_groups

	def require_access(self, medium, require_groups=False):
		signed_in = False
		owner = False
		manager = False

		if self.accounts.current_user:
			signed_in = True
			if medium.owner_uuid == self.accounts.current_user.uuid:
				owner = True
			if self.accounts.current_user_has_global_group('manager'):
				manager = True

		if not manager:
			if MediumStatus.ALLOWED != medium.status:
				abort(451, {'message': 'unavailable'})
			if not owner:
				if MediumProtection.PRIVATE == medium.protection:
					abort(404, {'message': 'medium_not_found'})
				protected = False
				if MediumProtection.NONE == medium.protection:
					if require_groups and 0 < int.from_bytes(medium.group_bits, 'big'):
						if not signed_in:
							abort(401, {'message': 'medium_protected'})
						if not self.accounts.current_user_has_permissions(
								medium.group_bits,
								'global'
							):
							protected = True
					return
				if not signed_in:
					abort(401, {'message': 'medium_protected'})
				if MediumProtection.GROUPS == medium.protection:
					if not self.accounts.current_user_has_permissions(
							'global',
							medium.group_bits
						):
						protected = True
				if protected:
					premium_groups = self.contains_premium_groups(medium.group_bits)
					if premium_groups:
						abort(402, {'message': 'premium_medium', 'groups': premium_groups})
					abort(403, {'message': 'protected_medium'})

	def upload_from_request(self):
		errors = []
		file_contents = None
		filename = ''
		if 'file_uri' in request.form and request.form['file_uri']:
			import urllib
			try:
				response = urllib.request.urlopen(request.form['file_uri'])
			except urllib.error.HTTPError as e:
				errors.append('remote_file_request_http_error')
			except urllib.error.URLError as e:
				errors.append('remote_file_request_url_error')
			else:
				if not response:
					errors.append('remote_file_request_empty_response')
				else:
					file_contents = response.read()
					filename = request.form['file_uri'].replace('\\', '/').split('/').pop()
		elif 'file_upload' in request.files:
			try:
				file_contents = request.files['file_upload'].stream.read()
			except ValueError as e:
				errors.append('problem_uploading_file')
			else:
				filename = request.files['file_upload'].filename
		elif 'local' in request.form:
			#TODO local file
			#request.form['local']
			pass
		else:
			errors.append('missing_file')

		if 0 < len(errors):
			return errors, None

		file_path = self.create_temp_medium_file(file_contents)
		size = get_file_size(file_path)
		mime = get_file_mime(file_path)

		if self.config['maximum_upload_filesize'] < size:
			errors.append('greater_than_maximum_upload_filesize')
		if mime in self.config['disallowed_mimes']:
			errors.append('mimetype_not_allowed')

		if 0 < len(errors):
			if os.path.exists(file_path):
				os.remove(file_path)
			return errors, None

		md5 = get_file_md5(file_path)
		uploader_remote_origin = request.remote_addr
		uploader_uuid = self.accounts.current_user.uuid
		owner_uuid = self.accounts.current_user.uuid
		# manager can set medium owner directly
		if self.accounts.has_global_group(self.accounts.current_user, 'manager'):
			if 'owner_id' in request.form:
				owner = self.accounts.get_user(id_to_uuid(request.form['owner_id']))
				if not owner:
					errors.append('owner_not_found')
					return errors, None
				#TODO only allow contributors to be assigned as owner?
				#self.accounts.users.populate_user_permissions(owner)
				#if not self.accounts.users.has_global_group(owner, 'contributor'):
					#TODO warning for owner not set
				#else:
				owner_uuid = owner.uuid

		try:
			medium = self.media.create_medium(md5, uploader_remote_origin, uploader_uuid, owner_uuid, mime, size)
		except ValueError as e:
			if os.path.exists(file_path):
				os.remove(file_path)

			medium = e.args[0]
			populate_id(medium)
			if MediumStatus.COPYRIGHT == medium.status:
				errors.append('medium_copyright')
			elif MediumStatus.FORBIDDEN == medium.status:
				errors.append('medium_forbidden')
			else:
				errors.append('medium_already_exists')
			return errors, medium

		updates = {}
			
		if 'searchability' in request.form:
			#TODO add exception handling here for ValueErrors
			updates['searchability'] = request.form['searchability'].upper()

		if 'protection' in request.form:
			#TODO add exception handling here for ValueErrors
			updates['protection'] = request.form['protection'].upper()

		if 'creation_date' in request.form:
			import dateutil.parser
			try:
				updates['creation_time'] = dateutil.parser.parse(request.form['creation_date']).timestamp()
			except ValueError:
				#TODO warning for creation time not set
				pass

		groups = []
		for group in self.accounts.users.available_groups:
			field = 'groups[' + group + ']'
			if field in request.form:
				groups.append(group)
		if 0 < len(groups):
			updates['group_bits'] = int.from_bytes(
				self.accounts.users.combine_groups(names=groups),
				'big'
			)

		if 0 < len(updates):
			self.media.update_medium(medium, **updates)

		tags = []
		if 'author_tag' in request.form:
			if self.accounts.current_user.display:
				tags.append('author:' + self.accounts.current_user.display)

		if 'filename_tag' in request.form and filename:
			tags.append('filename:' + filename)

		if 'tags' in request.form:
			tags += self.tag_string_to_list(request.form['tags'])

		if 0 < len(tags):
			self.media.add_tags(medium, tags)

		# update medium from db after alterations
		medium = self.get_medium(medium.md5)

		if 0 < len(errors):
			if os.path.exists(file_path):
				os.remove(file_path)
			return errors, medium

		self.place_medium_file(medium, file_path)
		if 'generate_summaries' in request.form:
			self.generate_medium_summaries(medium)

		return errors, medium

	def get_contributors(self):
		contributors = []
		contributor_bit = self.accounts.users.group_name_to_bit('contributor')
		permissions = self.accounts.search_permissions(filter={
			'permissions': {
				'global': contributor_bit,
				'media': contributor_bit,
			}
		})
		for permission in permissions:
			contributors.append(permission.user)
		return contributors

	def populate_media_covers(self, media):
		if not isinstance(media, list):
			media = [media]
		cover_medium_ids = []
		media_with_covers = []
		for medium in media:
			medium.cover = None
			for tag in medium.tags:
				if 'cover:' == tag[:6]:
					medium.cover_id = tag[6:]
					cover_medium_ids.append(medium.cover_id)
					media_with_covers.append(medium)
				else:
					continue

		if not cover_medium_ids:
			return

		cover_media = self.media.media_dictionary(self.search_media(filter={'ids': cover_medium_ids}))
		for medium in media_with_covers:
			medium.cover = cover_media[id_to_md5(medium.cover_id)]

	def get_api_uris(self):
		api_uris = {}
		if self.config['api_uri']:
			api_uris['upload'] = self.config['api_uri'].format('media/upload')
			api_uris['edit'] = self.config['api_uri'].format('media/edit')
			api_uris['remove'] = self.config['api_uri'].format('media/edit')
			api_uris['build'] = self.config['api_uri'].format('media/edit')
			api_uris['generate_set'] = self.config['api_uri'].format('media/set')
			api_uris['add_tags'] = self.config['api_uri'].format('tags/add')
			api_uris['remove_tags'] = self.config['api_uri'].format('tags/remove')
		else:
			api_uris['upload'] = url_for('media_archive.api_upload_medium')
			api_uris['edit'] = url_for('media_archive.api_edit_medium')
			api_uris['remove'] = url_for('media_archive.api_remove_medium')
			api_uris['build'] = url_for('media_archive.api_build_medium')
			api_uris['generate_set'] = url_for('media_archive.api_generate_set')
			api_uris['add_tags'] = url_for('media_archive.api_add_tags')
			api_uris['remove_tags'] = url_for('media_archive.api_remove_tags')
		return api_uris

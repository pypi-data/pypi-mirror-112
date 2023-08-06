#-*-coding:utf-8 -*-
from DodayUtils._dwrappers import *
import requests
import urllib.parse
import datetime
# from Cryptodome.Hash import SHA256, HMAC
# from base64 import b64decode, b64encode
from gadgethiServerUtils.authentication import *

class DodayHttpClient:
	"""
	This is the http client
	class. 
	"""
	def __init__(self, **configs):
		for key in configs:
			if "_http_url" in key:
				setattr(self, key, configs[key])

	def __getitem__(self, key):
		return getattr(self, key)
	
	@dutils	
	def client_get(self, key, input_dict,gauth=False,**configs):
		

		
		get_query = self[key]

		# assign query list
		query_list = ["?"]
		for key in input_dict:
			query_list.extend([str(key), "=", input_dict[key], "&"])

		# concatenate together
		get_query += "".join(query_list[:-1])

		if gauth:
			# authentication
			a = GadgethiAuthenticationStandardEncryption(configs['gadgethi_key'],configs['gadgethi_secret'])
			headers = a.authentication_encryption()
			r = requests.get(get_query,headers=headers)
		else:
			r = requests.get(get_query)
		response = r.text 
		return response
		
	@dutils	
	def client_post(self, key, input_dict,gauth=False,urlencode=False, **configs):
		# authentication
		# a = GadgethiAuthenticationStandardEncryption(configs['gadgethi_key'],configs['gadgethi_secret'])
		# headers = a.authentication_encryption()
		post_query = self[key]

		if gauth:
			# authentication
			a = GadgethiAuthenticationStandardEncryption(configs['gadgethi_key'],configs['gadgethi_secret'])
			headers = a.authentication_encryption()

			if urlencode:
				r = requests.post(post_query, data=input_dict,headers=headers)
			else:
				r = requests.post(post_query, json=input_dict,headers=headers)
			response = r.text			
		else:

			if urlencode:
				r = requests.post(post_query, data=input_dict)
			else:
				r = requests.post(post_query, json=input_dict)
			response = r.text

		return response


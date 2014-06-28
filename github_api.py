import requests
import json

class GithubAPI(object):
	"""docstring for GithubAPI"""
	
	def __init__(self, username, access_token):
		super(GithubAPI, self).__init__()
		self.base_url = 'https://api.github.com'
		self.username = username
		self.access_token = access_token

	def auth_tuple(self):
		return (self.access_token, 'x-oauth-basic')
	
	def print_major_repo_info(self, repo_info):
		if repo_info['name']: print "* name: "+ repo_info['name']
		if repo_info['description']: print "* description: "+ repo_info['description']
		if repo_info['homepage']: print "* homepage: "+ repo_info['homepage']
		if repo_info['clone_url']: print "* clone_url: "+ repo_info['clone_url']

	def request_description(self, r):
		print "STATUS: " + str(r.status_code)
		print ""
		print "HEADERS: " + str(r.headers)
		print ""
		print "BODY: " + str(r.text)
		print ""

	## Major Repo Methods ##

	def list_repos(self, page=1):
		r = requests.get(self.base_url+"/user/repos?page="+str(page), auth=self.auth_tuple())
		if ((r.status_code / 100) != 2):
			self.request_description(r)
			raise RuntimeError("unsucessful http code")
		json_res = r.json()
		if not json_res:
			self.request_description(r)
			raise RuntimeError("invalid JSON response")
		for repo in json_res:
			print repo['name']
		print ""
		print "* there maybe more records..."
		print "* use page paramater to see other pages. "
		print ""

	def info_repo(self, name):
		## Make Request and Parse ##
		r = requests.get(self.base_url+"/repos/"+self.username+"/"+name, auth=self.auth_tuple())
		if ((r.status_code / 100) != 2):
			self.request_description(r)
			raise RuntimeError("unsucessful http code")
		json_res = r.json()
		if not json_res:
			self.request_description(r)
			raise RuntimeError("invalid JSON response")
		clone_url = json_res['clone_url']
		if not clone_url:
			self.request_description(r)
			print r.json()
			raise RuntimeError("no clone url")
		self.print_major_repo_info(json_res)
	
	def create_repo(self, name, description="", homepage=""):
		
		## Populate Data ##
		if not name:
			raise RuntimeError("`name` parameter is requried.")
		data_dict = {}
		data_dict['name'] = name
		if description:
			data_dict['description'] = description
		if homepage:
			data_dict['homepage'] = homepage
		string_json_data = json.dumps(data_dict)
		
		## Make Request and Parse ##
		r = requests.post(self.base_url+"/user/repos", auth=self.auth_tuple(), data=string_json_data)
		if ((r.status_code / 100) != 2):
			self.request_description(r)
			raise RuntimeError("unsucessful http code")
		json_res = r.json()
		if not json_res:
			self.request_description(r)
			raise RuntimeError("invalid JSON response")
		clone_url = json_res['clone_url']
		if not clone_url:
			self.request_description(r)
			print r.json()
			raise RuntimeError("no clone url")
		self.print_major_repo_info(json_res)

	def edit_repo(self, name, new_name="", description="", homepage=""):
	
		## Populate Data ##
		if not name:
			raise RuntimeError("`name` parameter is requried.")
		data_dict = {}
		if new_name:
			data_dict['name'] = new_name
		else:
			data_dict['name'] = name
		if description:
			data_dict['description'] = description
		if homepage:
			data_dict['homepage'] = homepage
		string_json_data = json.dumps(data_dict)

		## Make Request and Parse ##
		r = requests.patch(self.base_url+"/repos/"+self.username+"/"+name, auth=self.auth_tuple(), data=string_json_data)
		if ((r.status_code / 100) != 2):
			self.request_description(r)
			raise RuntimeError("unsucessful http code")
		json_res = r.json()
		if not json_res:
			self.request_description(r)
			raise RuntimeError("invalid JSON response")
		clone_url = json_res['clone_url']
		if not clone_url:
			self.request_description(r)
			print r.json()
			raise RuntimeError("no clone url")
		self.print_major_repo_info(json_res)
	
	def delete_repo(self, name):
		if not name:
			raise RuntimeError("`name` parameter is requried.")
		r = requests.delete(
			self.base_url + "/repos/" + self.username + "/" + name, 
			auth=self.auth_tuple())
		if (r.status_code != 204):
			self.request_description(r)
			raise RuntimeError("unknown error")
		else :
			print "deleted `" + name + "` successfully."
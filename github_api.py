import requests
import json
import sys
import os.path

AUTH_INFO_FILEPATH = '/Users/vivekseth/.github_api_auth_info'

def request_description(r):
	print "STATUS: " + str(r.status_code)
	print ""
	print "HEADERS: " + str(r.headers)
	print ""
	print "BODY: " + str(r.text)
	print ""

class GithubAPI(object):
	"""docstring for GithubAPI"""
	
	def __init__(self, filepath=AUTH_INFO_FILEPATH, new_auth=False):
		super(GithubAPI, self).__init__()
		self.base_url = 'https://api.github.com'
		username = ""
		access_token = ""
		if os.path.isfile(filepath) and new_auth == False:
			f = open(filepath)
			d = self.parse_auth_info(f)
			f.close()
			username = d['username']
			access_token = d['access_token']
		else:
			username = raw_input("username: ")
			access_token = raw_input("access_token: ")
			self.write_auth_info(filepath, username, access_token)
		self.username = username
		self.access_token = access_token

	def parse_auth_info(self, f):
		return json.loads(f.read())

	def write_auth_info(self, filepath, username, access_token):
		auth_info_dict = {}
		auth_info_dict['username'] = username
		auth_info_dict['access_token'] = access_token
		auth_info_json_string = json.dumps(auth_info_dict)
		f = open(filepath, 'w')
		f.write(auth_info_json_string)
		f.close()

	def auth_tuple(self):
		return (self.access_token, 'x-oauth-basic')
	
	def print_major_repo_info(self, repo_info):
		if repo_info['name']: print "* name: "+ repo_info['name']
		if repo_info['description']: print "* description: "+ repo_info['description']
		if repo_info['homepage']: print "* homepage: "+ repo_info['homepage']
		if repo_info['clone_url']: print "* clone_url: "+ repo_info['clone_url']

	## Major Repo Methods ##

	def list_repos(self, page=1):
		r = requests.get(self.base_url+"/user/repos?page="+str(page), auth=self.auth_tuple())
		if ((r.status_code / 100) != 2):
			request_description(r)
			raise RuntimeError("unsucessful http code")
		json_res = r.json()
		if not json_res:
			request_description(r)
			raise RuntimeError("invalid JSON response")
		for repo in json_res:
			print repo['name']
		print ""
		print "* there maybe more records..."
		print "* use page paramater to see other pages. "
		print ""

		# clone_url = json_res['clone_url']
		# if not clone_url:
		# 	request_description(r)
		# 	print r.json()
		# 	raise RuntimeError("no clone url")
		# print clone_url

	def info_repo(self, name):
		## Make Request and Parse ##
		r = requests.get(self.base_url+"/repos/"+self.username+"/"+name, auth=self.auth_tuple())
		if ((r.status_code / 100) != 2):
			request_description(r)
			raise RuntimeError("unsucessful http code")
		json_res = r.json()
		if not json_res:
			request_description(r)
			raise RuntimeError("invalid JSON response")
		clone_url = json_res['clone_url']
		if not clone_url:
			request_description(r)
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
			request_description(r)
			raise RuntimeError("unsucessful http code")
		json_res = r.json()
		if not json_res:
			request_description(r)
			raise RuntimeError("invalid JSON response")
		clone_url = json_res['clone_url']
		if not clone_url:
			request_description(r)
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
			request_description(r)
			raise RuntimeError("unsucessful http code")
		json_res = r.json()
		if not json_res:
			request_description(r)
			raise RuntimeError("invalid JSON response")
		clone_url = json_res['clone_url']
		if not clone_url:
			request_description(r)
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
			request_description(r)
			raise RuntimeError("unknown error")
		else :
			print "deleted `" + name + "` successfully."

def main():
	if (len(sys.argv) >= 2):
		command = sys.argv[1]
		if command == "new_auth":
			g = GithubAPI(new_auth=True)
			return
		g = GithubAPI(new_auth=False)
		if command == "list":
			if (len(sys.argv) >= 3):
				g.list_repos(sys.argv[2])
			else:
				g.list_repos()
		elif command == "info":
			if (len(sys.argv) >= 3):
				g.info_repo(sys.argv[2])
			else:
				RuntimeError("USAGE: `python github_api.py in <name>`")
		elif command == "create":
			if (len(sys.argv) >= 3):
				name = sys.argv[2]
				description = ""
				homepage = ""
				if len(sys.argv) >= 4: description = sys.argv[3]
				if len(sys.argv) >= 5: homepage = sys.argv[4]
				g.create_repo(name, description, homepage)				
			else:
				RuntimeError("USAGE: `python github_api.py cr <name> [<description> [<homepage>]]`")
		elif command == "edit":
			if (len(sys.argv) >= 3):
				name = sys.argv[2]
				new_name = ""
				description = ""
				homepage = ""
				if len(sys.argv) >= 4: new_name = sys.argv[3]
				if len(sys.argv) >= 5: description = sys.argv[4]
				if len(sys.argv) >= 6: homepage = sys.argv[5]
				g.edit_repo(name, new_name, description, homepage)				
			else:
				RuntimeError("USAGE: `python github_api.py ed <name> [<new_name> [<description> [<homepage>]]]`")
		elif command == "delete":
			if (len(sys.argv) >= 3): 
				g.delete_repo(sys.argv[2])
			else: 
				RuntimeError("USAGE: `python github_api.py de <name>`")
		else:
			raise RuntimeError("invalid command")

if __name__ == '__main__': main()

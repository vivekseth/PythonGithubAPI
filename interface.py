import json
import sys
import os.path
from os.path import expanduser
from github_api import GithubAPI

AUTH_INFO_FILEPATH = expanduser("~/.github_api_auth_info")

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


def get_arg(index):
	if len(sys.argv) >= (index+1): 
		return sys.argv[index]
	else:
		return ""

def print_help():
	print "commands: [ new_auth, list, info, create, edit, delete ]" 

def create_api_obj():
	auth_info = read_auth(AUTH_INFO_FILEPATH)
	assert auth_info['username']
	assert auth_info['description']
	g = GithubAPI(auth_info['username'], auth_info['access_token'])

def read_auth(filepath):
	if not os.path.isfile(filepath):
		raise StandardError("could not find auth info, please create using `auth new` command")
	else:
		f = open(filepath)
		d = json.loads(f.read())
		f.close()
	if not 'username' in d or not 'access_token' in d:
		raise StandardError("could not parse auth info")
	else:
		return d
def write_auth(filepath, username, access_token):
	if not username or not access_token:
		raise StandardError("need both username and access_token")
	else:
		auth_info_dict = {'username': username, 'access_token': access_token}
		json_string = json.dumps(auth_info_dict)
		f = open(filepath, 'w')
		f.write(json_string)
		f.close()

def _auth():
	option = get_arg(2)
	assert option
	if option == "get":
		filepath = get_arg(3)
		if not filepath: 
			filepath = AUTH_INFO_FILEPATH
		auth_info = read_auth(filepath)
		print "* username: " + auth_info['username']
		print "* access_token: " + auth_info['access_token']
	elif option == "set":
		username = get_arg(3)
		access_token = get_arg(4)
		assert username
		assert access_token
		filepath = get_arg(5)
		if not filepath: 
			filepath = AUTH_INFO_FILEPATH
		write_auth(filepath, username, access_token)
	else:
		print "USAGE: "
		print "git hub auth get [filepath]"
		print "git hub auth set username access_token [filepath]"

def _create():
	options = {
		get_arg(2) : get_arg(3)
		get_arg(4) : get_arg(5)
		get_arg(6) : get_arg(7)
	}
	g = create_api_obj(AUTH_INFO_FILEPATH)
	g.create_repo(
		options['--name'] or options['-n']
		options['--description'] or options['-d']
		options['--homepage'] or options['-h']
	)

def main():
	option = get_arg(1)
	if option == "auth":
		_auth()
	elif option == "create":
		_create()
	else:
		print_help()




# def main():
# 	if (len(sys.argv) >= 2):
# 		command = sys.argv[1]
# 		if command == "help":
# 			print_help()
# 			return
# 		elif command == "new_auth":
# 			g = GithubAPI(new_auth=True)
# 			return
# 		g = GithubAPI(new_auth=False)
# 		if command == "list":
# 			if (len(sys.argv) >= 3):
# 				g.list_repos(sys.argv[2])
# 			else:
# 				g.list_repos()
# 		elif command == "info":
# 			if (len(sys.argv) >= 3):
# 				g.info_repo(sys.argv[2])
# 			else:
# 				RuntimeError("USAGE: `python github_api.py in <name>`")
# 		elif command == "create":
# 			if (len(sys.argv) >= 3):
# 				name = sys.argv[2]
# 				description = ""
# 				homepage = ""
# 				if len(sys.argv) >= 4: description = sys.argv[3]
# 				if len(sys.argv) >= 5: homepage = sys.argv[4]
# 				g.create_repo(name, description, homepage)				
# 			else:
# 				RuntimeError("USAGE: `python github_api.py cr <name> [<description> [<homepage>]]`")
# 		elif command == "edit":
# 			if (len(sys.argv) >= 3):
# 				name = sys.argv[2]
# 				new_name = ""
# 				description = ""
# 				homepage = ""
# 				if len(sys.argv) >= 4: new_name = sys.argv[3]
# 				if len(sys.argv) >= 5: description = sys.argv[4]
# 				if len(sys.argv) >= 6: homepage = sys.argv[5]
# 				g.edit_repo(name, new_name, description, homepage)				
# 			else:
# 				RuntimeError("USAGE: `python github_api.py ed <name> [<new_name> [<description> [<homepage>]]]`")
# 		elif command == "delete":
# 			if (len(sys.argv) >= 3): 
# 				g.delete_repo(sys.argv[2])
# 			else: 
# 				RuntimeError("USAGE: `python github_api.py de <name>`")
# 		else:
# 			raise RuntimeError("invalid command")
# 	else:
# 		print_help()

if __name__ == '__main__': main()


"""

git hub auth vivek seth
git hub create new_repo
git hub read new_repo
git hub update new_repo --name 


"""
import json
import sys
from os.path import isfile
from os.path import expanduser
from github_api import GithubAPI

AUTH_INFO_FILEPATH = expanduser("~/.github_api_auth_info")
COMMAND_PREFIX = "git hub"

# Help String Creation #
HELP_STRINGS = {
	"help" : "",
	"auth" : {
		"get": "[filepath]",
		"set": "username access_token [filepath]",
	},
	"create": "(--name|-n) <repo_name> [(--description|-d) <description>] [(--homepage|-h) <homepage>]",
	"read": {
		"all" : "[page]",
		"<repo_name>": ""
	},
	"update": "<repo_name> [(--name|-n) <repo_name>] (--description|-d) <description>] [(--homepage|-h) <homepage>]",
	"delete": "<repo_name>",
}

def create_help_string(prefix, key_path):
	curr_dict = HELP_STRINGS
	help_string = prefix + " "
	for i in range(len(key_path)):
		help_string += key_path[i] + " "
		curr_dict = curr_dict[key_path[i]]
	help_string += str(curr_dict)
	return help_string


# Authentication Read/Write #
def read_auth(filepath):
	if not isfile(filepath):
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


# Helper Accessor Methods #
def get_arg(index):
	if len(sys.argv) >= (index+1): 
		return sys.argv[index]
	else:
		return ""

def safe_dict_get(dict, key):
	if key in dict:
		return dict[key]
	else:
		return ""

def create_api_obj():
	auth_info = read_auth(AUTH_INFO_FILEPATH)
	assert auth_info['username']
	assert auth_info['access_token']
	g = GithubAPI(auth_info['username'], auth_info['access_token'])
	return g


# Options #
def print_help():
	print ""
	print "commands: [ help, auth, create, read, update, delete ]" 
	print "--help--"
	print create_help_string(COMMAND_PREFIX, ["help"])
	print "--auth--"
	print create_help_string(COMMAND_PREFIX, ["auth", "get"])
	print create_help_string(COMMAND_PREFIX, ["auth", "set"])
	print "--create--"
	print create_help_string(COMMAND_PREFIX, ["create"])
	print "--read--"
	print create_help_string(COMMAND_PREFIX, ["read", "all"])
	print create_help_string(COMMAND_PREFIX, ["read", "<repo_name>"])
	print "--update--"
	print create_help_string(COMMAND_PREFIX, ["update"])
	print "--delete--"
	print create_help_string(COMMAND_PREFIX, ["delete"])
	print ""

def _auth():
	option = get_arg(2)
	try:
		assert option, "invalid option"
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
			raise NotImplementedError("command `"+option+"` is not implemented")
	except Exception, e:
		print "ERROR: "
		print e
		print "USAGE: "
		print create_help_string(COMMAND_PREFIX, ["auth", "get"])
		print create_help_string(COMMAND_PREFIX, ["auth", "set"])

def _create():
	options = {
		str(get_arg(2)) : get_arg(3),
		str(get_arg(4)) : get_arg(5),
		str(get_arg(6)) : get_arg(7),
	}
	g = create_api_obj()
	try:
		g.create_repo(
			safe_dict_get(options, '--name') or safe_dict_get(options, '-n'),
			safe_dict_get(options, '--description') or safe_dict_get(options, '-d'),
			safe_dict_get(options, '--homepage') or safe_dict_get(options, '-h'),
		)
	except Exception, e:
		print "ERROR: "
		print e
		print "USAGE: "
		print create_help_string(COMMAND_PREFIX, ["create"])

def _read():
	option = get_arg(2)
	g = create_api_obj()
	try:
		if option == "all":
			page = get_arg(3)
			g.list_repos(page)
		else:
			repo_name = option
			g.info_repo(repo_name)
	except Exception, e:
		print "ERROR: "
		print e
		print "USAGE: "
		print create_help_string(COMMAND_PREFIX, ["read", "all"])
		print create_help_string(COMMAND_PREFIX, ["read", "<repo_name>"])

def _update():
	repo_name = get_arg(2)
	options = {
		str(get_arg(3)) : get_arg(4),
		str(get_arg(5)) : get_arg(6),
		str(get_arg(7)) : get_arg(8),
	}
	g = create_api_obj()
	try:
		g.edit_repo(
			repo_name,
			safe_dict_get(options, '--name') or safe_dict_get(options, '-n'),
			safe_dict_get(options, '--description') or safe_dict_get(options, '-d'),
			safe_dict_get(options, '--homepage') or safe_dict_get(options, '-h'),
		)
	except Exception, e:
		print "ERROR: "
		print e
		print "USAGE: "
		print create_help_string(COMMAND_PREFIX, ["update"])

def _delete():
	repo_name = get_arg(2)
	g = create_api_obj()
	try:
		g.delete_repo(repo_name)
	except Exception, e:
		print "ERROR: "
		print e
		print "USAGE: "
		print create_help_string(COMMAND_PREFIX, ["delete"])


# Main #
def main():
	option = get_arg(1)
	if option in ["h", "help", "-h", "--h", "--help"]:
		print_help()
	elif option in ["a", "auth"]:
		_auth()
	elif option in ["c", "create"]:
		_create()
	elif option in ["r", "read"]:
		_read()
	elif option in ["u", "update"]:
		_update()
	elif option in ["d", "delete"]:
		_delete()
	else:
		print "ERROR: invalid option"
		print "To see available commands please use:"
		print create_help_string(COMMAND_PREFIX, ["help"])

if __name__ == '__main__': main()
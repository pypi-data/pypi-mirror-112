#!/usr/bin/env python
import tornado.web
import tornado.ioloop
import json
import os
import pwd
import click
from pybis import Openbis

## auth.py
import os
import shutil

# Example method call: adduser("test_user", 1010, ["jupyterhub"])

# Critical files used to add new users to the system as they are on Cent OS 7 used at SIS JupyterHub image for openBIS
ETC_PASSWD = "/etc/passwd"
ETC_SHADOW = "/etc/shadow"
ETC_GROUP = "/etc/group"
HOME = "/home"
HOME_TEMPLATE = "/etc/skel"

def adduser(username, user_id, groups, create_home):
    # Verify input to avoid corrupting system files
    if (username is None) or (not isinstance(username, str)):
        raise Exception("username can't be None and should be a string")

    if (user_id is None) or (not isinstance(user_id, int)):
        raise Exception("user_id can't be None and should be an int")

    if groups is None:
        groups = []
    elif not isinstance(groups, list):
        raise Exception("groups can be None or a list of string")
    else:
        for group in groups:
            if (group is None) or (not isinstance(group, str)):
                raise Exception("group can't be None and should be a string")

    if (create_home is None) or (not isinstance(create_home, bool)):
        raise Exception("create_home can't be None and should be a bool")

    # 1. The next line needs to be added at the end of /etc/passwd
    etc_passwd_last_line = username + ":x:" + str(user_id) + ":" + str(user_id) + "::/home/" + username + ":/bin/bash"
    with open(ETC_PASSWD, 'a') as file:
        file.write("\n" + etc_passwd_last_line)
    # 2. The next line needs to be added at the end of /etc/shadow
    etc_shadow_last_line = username + ":!!:18813:0:99999:7:::"
    with open(ETC_SHADOW, 'a') as file:
        file.write("\n" + etc_shadow_last_line)
    # 3. The next line needs to be added at the end of /etc/group
    etc_group_last_line = username + ":x:" + str(user_id) + ":"
    with open(ETC_GROUP, 'a') as file:
        file.write("\n" + etc_group_last_line)
    # 4. Additional groups names, for example the jupyterhub group is needed on jupyterhub installations
    etc_group_additional_groups_end_line = "," + username
    for group in groups:
        new_etc_group_file = ""
        with open(ETC_GROUP, 'r') as etc_group_file:
            lines = etc_group_file.readlines()
            for line in lines:
                if line[0:len(group)] == group:
                    new_etc_group_file = new_etc_group_file + line.rstrip('\n') + etc_group_additional_groups_end_line + "\n"
                else:
                    new_etc_group_file = new_etc_group_file + line
        with open(ETC_GROUP, 'w') as etc_group_file:
            etc_group_file.write(new_etc_group_file)
    # 5. Create user directory at /home and copy the template from /etc/skel/.*
    if create_home: # This step is optional
        home_dir = HOME + "/" + username
        shutil.copytree(HOME_TEMPLATE, home_dir) # Create home directory from the skeleton files
    # 6. Set rights of existing user directory
    os.chown(home_dir, user_id, user_id) # Set as owner the user and the user group to the files on the user dir
    for dirpath, dirnames, filenames in os.walk(home_dir):
        for dname in dirnames:
            os.chown(os.path.join(dirpath, dname), user_id, user_id)
        for fname in filenames:
            os.chown(os.path.join(dirpath, fname), user_id, user_id)
    os.chmod(home_dir, 0o700) # Only allows owner to list files
##

class CreateNotebook(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self, whatever):
        self.send_error(400, {'message':'this webservice does not allow any GET requests. Please make a POST request with the arguments token, folder and filename. The body must contain the content of the file.'})

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def post(self, whatever):
        test = self.get_argument(name='test', default=None)

        try:
            token = self.get_argument(name='token')
            folder = self.get_argument(name='folder')
            filename = self.get_argument(name='filename')
        except Exception as e:
            self.send_error(400, {'message': str(e)})
            return

        # file-content
        content = self.request.body

        # extract username
        username, code = token.split('-')

        if test == None or test == 'False':
            test = False

        # test if openbis sessiontoken is still valid
        if not self.openbis.is_token_valid(token):
            self.send_error(401, {'message': 'token is invalid', 'token':token} )
            return

        try:
            user = pwd.getpwnam(username)
        except KeyError:
            if self.create_users_automatically:
                try: 
                    self.create_user(username)
                    user = pwd.getpwnam(username)
                except Exception:
                    self.send_error(500, {'message':"User {} cannot be created on the host system".format(username)} )
                    return
            else:
                self.send_error(401, {'message':"User {} does not exist on host system".format(username)} )
                return


        path_to_notebook = os.path.join(
            user.pw_dir, 
            folder,
            filename
        )

        # create necessary directories
        try:
            os.makedirs(os.path.dirname(path_to_notebook), exist_ok=True)
        except Exception as e:
            self.send_error(500, {'message':'unable to create directory {}: {}'.format(os.path.dirname(path_to_notebook), e)} )
            
        
        # add sequence to the filename if file already exists
        filename_name_end = filename.rfind('.')
        filename_name = filename[:filename_name_end]
        filename_extension = filename[filename_name_end:]
        filename_new = filename_name + filename_extension

        # check whether file exists
        path_to_notebook_new = os.path.join(
            user.pw_dir, 
            folder,
            filename_new
        )

        # add a number to the end of the file, if file already exists (OS X like)
        # file.ext
        # file.ext 2
        # file.ext 3
        i = 1
        while os.path.isfile(path_to_notebook_new):
            i += 1
            filename_new = filename_name + " " + str(i) + filename_extension
            path_to_notebook_new = os.path.join(
                user.pw_dir, 
                folder,
                filename_new
            )
        path_to_notebook = path_to_notebook_new
        
        link_to_notebook = {
            "fileName": filename_new,
            "path": path_to_notebook
        }
        
        # test: return without actually writing the file
        if test:
            self.write(json.dumps(link_to_notebook))
            return

        # try to write the file
        try:
            with open(path_to_notebook, 'wb') as f:
                f.write(content)
            os.chown(path_to_notebook, user.pw_uid, user.pw_gid)
            os.chmod(path_to_notebook, 0o644)
            path_to_notebook_folder = os.path.join(
                user.pw_dir, 
                folder
            )
            os.chown(path_to_notebook_folder, user.pw_uid, user.pw_gid)
            os.chmod(path_to_notebook_folder, 0o755)
        except Exception as e:
            self.send_error(500, {'message': 'unable to write file {} : {}'.format(path_to_notebook, e)} )

        self.write(json.dumps(link_to_notebook))

    def get_new_uid_for_home(self, os_home):
        id_sequence = 999; # Linux uids start at 1000
        for file in next(os.walk(os_home))[1]:
            home_info = os.stat(os_home + file)
            if home_info.st_uid > id_sequence:
                id_sequence = home_info.st_uid
            if home_info.st_gid > id_sequence:
                id_sequence = home_info.st_gid
        if id_sequence is None:
            return None
        else:
            return { "uid" : id_sequence + 1 }

    def create_user(self, username):
        os_home = "/home/" # Default CentOS home as used at the ETHZ
        home = os_home + username
        if os.path.exists(home): # If the home exists
            home_info = os.stat(home)
            home_uid = home_info.st_uid
            adduser(username, home_uid, ["jupyterhub"], False) # Add user to the OS without recreating his home folder
        else:
            new_uid = self.get_new_uid_for_home(os_home)
            adduser(username, new_uid["uid"], ["jupyterhub"], True) # Add user to the OS creating his home folder

    def send_error(self, status_code=500, message=""):
        self.set_status(status_code)
        self.write(message)

    def initialize(self, openbis, create_users_automatically):
        self.openbis = openbis
        self.create_users_automatically = create_users_automatically
        self.set_header('Content-Type', 'application/json')


def make_app(openbis, create_users_automatically):
    """All the routing goes here...
    """
    app = tornado.web.Application([
        (r"/(.*)", CreateNotebook, {"openbis": openbis, "create_users_automatically": create_users_automatically})
    ])
    return app

@click.command()
@click.option('--port', default=8123, help='Port where this server listens to')
@click.option('--cert', default=None, help='Path to your cert-file in PEM format')
@click.option('--key', default=None, help='Path to your key-file in PEM format')
@click.option('--openbis', required=True, help='URL and port of your openBIS installation')
@click.option('--create-users', is_flag=True, help='automatically create users, if they are not present in the system')
def start_server(port, cert, key, openbis, create_users):
    openbis = Openbis(url=openbis, verify_certificates=False)
    application = make_app(openbis=openbis, create_users_automatically=create_users)

    if cert is not None and key is not None:
        application.listen(port , ssl_options = { "certfile": cert, "keyfile":  key })
    else:
        application.listen(port);

    print("openBIS integration service started, listening on port {}".format(port))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start_server()

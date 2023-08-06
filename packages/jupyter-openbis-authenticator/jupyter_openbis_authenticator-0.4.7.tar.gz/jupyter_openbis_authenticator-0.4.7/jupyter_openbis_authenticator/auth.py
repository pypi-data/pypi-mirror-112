#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import pwd

from jupyterhub.auth import Authenticator
from sudospawner import SudoSpawner
import pamela
from tornado import gen
from traitlets import Unicode, Bool

from pybis.pybis import Openbis

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

class OpenbisAuthenticator(Authenticator):
    server_url = Unicode(
        config=True,
        help='URL of openBIS server to contact'
    )

    kerberos_domain = Unicode(
        config=True,
        help='The domain to authenticate against to obtain a kerberso ticket'
    )

    default_username = Unicode(
        config=True,
        help='the username which should be used within jupyterhub/binderhub instead of the real username, usually jovyan'
    )

    verify_certificates = Bool(
        config=True,
        default_value=True,
        help='Should certificates be verified? Normally True, but maybe False for debugging.'
    )

    create_system_users = Bool(
        config=True,
        default_value=False,
        help='Should create system users?'
    )

    valid_username_regex = Unicode(
        r'^[a-zA-Z][.a-zA-Z0-9_-]*$',
        config=True,
        help="""Regex to use to validate usernames before sending to openBIS."""
    )

    normalize_usernames = Bool(
        config=True,
        default_value=True,
        help='Should user names be normalized (by default changed to lowercase)?'
    )

    def normalize_username(self, username):
        if self.normalize_usernames:
            return super().normalize_username(username)
        else:
            return username

    @gen.coroutine
    def authenticate(self, handler, data):
        """Checks username and password against the given openBIS instance.
        If authentication is successful, it not only returns the username but
        a data structure:
        {
            "name": username,
            "auth_state": {
                "token": openBIS.token,
                "url"  : openBIS.url
            }
        }
        """
        username = data['username']
        password = data['password']
        session = data['session'] # If session is given it takes precedence over the username and password

        if session is None or session.strip() == '':
            # Protect against invalid usernames as well as LDAP injection attacks
            if not re.match(self.valid_username_regex, username):
                self.log.warn('Invalid username')
                return None

            # No empty passwords!
            if password is None or password.strip() == '':
                self.log.warn('Empty password')
                return None
        else:
            if session.find('-') > -1:
                username = session[0:session.index('-')]
                password = ''
            else:
                self.log.warn('Invalid session')
                return None

        openbis = Openbis(self.server_url, verify_certificates=self.verify_certificates)
        try:
            # authenticate against openBIS and store the token (if possible)
            if session is None or session.strip() == '':
                openbis.login(username, password, True)
            else:
                openbis.token = session
                if openbis.is_session_active():
                    self.log.warn('Valid session')
                    if os.environ.get('OPENBIS_URL') == openbis.url:
                        os.environ['OPENBIS_TOKEN'] = openbis.token
                else:
                    self.log.warn('Invalid session')
                    return None
            # creating user if not found on the system
            if self.create_system_users:
                try:
                    user = pwd.getpwnam(username)
                except KeyError:
                    self.create_user(username)

            # instead of just returning the username, we return a dict
            # containing the auth_state as well
            kerberos_username = username
            if getattr(self, 'kerberos_domain', None):
               kerberos_username = username + '@' + self.kerberos_domain

            if getattr(self, 'default_username', None):
                kerberos_username = self.default_username
            return {
                "name": kerberos_username,
                "auth_state": {
                    "token": openbis.token,
                    "url": openbis.url,
                    "kerberos_username": kerberos_username,
                    "username": username,
                    "kerberos_password": password,

                }
            }
        except ValueError as err:
            self.log.warn(str(err))
            return None


    @gen.coroutine
    def pre_spawn_start(self, user, spawner):
        """Pass openbis token to spawner via environment variable"""
        auth_state = yield user.get_auth_state()
        if not auth_state:
            # auth_state not enabled
            return

        # Write the openBIS token to the users' environment variables
        spawner.environment['OPENBIS_URL']       = auth_state['url']
        spawner.environment['OPENBIS_TOKEN']     = auth_state['token']
        spawner.environment['KERBEROS_USERNAME'] = auth_state['kerberos_username']
        spawner.environment['KERBEROS_PASSWORD'] = auth_state['kerberos_password']
        spawner.environment['USERNAME']          = auth_state['username']


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

class KerberosSudoSpawner(SudoSpawner):
    """Specialized SudoSpawner which defines KERBEROS_USERNAME and KERBEROS_PASSWORD
    for the global environment variables. These variables are later used by the
    sudospawner-singleuser script to log in to Active Director to obtain a valid Kerberos ticket
    """

    def get_env(self):
        env = super().get_env()

        spawner_env = getattr(self.user.spawner, 'environment', None)
        if not spawner_env:
            # auth_state was probably not enabled
            return env
        env['KERBEROS_USERNAME'] = spawner_env['KERBEROS_USERNAME']
        env['KERBEROS_PASSWORD'] = spawner_env['KERBEROS_PASSWORD']
        return env

    @gen.coroutine
    def do(self, action, **kwargs):
        """Before we spawn the notebook server, we need to obtain a Kerberos ticket
        otherwise we'll get a PID error as we cannot access the (SMB mounted) user home
        without a valid Kerberos ticket.
        """

        if os.getenv('KERBEROS_USERNAME') and os.getenv('KERBEROS_PASSWORD'):
            pamela.authenticate(
                os.getenv('KERBEROS_USERNAME'),
                os.getenv('KERBEROS_PASSWORD'),
                resetcred=0x0002
            )

        return super().do(action, **kwargs)

"""
CloudPipe libraries

"""

import logging
import os
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

import contrib
import flags
from nova import crypto
from nova.auth import users
FLAGS = flags.FLAGS


class CloudPipe(object):
    def __init__(self, cloud_controller):
        self.controller = cloud_controller
        self.manager = users.UserManager()
    
    def launch_vpn_instance(self, username):
        logging.debug( "Launching VPN for %s" % (username))
        user = self.manager.get_user(username)
        # Make a payload.zip
        tmpfolder = tempfile.mkdtemp()
        filename = "payload.zip"
        zippath = os.path.join(tmpfolder, filename)
        z = ZipFile(zippath, "w", ZIP_DEFLATED)
        z.write('bootscript.sh','autorun.sh')
        z.close()
    
        self.setup_keypair(username)
        zippy = open(zippath, "r")
        reservation = self.controller.run_vpn_instance(user, user_data = zippy.read().encode("base64"), key_name = "vpn-key", security_groups = ["vpn-secgroup"])
        zippy.close()

    def setup_keypair(self, username):
        try:
            keypair, fingerprint = self.manager.generate_key_pair(username, "vpn-key")
            os.mkdir("%s/%s" % (FLAGS.keys_path, username))
            keypair.save(os.path.abspath("%s/%s" % (FLAGS.keys_path, username)))
        except:
            pass
        
    # def setup_secgroups(self, username):
    #     conn = self.euca.connection_for(username)
    #     try:
    #         secgroup = conn.create_security_group("vpn-secgroup", "vpn-secgroup")
    #         secgroup.authorize(ip_protocol = "udp", from_port = "1194", to_port = "1194", cidr_ip = "0.0.0.0/0")
    #         secgroup.authorize(ip_protocol = "tcp", from_port = "80", to_port = "80", cidr_ip = "0.0.0.0/0")
    #         secgroup.authorize(ip_protocol = "tcp", from_port = "22", to_port = "22", cidr_ip = "0.0.0.0/0")
    #     except:
    #         pass
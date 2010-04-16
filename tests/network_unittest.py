# vim: tabstop=4 shiftwidth=4 softtabstop=4
import logging
import StringIO
import time
import unittest
from xml.etree import ElementTree

import contrib
import mox
from tornado import ioloop
from twisted.internet import defer

import exception
import flags
import node
import network
import test


FLAGS = flags.FLAGS


class NetworkTestCase(unittest.TestCase):
    def setUp(self):
        FLAGS.fake_libvirt = True
        FLAGS.fake_network = True
        FLAGS.fake_rabbit = True
        FLAGS.fake_users = True
        super(NetworkTestCase, self).setUp()
        self.node = node.Node()
        self.network = network.NetworkNode()
        logging.getLogger().setLevel(logging.DEBUG)
        
        # Create one volume and one node to test with
        self.instance_id = "network-test"
        rv = self.node.run_instance(self.instance_id)
    
    def _get_user_addresses(self, user_id):
        rv = self.network.describe_addresses()
        user_addresses = []
        for item in rv:
            if rv['user_id'] == user_id:
                user_addresses.append(rv['address'])
        return user_addresses
        
    
    def test_allocate_deallocate_address(self):
        address = yield self.network.allocate_address("fake")
        self.assertEqual(True, address in self._get_user_addresses("fake"))
        rv = yield self.network.deallocate_address(address)
        self.assertEqual(False, address in self._get_user_addresses("fake"))
        
    
    def test_associate_deassociate_address(self):
        raise NotImplementedError
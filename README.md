PiNet
=====

a eucalyptus clone in python, amqp, tornado, ...

DEPENDENCIES
============

RabbitMQ: messaging queue, used for all communication between components
OpenLDAP: users, groups (maybe cut)
Redis: data store
Tornado: scalable non blocking web server for api requests
Twisted: just for the twisted.internet.defer package
M2Crypto: boto has a dependency on it, yup
IPy: library for managing ip addresses

COMPONENTS
==========

API: receives http requests from boto, and sends commands to other components via amqp
Controller: global state of system and 
Nodes: worker that spawns instances
S3: tornado based http/s3 server

MILESTONES
==========

Alive
-----

  [x] can spawn instances via python api from a single image
  [ ] can ssh into instance spawned instances (network system mode)

Growing
-------

  [ ] Cloud init generates certs for cloud
  [ ] images stored on s3 as full files (not encrypted)
  [ ] euca-get-console-output works
  [ ] euca-terminate-instances works
  [X] euca-run-instances works
  [X] euca-describe-instances works
  [X] can launch from many different images
  [ ] can launch different sizes
  [ ] node downloads images

Works
-----

  [X] can create volumes
  [X] can destroy volumes
  [X] can attach volumes

Secure
------

  [ ] x509 certificate generation
  [ ] can list, upload and register images using real apis
  [X] users exist and have ec2 credentials
  [X] api calls are validated and ran as a user
  [ ] keypairs work
  [X] Deliver creds to user (pinetrc, etc)

Wow
----

  [ ] works with dashboard
  [ ] network with subnets/vlans works
  [ ] can allocate and attach public IPs
  [ ] security groups works
  [ ] instances can access their user-data, meta-data

Installation
============

  apt-get install python-libvirt libvirt-bin kvm rabbitmq-server python-dev python-pycurl python-simplejson
  apt-get install iscsitarget aoetools vblade-persist

  # fix ec2 metadata/userdata uri
  iptables -t nat -A PREROUTING -s 0.0.0.0/0 -d 169.254.169.254/32 -p tcp -m tcp --dport 80 -j DNAT --to-destination 10.0.0.2:8773

  # install tornado
  wget http://www.tornadoweb.org/static/tornado-0.2.tar.gz
  tar xvzf tornado-0.2.tar.gz
  cd tornado-0.2
  python setup.py build
  sudo python setup.py install

import boto
from boto.ec2.regioninfo import RegionInfo

CLC_IP = '127.0.0.1'
#CLC_IP = '172.24.193.2'
CLC_PORT = 8773
REGION = 'omega'
ACCESS_KEY = 'WKy3rMzOWPouVOxK1p3Ar1C2uRBwa2FBXnCw'
SECRET_KEY = 'icSUO24isz55qbfEFQ5bl3pU1C6ZED9MmAA'

conn = boto.connect_ec2 (
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    is_secure=False,
    region=RegionInfo(None, REGION, CLC_IP),
    port=CLC_PORT,
    path='/services/Configuration',
    debug=99
)

"""
euca = Euca ( 
    CLC_IP,
    REGION,
    ACCESS_KEY,
    SECRET_KEY
)

conn = euca.connection_for('test', debug=2)
"""

print conn.get_all_images()
#print conn.get_all_key_pairs()
#print conn.create_key_pair
#print conn.create_security_group('name', 'description')


from nova.exception import NotFound, NotAuthorized
from nova.objectstore import Object

import nova.contrib
from nova.flags import FLAGS

import os
import anyjson
import glob

class Bucket(object):
    def __init__(self, name):
        self.name = name
        self.path = os.path.abspath(os.path.join(FLAGS.buckets_path, name))
        if not self.path.startswith(os.path.abspath(FLAGS.buckets_path)) or \
           not os.path.isdir(self.path):
            raise NotFound
        
        self.ctime = os.path.getctime(self.path)

    def __repr__(self):
        return "<Bucket: %s>" % self.name

    @staticmethod
    def all():
        """ list of all buckets """
        buckets = []
        for fn in glob.glob("%s/*.json" % FLAGS.buckets_path):
            try:
                anyjson.deserialize(open(fn).read())
                name = os.path.split(fn)[-1][:-5]
                buckets.append(Bucket(name))
            except:
                pass

        return buckets
    
    @staticmethod
    def create(name, user):
        """ create a new bucket owned by a specific user """
        path = os.path.abspath(os.path.join(
            FLAGS.buckets_path, name))
        if not path.startswith(os.path.abspath(FLAGS.buckets_path)) or \
           os.path.exists(path):
            raise NotAuthorized
        
        os.makedirs(path)
        
        f = open(path+'.json', 'w')
        f.write(anyjson.serialize({'ownerId': user.id}))
        f.close()
        
        
    def to_json(self):
        return {
            "Name": self.name,
            "CreationDate": datetime.datetime.utcfromtimestamp(self.ctime),
        }
    
    @property
    def owner_id(self):
        try:
            return anyjson.deserialize(open(self.path+'.json').read())['ownerId']
        except:
            return None
    
    def is_authorized(self, user):
        try:
            return user.is_admin() or self.owner_id == user.id
        except:
            pass
    
    def list_keys(self, prefix='', marker=None, max_keys=1000, terse=False):
        object_names = []
        for root, dirs, files in os.walk(self.path):
            for file_name in files:
                object_names.append(os.path.join(root, file_name)[len(self.path)+1:])
        object_names.sort()
        contents = []

        start_pos = 0
        if marker:
            start_pos = bisect.bisect_right(object_names, marker, start_pos)
        if prefix:
            start_pos = bisect.bisect_left(object_names, prefix, start_pos)

        truncated = False
        for object_name in object_names[start_pos:]:
            if not object_name.startswith(prefix):
                break
            if len(contents) >= max_keys:
                truncated = True
                break
            object_path = self._object_path(object_name)
            c = {"Key": object_name}
            if not terse:
                info = os.stat(object_path)
                c.update({
                    "LastModified": datetime.datetime.utcfromtimestamp(
                        info.st_mtime),
                    "Size": info.st_size,
                })
            contents.append(c)
            marker = object_name

        return {
            "Name": self.name,
            "Prefix": prefix,
            "Marker": marker,
            "MaxKeys": max_keys,
            "IsTruncated": truncated,
            "Contents": contents,
        }
        
    def _object_path(self, object_name):
        fn = os.path.join(self.path, object_name)
        
        if not fn.startswith(self.path):
            raise NotAuthorized
        
        return fn
    
    def delete(self):
        if len(os.listdir(self.path)) > 0:
            raise NotAuthorized
        os.rmdir(self.path)
        os.remove(self.path+'.json')
    
    def __getitem__(self, key):
        return Object(self, key)
    
    def __setitem__(self, key, value):
        fn = self._object_path(key)
        f = open(fn, 'wb')
        f.write(value)
        f.close()
    
    def __delitem__(self, key):
        Object(self, key).delete()

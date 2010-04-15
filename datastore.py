import os
import contrib
import anyjson

import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('datastore_path', '/Users/joshua/pinet/keeper',
                    'where keys are stored on disk')

PREFIX = "stuff-"

class keeper(object):
    def __init__(self, prefix="pinet-"):
        #self.prefix = prefix
        pass
        
    def _slugify(self, key):
        return key

    

    def __getitem__(self, item):
        # TODO - Memoize this
        item = self._slugify(item)
        path = "%s/%s%s" % (FLAGS.datastore_path, PREFIX, item)
        if os.path.isfile(path):
            return anyjson.deserialize(open(path, 'r').read())
        return None


    def __setitem__(self, item, value):
        item = self._slugify(item)
        path = "%s/%s%s" % (FLAGS.datastore_path, PREFIX, item)
        f = open(path, "w")
        f.write(anyjson.serialize(value))
        # TODO: Pop and return the old value?
        return value

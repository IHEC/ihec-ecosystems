import sys


class Config:
    @staticmethod
    def sys():
        return Config(sys.argv[1:])
    @staticmethod
    def from_raw(keys = None, values=None, flags=None):
        config = Config()  
        config.keys = dict() if not keys else keys
        config.values = list() if not values else values
        config.flags = set() if not flags else flags  
        return config 
    def __init__(self, args, keydelim=':'):
        self.values = list()
        self.keys = dict()
        self.flags = set()
        self.log = lambda x: sys.stderr.write('# {0}\n'.format(x))		
        if not args: args = []
        for e in args:
            if e[0] == '-':
                keyvalue = e.split(keydelim)
                if len(keyvalue) == 1:
                    self.flags.add(e)
                else:
                    assert not keyvalue[0] in self.keys
                    self.keys[keyvalue[0]] = keydelim.join(keyvalue[1:])
            else:
                self.values.append(e)
    def add_key(self, k, v, update=False):
        if not update:
            assert not k in self.keys
        self.keys[k] = v
        return v
    def has(self, k):
        return k in self.keys or k in self.flags
    def orElse(self, k, default):
        return self.keys.get(k, default)
	def __contains__(self, item):
		return self.has(k)
    def __getitem__(self, k):
        if k in self.keys: return self.keys[k]
        elif k in self.flags: return True
        else:
            self.log('...missing key "{0}"'.format(k))
            return None
    def getOrElse(self, k, defaultValue=None):
        return self.keys.get(k, defaultValue) 

    def args(self, orpipe=False):
        if '-args' in self.keys:
            with open(self.keys['-args']) as infile:
                return [e.strip() for e in infile]
        elif self.values:
            return self.values
        elif not orpipe:
            return list()
        else:
            import fileinput
            return [e for e in fileinput.input([])]



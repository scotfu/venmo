#!/usr/bin/env python

class Storage:
    _instance = None


    def __init__(self):
        if not Storage._instance:
            self.db = {}
            Storage._instance =self

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            self.__init__()
        return cls._instance

    def put(self, instance):
        class_name = instance.__class__.__name__
        if class_name in self.db:
            self.db[class_name].append(instance)
        else:
            self.db[class_name] = [instance]

    def get(self, mclass, user=None):
        class_name = mclass.__name__
        return self.db[class_name]

    def all(self, name, user=None):
        class_name = name
        return self.db[class_name]
        
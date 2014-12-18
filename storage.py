#!/usr/bin/env python
"""
Storage layer
All data is pesisted in memory
Singleton pattern, only one instance of tables

"""
tables = {}


def put(instance):
    """save an instance to its table, table name is the same as class name"""
    global tables
    key = instance.__class__.__name__
    if key in tables:
        tables[key].append(instance)
    else:
        tables[key] = [instance]

def get():
    pass

def destory():
    global tables
    tables = {}
    

def get_all(kls):
    """return a list of all instances of that class """
    global tables
    return tables.get(kls.__name__,[])
    
        
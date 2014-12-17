#!/usr/bin/env python

tables = {}


def put(instance):
    global tables
    key = instance.__class__.__name__
    if key in tables:
        tables[key].append(instance)
    else:
        tables[key] = [instance]

def get():
    pass


def get_all(kls):
    global tables
    return tables.get(kls.__name__,[])
    
        
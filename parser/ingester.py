#!/usr/bin/env python
# coding: utf-8

##Imports - try to pull off more dependencies by the end:
import argparse
from lxml import etree
import multiprocessing
import os
import operator
import psycopg2
import pytest
import sys
import time

#Internals
from parsing_funcs import lumberjack
from parsing_funcs import pg_inter


## Main ingestion object:
class ingester:
    """take file and column labels and insert into postgresql"""
    def __init__(self, interface=None, fname, uname, pword, cols=None, validation_file=None, unit=None, port="5432", db=None):
        super(ingester, self).__init__()
        self.filename = fname #expects a path
        self.columns = cols #expects a list of names (str)
        self.username = uname #expects a string
        self.password = pword #expects a string
        self.validation_file = validation_file #expects some DTD
        self.unit = unit #expects a string        
        self.port = port #gives a default string
        self.database = db #default is to create a new one
        self.tree = None
        #encoding specification
        #host specification
        
    filename = property(operator.attrgetter('_filename'))
    columns = property(operator.attrgetter('_columns'))
    username = property(operator.attrgetter('_username'))
    password = property(operator.attrgetter('_password'))
    validation_file = property(operator.attrgetter('_validation_file')) #not passing test
    unit = property(operator.attrgetter('_unit'))
    port = property(operator.attrgetter('_port'))
    database = property(operator.attrgetter('_database'))
    
    @filename.setter
    def filename(self, f):
        if not os.path.isfile(os.path.join(os.getcwd(),f)):
            #default behavior is for the tool to be called in the directory of the file.
            raise Exception("No file at given path")
        else:
            self._filename = f       
        
    @columns.setter
    def columns(self, c):
        if not c:
            self._columns = False
        else:
            if type(c)==list:
                self._columns = c
            else:
                self._columns = list(c)
                assert len(self._columns)==1, "pass a list of names or single string"

    @username.setter
    def username(self, u):
        assert type(u)==str, "username must be string"
        self._username = u

    @password.setter
    def password(self, p):
        assert type(p)==str, "password must be string"
        self._password = p
   
    @validation_file.setter
    def validation_file(self, vf):
        if not vf:
            self._validation_file = False
        else:
            if not os.path.isfile(os.path.join(os.getcwd(),f)):
                #default behavior is for the tool to be called in the directory of the file.
                raise Exception("No file at given path")
            else:
                self._validation_file = vf
            
    @unit.setter
    def unit(self, unit):
        if unit:
            #infer this later (for each set(base element) in the tree, proceed)
            assert type(unit)==str, "primary unit must be string" 
        self._unit = unit

    @port.setter
    def port(self, pt):
        pt = str(pt) #if passed int
        self._port = pt

    @database.setter
    def database(self, db):
        if not db:
            self._database = False
        else:
            assert type(db)==str, "database name must be string"
            self._database = db
        
import json
import os.path
import csv
import datetime
import requests
import urllib
from doc_search import search
import re

class UniversityList:
    "Class for managing Grid Data loads and filtering"
    
    def __init__(self, 
                 country = None, 
                 list = None, 
                 type = 'Education',
                 loadgrid = True,
                 immediatefilter = False,
                 core_data_dir = None):
        self.country = country
        self.list = list
        self.type = type
        self.core_data_dir = core_data_dir

        if loadgrid:
            self.loadgrid()
        if immediatefilter:
            self.filtergrid()


    def loadgrid(self):
        "Load data from a Grid data dump"

        if not self.core_data_dir:
        	self.core_data_dir = os.path.join('../general/core_data','grid20170926')
        gridjsonfile = 'grid.json'
    
        filename = os.path.join(self.core_data_dir,  
                                gridjsonfile)
        with open(filename, encoding = 'utf-8') as f:
                self.grid = json.load(f)
    
        return self.grid

    def filtergrid(self):
        "Apply filters to full Grid Database to make clean list"
        
        self.unis = []
        
        # Filter for list
        if self.list:
            with open(self.list, encoding = 'utf-8-sig') as f:
                reader = csv.DictReader(f)
                idlist = [line.get('id') for line in reader]
            self.unis = [uni for uni in self.grid['institutes'] 
                                          if uni.get('id') in idlist]
            return
            
        # Filter for type
        typematches = [uni for uni in self.grid['institutes'] 
                                            if self.typefilter(uni)]
        
        # Filter for country
        if self.country:
            cf = self.makecountryfilter(self.country)
            self.unis = [uni for uni in typematches if cf(uni)]
            return
        
        else:
            self.unis = typematches
            return
            

    def typefilter(self,item):
        try:
            return self.type in item.get('types')
        except TypeError:
            return False
    		
    def makecountryfilter(self, country):
        def countryfilter(item):
            for address in item.get('addresses'):
                if country in address['country']:
                    return True
        return countryfilter
    
    def savelist(self, filepath):
        "Write current unis to a CSV list of Grid ID and Name to a file"
        
        with open(filepath, 'w', encoding = 'utf-8') as csvfile:
            fieldnames = ['id', 'name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for uni in self.unis:
                writer.writerow({'id': uni.get('id'), 'name': uni.get('name')})
	
	
class Catalog:
    "Class for handling and managing data catalog files"
    
    def __init__(self,
                 outfilepath = None,
                 fieldnames = None):
        
        self.outfilepath = outfilepath
        self.fieldnames = fieldnames
        self.catalog = []
        
    def load_catalog(self):
        
        if not os.path.isdir(os.path.split(self.outfilepath)[0]):
            os.makedirs(os.path.split(self.outfilepath)[0])
        if not os.path.isfile(self.outfilepath):
            return
            
        with open(self.outfilepath, encoding = 'utf-8-sig') as f:
            reader = csv.DictReader(f)
            self.catalog = [line for line in reader]
            self.fieldnames = reader.fieldnames
            
    def save_full(self, outfilepath = None):
        if not outfilepath: outfilepath = self.outfilepath
        if not os.path.isdir(os.path.dirname(self.outfilepath)):
            os.mkdir(os.path.dirname(self.outfilepath)) #todo fix case when self.outfilepath is None        

        with open(outfilepath, 'w', encoding = 'utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)

            writer.writeheader()
            for row in self.catalog:
                writer.writerow(row)
            
    def save_append(self, newitems):
        "Append new items to catalog file from a list of dictionaries"

        if type(newitems) == dict:
            newitems = [newitems]

        if not os.path.isfile(self.outfilepath):
            with open(self.outfilepath, 'a', encoding = 'utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
                writer.writeheader()
        for row in newitems:                
            newrow = self.append_row(row)
                
            with open(self.outfilepath, 'a', encoding = 'utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
                writer.writerow(newrow)
                
    def append_row(self, d):
        """Append a new row to the catalog
        
        Takes a dictionary as input, checks it against self.fieldnames
        and adds a row containing the input values from d or an
        empty string. Additional elements are dropped.
        
        Parameters
        ----------
        d : dict
           A dictionary of items for incorporation
           
        Returns
        -------
        newrow : dict
           Returns the new row for the catalog with entries for all keys in
           self.fieldnames
        """
        
        newrow = {}
        for k in self.fieldnames:
            newrow[k] = d.get(k, '')
        
        self.catalog.append(newrow)               
        return newrow
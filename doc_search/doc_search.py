#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 16:40:10 2018

@author: cn@cameronneylon.net
"""

from doc_search import ccat_utils
from doc_search import search
import re
import datetime

class Model(ccat_utils.Catalog):
    """Model Class for the General Web Document Search Notebook App
    
    """
    
    def __init__(self,
                 unilistfile = None,
                 searchterm = None,
                 outfilepath = None,
                 includeuniurl = True,
                 continuing=False,
                 grid_dir = None):

        super().__init__(outfilepath=outfilepath,
                         fieldnames = ['id', 'name', 'grid_link', 
                                       'searchterm', 
                                       'search_datetime', 'searchrank', 
                                       'url', 'pagename', 'download_file',
                                       'download_datetime']
                         )
        self.unilistfile = unilistfile
        self.searchterm = searchterm
        self.includeuniurl = includeuniurl
        self.grid_dir = grid_dir
        self.cursor = 0
        self.advOperators = None
        self._init_text = 'Ready for first search'
        self.select_options = 5
        
        if self.unilistfile:
            self.load_unilist()
            if self.outfilepath: 
                self.load_catalog()
                for i, gid in enumerate([u['id'] for u in self.unilist.unis]):
                    if gid not in [u['id'] for u in self.catalog]:
                        self.cursor = i
                        break

            if self.searchterm:
                self.run_search()
        
    def load_unilist(self):
        self.unilist = ccat_utils.UniversityList(list = self.unilistfile,
                                                 loadgrid = True,
                                                 immediatefilter = True,
                                                 core_data_dir = self.grid_dir)
            
    def run_search(self):
        try:
            uni = self.unilist.unis[self.cursor]
        except IndexError:
            self.most_recent_response = 'Reached end of list'
            return False
        query = self.construct_search(uni)
        self.most_recent_response = search.BingWebSearch(query)
        return True

    def construct_search(self, uni):
        uniwebsites = uni.get('links')
        if uniwebsites and self.includeuniurl:
            regex = re.compile('https?:\/\/(?:www\d?)*(?:en)*\.?(?:en\.)*(([\w-]*\.)*([\w-]*))\/?.*')
            sites = []
            for site in uniwebsites:
                m = regex.search(site)
                sites.append(m.group(1))
            sites_for_search = '(site:{})'.format(' OR site:'.join(sites))
            
        else:
            uniwebsites = ''
            
        term = self.searchterm
        term = term.format(**uni)
        full_query = '({}) AND {}'.format(term, sites_for_search)
        self.last_full_query = full_query
        return full_query    

    def process_selection(self):
        uni = self.unilist.unis[self.cursor]

        if uni.get('links'):
            link = ",".join([s for s in uni.get('links')])
        else: link = None
        row = {'id' : uni.get('id'),
               'name' : uni.get('name'),
               'grid_link' : link,
               'searchterm' : self.most_recent_response.search_query,
               'search_datetime' : datetime.datetime.utcnow().isoformat() #todo record this from search response
               }
                
        if self.current_selection:
            for selected in self.current_selection:
                rank = selected # Note that selected is a 1-based index
                i = rank - 1
                results = self.most_recent_response.results
                url = results[i].url
                pagename = results[i].name
                
                row.update({'url' : url,
                            'searchrank' : rank,
                            'pagename' : pagename})
                self.save_append(row)
        else:
            self.save_append(row)


    def next_uni(self):
        self.process_selection()        
        self.cursor += 1
        self.clear_current_selection()
        success = self.run_search()
        return success
        
    def previous_uni(self):
        if self.cursor > 0:
            self.cursor -=1
            self.clear_current_selection
            self.run_search()
        #todo deactivate the 'previous' button because can only go back once

    @property
    def most_recent_response(self):
        try:
            return self._most_recent_response
        except AttributeError:
            return None
    
    @most_recent_response.setter
    def most_recent_response(self, response):
        self._most_recent_response = response

    @property
    def searchterm(self):
        try:
            return self._searchterm
        except AttributeError:
            return None
        
    
    @searchterm.setter
    def searchterm(self,searchterm):
        self._searchterm = searchterm
        
    @property
    def current_selection(self):
        try:
            return self._current_selection
        except AttributeError:
            return None

            
    def toggle_selection(self,selection):
        if not self.current_selection:
            self._current_selection = [] 
            
        if selection in self._current_selection:
            self._current_selection.remove(selection)
            return
        
        if type(selection) == int:
            self._current_selection.append(selection)
            
        elif type(selection) == str:
            self._current_selection.append(selection)

        elif type(selection) == list:
            self._current_selection.extend(selection)
            
        self._current_selection.sort()
        #print(self.current_selection)


    def clear_current_selection(self):
        self._current_selection = None
        
if __name__ == '__main__':
    test_clean_init = Model()
    test_with_unilist = Model(unilistfile = '../core_data/pilotunilist.csv')
    test_with_searchterm = Model(unilistfile = '../core_data/pilotunilist.csv',
                                 searchterm = '"open access policy"',
                                 outfilepath = 'test_data/test_catalog.csv')
#    test_with_searchterm.cursor = 0
    print(test_with_searchterm.cursor)
    print(test_with_searchterm.most_recent_response)
    print('running search')
    success = test_with_searchterm.run_search()
#    print(success)
#    print(test_with_searchterm.most_recent_response)
#    print(test_with_searchterm.most_recent_response.results[0].name)
#    print(test_with_searchterm.next_uni())
#    print(test_with_searchterm.most_recent_response.results[0].name)
#    test_with_searchterm.previous_uni()
#    print(test_with_searchterm.current_selection)
    test_with_searchterm.add_selection(3) 
    test_with_searchterm.add_selection(1)
    print(test_with_searchterm.current_selection)
    test_with_searchterm.next_uni()                                                 
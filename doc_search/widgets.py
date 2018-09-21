#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 17:26:52 2018

@author: cameronneylon
"""

import ipywidgets as wd

class SelectionWidget:
    """Three part widget for text information, selection, and activation
    
    """
    
    def __init__(self, model=None):
        
        if model:
            self.model = model
            self._init_text(self.model._init_text)
            self._init_selection(n = self.model.select_options)
            self._init_progress(len(self.model.unilist.unis), 
                                self.model.cursor)
            self.text_print_new()
            
        self._init_next()


        self.widget = wd.VBox([self._progress, self._text, self._selection, self._next])
        display(self.widget)


    def _init_progress(self, total, progress):
        self._progress_bar = wd.IntProgress(min = 0,
                                        max = total,
                                        value = progress,
                                        step = 1,
                                        description = "Progress")
        self._progress_label = wd.Label(value = self.format_progress_label(
                                             total, progress))
        self._progress = wd.HBox([self._progress_bar, self._progress_label])

        
    def _init_text(self, text):
        self._text = wd.Output(layout=wd.Layout(height='45em',
                                                border='solid'))
        with self._text:
            print(text)

    
    def _init_selection(self, n=None, names=None):
        if n:
            labels = list(range(1,n+1))
        if names:
            labels = names
            
        selection_buttons = []
        for label in labels:
            b = wd.Button(description=str(label))
            selection_buttons.append(b)
            b.on_click(self.on_selection_button_clicked)
            
        none_selection = wd.Button(description='None')
        selection_buttons.append(none_selection)
        none_selection.on_click(self.none_selection_button_clicked)

        self._selection = wd.HBox(selection_buttons)        


    def _init_next(self, buttons=['Next', 'Previous'], 
                         styles = ['primary', 'danger']):
        next_buttons = []
        for i, label in enumerate(buttons):
            b = wd.Button(description=label,
                          button_style=styles[i])
            next_buttons.append(b)
            b.on_click(self.on_next_button_clicked)
            
        self._next = wd.HBox(next_buttons)


    def on_selection_button_clicked(self,b):
        if b.style.button_color == 'lightgray':
            b.style = wd.ButtonStyle()
            
        else:
            b.style.button_color = 'lightgray'

        s = b.description
        if s.isdigit():
            s = int(s)
        self.model.toggle_selection(s)

    
    def none_selection_button_clicked(self,b):
        self.clear_selection_buttons()


    def clear_selection_buttons(self):
        for button in self._selection.children:
            button.style = wd.ButtonStyle()
            
        self.model.clear_current_selection()

        
    def on_next_button_clicked(self,b):
        if b.description == 'Next':
            self.next_item(b)
        if b.description == 'Previous':
            self.previous_item()

    def next_item(self, b):
        self._text.clear_output()
        with self._text:
            print('Running search...')
        another_result = self.model.next_uni()
        self.clear_selection_buttons()
        self.update_progress()
        if another_result:
            self.text_print_new()                
        else:
            self._text.clear_output()
            with self._text:
                print('Finished List')
                b.disabled = True
            
        
    def previous_item(self):
        self._text.clear_output()
        with self._text:
            print('Running search...')
        self.model.previous_uni()
        self.text_print_new()
        self.update_progress()       


    def text_print_new(self):
        self._text.clear_output()
        if self.model.most_recent_response.results:
            selection_text = self.format_choice_list(
                                 self.model.most_recent_response.results)
        else:
            selection_text = 'No results received for search {}'.format(
                                    self.model.last_full_query)
        with self._text:
            print(selection_text)


    def update_progress(self):
        self._progress_bar.value = self.model.cursor
        self._progress_label.value = self.format_progress_label(
                                            len(self.model.unilist.unis),
                                            self.model.cursor)
        
    def format_progress_label(self, total, progress):
        return "{} of {} universities remaining".format(str(total-progress),
                                            str(total))
        

    def format_choice_list(self, items):
        """Format the set of lists based on a list of dicts and keys to show
        
        Structured to work on the responses from a Bing Search given by the
        seach module. The keys for elements to display are current hard
        coded here but should probably be a class variable for future
        flexibility.
        """
        
        text = "Search Term: {}\n\n".format(self.model.last_full_query)
        keys = ['rank', 'name', 'url', 'snippet']
        for i,item in enumerate(items):
            try:
                text += self.format_choice(item, keys)
            except AttributeError:
                item.raw_result['rank'] = str(i+1)
                text += self.format_choice(item.raw_result, keys)
            text += '\n'
        return text

    def format_choice(self, itemdict, keys):
        """Format a single option based on a dict and set of keys"""
        
        t = ""
        for key in keys:
            t = t + '{}: {}\n'.format(key,itemdict.get(key, 'n/a'))
            
        return t

    
class MockModel:
    """A Mock Model Class for Testing the Widget"""
    
    def __init__(self):
        self._init_text = 'MockModel Test text'
        self.select_options = 5
        self.cursor = 0
        self.most_recent_response = MockResponse()
        self.unilist = MockUniList()
    
        
    def clear_current_selection(self):
        pass
    
    def next_uni(self):
        self.cursor +=1
        return True
    
    def previous_uni(self):
        if self.cursor > 0:
            self.cursor -= 1
    
    def add_selection(self,s):
        pass

class MockResponse:
    """Mock Response Class for Testing the Widget"""
    
    def __init__(self):
        self._init_text = 'MockResponse Init Text'
        self.results = [{'rank' : '1',
                      'name' : 'test_name_1',
                      'url' : 'http://example.com',
                      'snippet' : 'a snippet'},
                     {'rank' : '2',
                      'name' : 'test_name_2',
                      'url' : 'http://example.com',
                      'snippet' : 'a snippet'},
                     {'rank' : '3',
                     'name' : 'test_name_3',
                     'url' : 'http://example.com',
                     'snippet' : 'a snippet'},
                     {'rank' : '4',
                     'name' : 'test_name_4',
                     'url' : 'http://example.com',
                     'snippet' : 'a snippet'}
                     ]
        

class MockUniList:
    def __init__(self):
        self.unis = [1,2,3,4,5,6,7,8,9,10]


if __name__ == '__main__':
    test = SelectionWidget(n=4, text='test')
    
        
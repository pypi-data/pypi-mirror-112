'''
Utils class
'''
import json
import re
import pandas as pd

class Utils():
    '''
    Common functions holder
    '''
    @classmethod
    def to_camel_case(cls, snake_str, joining='_'):
        '''
        Translate from Python Code to JavaScript
        Parameter:
            snake_str: Python name convention
            joining: sign joinig string in python name
        Return: JavaScript name convention
        '''
        if snake_str == '_id':
            return snake_str
        components = snake_str.split(joining)
        return components[0] + ''.join(x.title() for x in components[1:])

    @classmethod
    def to_snake_case(cls, camel_str):
        '''
        Translate from JavaScript to Python
        Parameter:
            camel_str: JavaScript name convention
        Return: Python name convention
        '''
        if camel_str == '_id':
            return camel_str
        return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()

    @classmethod
    def output_form(cls, class_, data_list, output):
        '''
        Transform a data to standardised format, default DataFrame
        Parameter:
            class_: format class to transform (list, set, tuple, numpy, etc.)
            data_list: data to transform
            output: name of the format in string so that don't need to pass a class object in class_
            (currently support only 'DataFrame')
        Return: corresponding data in chosen format
        '''
        if not data_list:
            return []
        if output == 'DataFrame':
            return pd.DataFrame(data_list)
        else:
            return [class_(instance) for instance in data_list]

    @classmethod
    def build_filter_params_v0(cls, filter_, pre_character='&'):
        '''
        Transform a dictionary to a string with the format: "&key_1[$regex]=x&val_1[$options]=i"
        for each member in the list and joining members by '&'
        Parameter:
            filter: dictionary to transform
            pre_character: character linking each option (default: '&')
        '''
        if not filter_:
            return ''
        result = pre_character
        if 'EXACT' in filter_:
            del filter_['EXACT']
            for key in filter_:
                result += f'{key}={filter_[key]}&'
        else:
            for key in filter_:
                result += f'{key}[$regex]={filter_[key]}&{key}[$options]=i&'
        return result[:-1]

    @classmethod
    def build_filter_params(cls, filter_, page=1, limit=1000):
        '''
        Build query params object to pass to request.get(query_params=?)
        Parameter:
            filter: dictionary of query conditions
            page, limit: for pagination
        '''
        query_params = {}
        if filter_ and type(filter_) is dict:
            for key in filter_:
                query_params[f'filter[{key}]'] = filter_[key]
        query_params['page'] = page
        query_params['limit'] = limit
        return query_params

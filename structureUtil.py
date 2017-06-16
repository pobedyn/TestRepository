import re
from bs4 import BeautifulSoup
import argparse
import requests
from collections import Counter
import urllib.request

class StructureUtil:
    # Getting a string form given tag (p-tag or div-tag).  
    def get_string(tag):
        string = ''
        string = tag.text.strip()
        return string      

    # Checking string for emptiness.  
    def is_empty(string):
        string = re.sub(' ', '', string)
        return (len(string) == 0)

    # Return the number of occurrences of the attribute in given attribute dictionary.  
    def get_attribute_frequency(attributeDictionary):
        result = {}
        for value in attributeDictionary.values():
            try:
                result[value] = result[value] + 1
            except:
                result[value] = 1
        return result

    # Return a dictionary with marks for atrributes, 
    # according to how often they are occur.  
    def get_typical_values(attributeDictionary):
        result = {}
        typicalVal = len(attributeDictionary)
        while len(attributeDictionary.keys()) > 0:
            minVal = attributeDictionary[list(attributeDictionary.keys())[0]]
            minKey = list(attributeDictionary.keys())[0]
        
            for key in attributeDictionary.keys():
                if attributeDictionary[key] < minVal:
                    minVal = attributeDictionary[key]
                    minKey = key
            result[minKey] = typicalVal
            typicalVal = typicalVal - 1
            attributeDictionary.pop(minKey)
        return result

    # Return font-size from given tag (p or div).  
    def get_string_size (tag):
        size = ''
        
        sub_result = re.split(r'font-size:', str(tag))
        if len(sub_result) > 1:
            size = re.split(r'pt|px', str(sub_result[1]))[0]
        else:
            size = '0'
        
        if size == '0' and tag.font:
            try:
                size = tag.font['size']
            except:
                size = '0'
        return size

    # Return font-style from given tag (p or div).  
    def get_string_style (tag):
        style = ''
        sub_result = re.split(r'font-family:', str(tag))
        if len(sub_result) > 1:
            style = re.split(r'"|;', str(sub_result[1]))[0]
        else:
            style = 'None'
        if style == 'None' and tag.font:
            try:
                style = tag.font['style']
            except:
                style = 'None'
        return style


    # Return text-align from given tag (p or div).  
    def get_string_align (tag):
        align = ''
        try:
            align = tag['align']
        except:
            align = 'None'
        if align == 'None':
            sub_result = re.split(r'text-align:', str(tag))
            if len(sub_result) > 1:
                align = re.split(r'"|;', str(sub_result[1]))[0]
            else:
                align = 'None'
                
        return align

    # Check whether given tag has bold text.  
    # If it does - return 'b', otherwise - return 'None'.  
    def get_string_bold (tag):
        bold = ''
        
        sub_result = re.split(r'bold', str(tag))
        if len(sub_result) > 1:
            bold = 'b'
        else:
            bold = 'None'
        
        if bold == 'None':
            bold = ('None', 'b')[tag.b != None]
        return bold

    # Check whether given tag has italic text.  
    # If it does - return 'i', otherwise - return 'None'.  
    def get_string_italic (tag):
        italic = ''
        
        sub_result = re.split(r'italic', str(tag))
        if len(sub_result) > 1:
            italic = 'i'
        else:
            italic = 'None'
        
        if italic == 'None':
            italic = ('None', 'i')[tag.i != None]
        return italic

    # Check whether given tag has underlined text.  
    # If it does - return 'u', otherwise - return 'None'.  
    def get_string_underline (tag):
        underline = ''
        
        sub_result = re.split(r'underline', str(tag))
        if len(sub_result) > 1:
            underline = 'u'
        else:
            underline = 'None'
        
        if underline == 'None':
            underline = ('None', 'u')[tag.u != None]
        return underline

    # Check whether given tag has text in upper case.  
    # If it does - return True, otherwise - return False.  
    def get_string_upper(tag):
        isUpper = ''
        isUpper = tag.text.strip().isupper()
        return isUpper

    # Erase from typDict all dublicate lines and
    # lines with only numbers.  
    def clear_typDict(typDict, tags):
        prevStk = list(typDict.keys())[0]
        for stk in list(typDict.keys())[1:]:
            if tags[stk].text.strip().isdigit():
                typDict.pop(stk)
                continue
            if tags[stk].text.strip() == tags[prevStk].text.strip():
    #             print(dTags[stk].text.strip())
                typDict.pop(stk)
                typDict.pop(prevStk)
                prevStk = 0
            else:
                prevStk = stk

    # using urllib for reading html.  
    def get_html(link): 
        return(urllib.request.urlopen(link).read())      
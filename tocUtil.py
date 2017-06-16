import re
from bs4 import BeautifulSoup
import argparse
import requests
from collections import Counter
import urllib.request

class TocUtil:

 
    # Create dictionary witch consist text as a key and level of nesting as value.  

    def table_of_content_estimation(result): 
        TOC = {} 
        for i in range(0, len(result)): 
            if 'PART' in result[i].upper(): 
                TOC.update({result[i]: 0}) 
            elif 'ITEM' in result[i].upper(): 
                TOC.update({result[i]: 1}) 
            else: 
                TOC.update({result[i]: 2}) 
        return(TOC)


    # Withdrawal table of content from document.  
    # Finding table from first part of document with max concenration of items.  
    # Extract the corresponding table into my_table. 

    def get_table_of_content(html):
        soup = BeautifulSoup(html, 'html5lib')
        tables = soup.findChildren('table')
        gettable = []
        for i in range(0, round(len(tables)/2)):   
            result = re.findall(r'(?:Item|ITEM|PART|Part)', tables[i].text.strip())
            gettable.append(len(result))
        my_table = tables[gettable.index(max(gettable))]
        return(my_table)

    # Cut the table text into sentences.  
    # Deleting unwanted symbols from sentences.  
	
    def create_sentences(my_table):
        rows = my_table.findChildren(['th', 'tr'])
        sentences = []
        for i in range(0, len(rows)):
            if len(rows[i]) == 0:
                continue
            if i == 0:
                result = re.findall(r'(?:Item|ITEM|PART|Part)', rows[i].text.strip())
                if len(result) == 0:
                    continue
            cols = rows[i].find_all('td')
            cols = [ele.text.strip() for ele in cols]
            sentences.append([ele for ele in cols if ele]) 
        for i in range(0, len(sentences)):
            if len(sentences[i]) == 0:
                continue
            sentences[i][0] = re.sub('[^\x00-\x7F]+', '', sentences[i][0])    
        return(sentences)

    # Deleting empty strings symbols from sentences.  
    # Deleting page numbers.  
	
    def create_contents(sentences):
        ss=[]
        for i in range(0, len(sentences)):
            if len(sentences[i]) == 0:
                continue
            ss.append(sentences[i])
        contents = []
        for i in range(0, len(ss)):
            for k in range(0, len(ss[i])):
                result = re.findall(r'\w[-,][\d]', ss[i][k])
                if ss[i][k].isdigit() or len(result) != 0:
                    continue
                contents.append(ss[i][k])
        return (contents)

    # Remove unnecessary information from the title of table of contents. 

    def get_result(contents):
        start = 0
        getstart = False
        for i in range(0, len(contents)):
            if 'PART' in contents[i].upper() and not getstart:
                start = i
                getstart = True 
        result = []
        for i in range(start, len(contents)):
            result.append(contents[i])
        return(result)

    # Using urllib for reading html.  

    def get_html(link):
        return(urllib.request.urlopen(link).read())

    # If the result is very small or there is no concentration of items in it  
    # Reduce the content table search to the first 20.  

    def correction(html):
        soup = BeautifulSoup(html, 'lxml')
        tables = soup.findChildren('table')
        gettable = []        
        gettable = tables.index(max(tables[0:20], key=len))
        my_table = tables[gettable]
        rows = my_table.findChildren(['th', 'tr'])
        sentences = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            sentences.append([ele for ele in cols if ele]) 
        start = 0
        for i in range(0, len(sentences)):
            if len(sentences[i]) == 0:
                continue        
            sentences[i][0] = re.sub('[^\x00-\x7F]+', '', sentences[i][0])
        contents = create_contents(sentences)
        return(contents)
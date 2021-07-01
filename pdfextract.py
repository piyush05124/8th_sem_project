#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PyPDF2 as pdf
import cv2
import os
import pprint
import json
import re # REGULAR EXPRESSION


# In[110]:


def pdftext(filepath,pno):
    li=[]
    try:
        if filepath.endswith('.pdf'):
            reader=pdf.PdfFileReader(filepath)
            pnum=reader.getNumPages() # TOTAL PAGE
            pg=reader.getPage(int(pno)) # SINGLE PAGE
            page=pg.extractText().splitlines() # SPLITLINES FOR PROPER FORMATING
            print(page)
            for i in page:
                g=re.findall(r'[a-z, A-z, 0-9, : ,/,*, ., \n]',i)
                li.append(''.join(g))
            for j in li:
                if j=='':
                    li.remove(j)  # USED FOR REMOVING EXTRA SPACES  
            return ''.join(li) # LIST TO STRING 
        else:
            return 'please upload pdf file'
    except IndexError:
        return "Page number not found, total number of pages are: {}".format(pnum)
    except TypeError:
        return "enter page no"


# In[ ]:





from tkinter import *
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import urllib.request
import sys
from os import listdir
from os.path import isfile, join
import os
dir_name=sys.argv[0].split('/')[:-1]
dir_name='/'.join(dir_name)
onlyfiles = [f for f in listdir(dir_name) if isfile(join(dir_name, f))]
for file in onlyfiles:
    ext=file.split('.')[-1]
    if ext != 'py':
        os.remove(file)
############  Main layout  ##################
main_window=Tk()
main_window.title('Live News Feed')
main_window.state('zoomed')
main_window.resizable(0,0)
menu=Menu(main_window)
main_window.config(menu=menu)
text=Text(main_window,width=1366,height=768)
scrollbar =Scrollbar(main_window)
scrollbar.pack(side=RIGHT,fill=Y)
scrollbar.config(command=text.yview)
text.config(yscrollcommand=scrollbar.set)
text.pack()
#############################################
genere_map=\
{
'Nation':'http://zeenews.india.com/rss/india-national-news.xml',
'World':'http://zeenews.india.com/rss/world-news.xml',
'States':'http://zeenews.india.com/rss/india-news.xml',
'Asia':'http://zeenews.india.com/rss/asia-news.xml',
'Business':'http://zeenews.india.com/rss/business.xml',
'Sports':'http://zeenews.india.com/rss/sports-news.xml',
'Science & Environment':'http://zeenews.india.com/rss/science-environment-news.xml',
'Entertainment':'http://zeenews.india.com/rss/entertainment-news.xml',
'Health':'http://zeenews.india.com/rss/health-news.xml',
'Technology':'http://zeenews.india.com/rss/technology-news.xml'
}
genere_list=\
[
'Nation',
'World',
'States',
'Asia',
'Business',
'Sports',
'Science & Environment',
'Entertainment',
'Health',
'Technology'
]
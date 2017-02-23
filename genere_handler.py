from config import *
import threading
import html
import urllib.request
from PIL import Image,ImageTk
curr_thread_name=''
from tkinter import font
class thread(threading.Thread):
    def __init__(self,genere):
        super(thread, self).__init__()
        self.genere=genere
        self.daemon=True
    def run(self):
        if self.genere is 'Home':
            home_handler(self.name)
        else:
            genere_handler(self.genere,self.name)
def threader(genere):
    t=thread(genere)
    global curr_thread_name
    curr_thread_name = t.name
    t.start()
def convert(string):
    return html.unescape(str(string).replace('&amp;','&'))
def convert_date(date):
    date=date.split(', ')
    date[1]=date[1].split()
    date[3]=date[3].split()
    date=date[1:]
    month_map={
        'January':'1',
        'February':'2',
        'March':'3',
        'April':'4',
        'May':'5',
        'June':'6',
        'July':'7',
        'August':'8',
        'September':'9',
        'October':'10',
        'November':'11',
        'December':'12'
    }
    date[0][0]=month_map[date[0][0]]
    date=(date[1]+'/'+date[0][0]+'/'+date[0][1]+' '+date[2][0])
    return date
def return_key(x):
    try:
        return x.pubDate.string
    except:
        return x.pubdate.string
def home_handler(thread_name):
    # end####
    if thread_name != curr_thread_name:
        return
    ########
    # Text window for a Home
    text_view = text
    text_view.config(state=NORMAL)
    text_view.delete('1.0', END)
    text_view.config(state=DISABLED)
    # end####
    if thread_name != curr_thread_name:
        return
    ########
    items=list()
    print('1--')
    for genere in genere_map:
        # end####
        if thread_name != curr_thread_name:
            return
        ########
        base_url = genere_map[genere]
        # source_code = urllib.request.urlopen(base_url).read()
        #
        print('2--')
        source_code = urllib.request.urlopen(base_url)
        print('3--')
        count = 1
        eff_source = ''
        for line in source_code:
            if count <= 50:
                eff_source = eff_source + str(line.decode('utf-8'))
            else:
                break
            count = count + 1
        source_code = eff_source
        #
        # end####
        if thread_name != curr_thread_name:
            return
        ########
        print('4--')
        soup = BeautifulSoup(source_code, 'xml')
        print('5--')
        curr_item=soup.find('item')
        next_item=curr_item.findNext('item')
        items.append(curr_item)
        items.append(next_item)
    # end####
    if thread_name != curr_thread_name:
        return
    ########
    print('6--')
    items.sort(key=lambda x:convert_date(return_key(x)),reverse=True)
    print('7--')
    latest_count=1
    for item in items:
        if latest_count==6:
            break;
        link = item.link.string
        # end####
        if thread_name != curr_thread_name:
            return
        ########
        print('8--')
        article_source = urllib.request.urlopen(link)
        # end####
        if thread_name != curr_thread_name:
            return
        ########
        print('9--')
        count = 1
        eff_source = ''
        for line in article_source:
            if count >= 700 and count <= 1000:
                eff_source = eff_source + str(line.decode('utf-8'))
            else:
                if count > 1000:
                    break
            count = count + 1
        article_source = eff_source
        only_req_div_tag = SoupStrainer('div')
        # end####
        if thread_name != curr_thread_name:
            return
        ########
        print('10--')
        article_soup = \
            BeautifulSoup(article_source, 'html.parser', parse_only=only_req_div_tag)
        print('11--')
        article_content = \
            article_soup.findAll('div', {'class': ['field-item', 'even']})
        if len(article_content) == 2:
            article_img_soup = article_content[0]
            article_text_soup = article_content[1]
        else:
            article_img_soup = 'None'
            article_text_soup = article_content[0]
        article_title = convert(item.title.string) + '\n'
        # Try catch due to weird behaviour of pubdate in rss
        try:
            article_date = convert(item.pubDate.string) + '\n'
        except:
            article_date = convert(item.pubdate.string) + '\n'
        ###############################################
        article_text = ''
        temp=article_text_soup.findAll('p')
        for p in temp:
            if p.string is p.contents[0]:
                article_text += convert(p.string) + '\n'
        if thread_name == curr_thread_name:
            text_view.config(state=NORMAL)
            topic_font = font.Font(weight='bold')
            start = text_view.index('insert')
            text_view.insert(END, article_title)
            end = text_view.index('insert')
            print(start + ' ' + end)
            text_view.tag_add('title', start, end)
            text_view.tag_config('title', font=topic_font)
            if article_img_soup is not 'None':
                url=article_img_soup.img['src']
                complete_img_name=url.split('/')[-1]
                urllib.request.urlretrieve \
                    (url,complete_img_name)
                image = Image.open(complete_img_name)
                photo = ImageTk.PhotoImage(image)
                label = Label(image=photo)
                label.image = photo  # keep a reference!
                label.pack()
                text_view.image_create(END,image=photo)
            text_view.tag_add('wrap', '1.0', 'end')
            text_view.tag_config('wrap', wrap=WORD)
            text.insert(END, '\n')
            text_view.insert(END, article_date)
            text_view.insert(END, article_text)
            text_view.insert(END, '---------------------------------\n')
            text_view.update_idletasks()
            text_view.config(state=DISABLED)
        else:
            return
def genere_handler(genere,thread_name):
    #end####
    if thread_name!=curr_thread_name:
        return
    ########
    # Text window for a genere of articles
    text_view = text
    text_view.config(state=NORMAL)
    text_view.delete('1.0', END)
    text_view.config(state=DISABLED)
    base_url=genere_map[genere]
    print('1--')
    source_code = urllib.request.urlopen(base_url).read()
    print('2--')
    # end####
    if thread_name != curr_thread_name:
        return
    ########
    soup=BeautifulSoup(source_code,'xml')
    print('3--')
    items=soup.findAll('item')
    # end####
    if thread_name != curr_thread_name:
        return
    ########
    for item in items:
        link=item.link.string
        # end####
        if thread_name != curr_thread_name:
            return
        ########
        print('4--')
        article_source=urllib.request.urlopen(link)
        # end####
        if thread_name != curr_thread_name:
            return
        ########
        print('5--')
        count=1
        eff_source=''
        for line in article_source:
            if count>=700 and count<=1000:
                eff_source=eff_source+str(line.decode('utf-8'))
            else:
                if count>1000:
                    break
            count=count+1
        article_source=eff_source
        print('6--')
        only_req_div_tag=SoupStrainer('div')
        print('7--')
        # end####
        if thread_name != curr_thread_name:
            return
        ########
        article_soup=\
        BeautifulSoup(article_source,'html.parser',parse_only=only_req_div_tag)
        print('8--')
        article_content=\
            article_soup.findAll('div',{'class':['field-item','even']})
        if len(article_content)==2:
            article_img_soup=article_content[0]
            article_text_soup=article_content[1]
        else:
            article_img_soup ='None'
            article_text_soup = article_content[0]
        article_title=convert(item.title.string)+'\n'
        # Try catch due to weird behaviour of pubdate in rss
        try:
            article_date =convert(item.pubDate.string)+'\n'
        except:
            article_date =convert(item.pubdate.string)+'\n'
        ###############################################
        article_text=''
        for p in article_text_soup.findAll('p'):
            if p.string is p.contents[0]:
                article_text +=convert(p.string)+'\n'
        if thread_name == curr_thread_name:
            text_view.config(state=NORMAL)
            topic_font = font.Font(weight='bold')
            start = text_view.index('insert')
            text_view.insert(END, article_title)
            end = text_view.index('insert')
            text_view.tag_add('title', start, end)
            text_view.tag_config('title', font=topic_font)
            if article_img_soup is not 'None':
                url = article_img_soup.img['src']
                complete_img_name = url.split('/')[-1]
                urllib.request.urlretrieve \
                    (url, complete_img_name)
                image = Image.open(complete_img_name)
                photo = ImageTk.PhotoImage(image)
                label = Label(image=photo)
                label.image = photo  # keep a reference!
                label.pack()
                text_view.image_create(END, image=photo)
            text_view.tag_add('wrap', '1.0', 'end')
            text_view.tag_config('wrap', wrap=WORD)
            text.insert(END,'\n')
            text_view.insert(END, article_date)
            text_view.insert(END, article_text)
            text_view.insert(END, '---------------------------------\n')
            text_view.update_idletasks()
            text_view.config(state=DISABLED)
        else:
            return
from genere_handler import threader
from config import *
menu.add_cascade(label='Home',command=lambda g='Home':threader(g))
for genere in genere_list:
    menu.add_cascade\
        (label=genere,
         command=lambda g=genere:threader(g))
text.pack(side=LEFT,fill=Y)
threader('Home')
main_window.mainloop()
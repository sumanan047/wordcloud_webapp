# total package for wordcloud

# dependecies for the package
import random
import string
import os
from PyPDF2 import PdfFileReader                                   # to extract text from pdf
import wordcloud                                                   # to create wordcloud
from wordcloud import WordCloud,ImageColorGenerator, STOPWORDS     # for image color masking
import numpy as np                                                 # for generating the pixels 
from matplotlib import pyplot as plt                               # for image show and plotting 
#from IPython.display import display                                # to display in jupyter environement
import re                                                          # for removing punctuations etc.
from bs4 import BeautifulSoup                                      # to parse the html document
from bs4.element import Comment                                    # for element interacting in html
import urllib.request                                              # to accept url link and work with python on it
from PIL import Image                                              # to create the image mask for wordcloud
import secrets
from pathlib import Path
import base64
from io import BytesIO



#globals

#msk = "default"

#original function
'''
def str_for_image(file=None,url=None):
    if (file!=None and file.endswith('.txt')):
        string=txt_text_extractor(file)
    elif (file!=None and file.endswith('.pdf')):
        string=pdf_text_extractor(file)
    elif (file==None and url!=None):
        html=get_bytes_from_url(url)
        string=text_from_html(html)
    return string
'''

# for checking the extension of the file uploaded

def str_for_image(file):
    if (file.endswith('.txt')):
        string=txt_text_extractor(file)
    elif (file.endswith('.pdf')):
        string=pdf_text_extractor(file)
    return string
        
#for extracting text from pdf files
        
def pdf_text_extractor(f):
    #with open(path, 'rb') as f:
    pdf = PdfFileReader(f)
    page_num=pdf.getNumPages()
    # get the first page
    text=""
    for p in range(page_num):
        page = pdf.getPage(p)
        t = page.extractText()
        text=text+t
    return text


#for extracting text from txt files

def txt_text_extractor(path):
    txt_file = open(path,"r",encoding='utf8', errors='ignore')
    txt=txt_file.read()
    return txt
# for extracting text from webpage link, it takes a url and returns a sting output

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_bytes_from_url(url):
    html=urllib.request.urlopen(url).read()
    return html

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    txt = u" ".join(t.strip() for t in visible_texts)
    return txt

#for creating mask for images

def default_circle_mask():
    x, y = np.ogrid[:600, :600]
    circle = (x - 300) ** 2 + (y - 300) ** 2 > 300 ** 2
    circle = 255 * circle.astype(int)
    default_mask=circle
    image_colors=None
    return default_mask,image_colors

def mask_image(msk):
    image_color = np.array(Image.open(msk)) 
    image_color = image_color[::1, ::1]# variable to provide shape for wordcloud based on image uploaded
    image_colors = ImageColorGenerator(image_color) # variable for recolor wordcloud using mask image
    return image_color,image_colors

def mask_assignment(msk):
    if msk==None:
        mask_,image_colors=default_circle_mask()
    else:
        mask_,image_colors=mask_image(msk)
    return mask_,image_colors


# function for generating word frequencies, string returned by str_for_image is the file_contents

def calculate_frequencies(file_contents):
    # Here is a list of punctuations and uninteresting words you can use to process your text
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    uninteresting_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", \
    "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them", \
    "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being", \
    "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how", \
    "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just","in",\
    "not","for","said","on","thou","one","into","up","then","ye","would","so","must","thee","there","out","back","could",\
                          "again"]
    
    # LEARNER CODE START HERE
    w = {}
    file_contents = re.sub(r'[^\w\s]','',file_contents).lower()
    list_of_words = file_contents.split()
    for word in list_of_words:
        if word not in uninteresting_words:
            if word not in w:
                w[word] = 1
            else:
                w[word] += 1
        else:
            continue
        
    return w

# implementation now begins here with calling str_for_image func to get string from files 

#stg = str_for_image(url='https://www.cnn.com/2020/06/16/tech/nasa-kirk-shireman-iss-scn/index.html')   

#tup = (max_words=1000,background_color = "white",scale=2,contour_color="black",contour_width=1)



def Wd(cloud,stg,msk):
    file_contents=stg
    w = calculate_frequencies(file_contents)
    cloud.generate_from_frequencies(w)
    
    if msk==None:
        image_colors=None
    else:
        image_colors = ImageColorGenerator(mask_assignment(msk)[0])
    cloud.recolor(color_func=image_colors)    
    return cloud.to_array()    


# function for returning the final wodcloud image, the file_contents come from str_for_image function, so has to be run before 
# this function


def image_return(file_contents,img_mask,bg="black",max_words=1000,s=4,c_color="grey",c_width=1):
    temp_mask = mask_assignment(img_mask)[0]
    cloud=wordcloud.WordCloud(max_words=max_words,mask=temp_mask,background_color = bg,scale=s,contour_color=c_color,contour_width=c_width)
    myimage = Wd(cloud,file_contents,img_mask)
    plt.figure( figsize=(10,7) )
    plt.imshow(myimage, interpolation = 'nearest')
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format="png")
    return buf

'''

def image_return(file_contents,bg="black",img_mask=mask_assignment(msk)[0],max_words=1000,s=4,c_color="grey",c_width=1):
    cloud=wordcloud.WordCloud(max_words=max_words,mask=img_mask,background_color = bg,scale=s,contour_color=c_color,contour_width=c_width)
    myimage = Wd(cloud,file_contents)
    plt.figure( figsize=(10,7) )
    plt.imshow(myimage, interpolation = 'nearest')
    plt.axis('off')
    filep = Path("wd_app\static")
    rand_name = secrets.token_hex(8)
    f_ext = ".jpg"
    file_name=rand_name+f_ext
    filepath = filep/file_name
    plt.savefig(filepath,dpi=600) 
    return filepath,file_name

'''
#############################################################
# the other file wd_1 uses the original approach without Byte stream
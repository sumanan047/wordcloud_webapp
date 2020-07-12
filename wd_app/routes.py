import os
from flask import render_template, url_for,request,flash
from wd_app import app
from wd_app import forms
#from wd_app.models import Userdata
from wd_app.wd_cloud import image_return # this is the randomw filename created for the image to be displayed
from wd_app.wd_cloud import pdf_text_extractor,get_bytes_from_url,text_from_html
import base64
import io
from io import BytesIO
from PIL import Image

def get_string_from_text(file_string):
    if (file_string.content_type=='text/plain'):
        file_data=file_string.stream.read().decode()
        stg=file_data
    return stg

def get_string_from_pdf(file_string):
    text=pdf_text_extractor((io.BytesIO(file_string.read())))
    stg=text
    return stg


def form_for_image():
    if request.method=="POST":
        #color input
        color_name = request.form['color']
        #max_word data
        max_word_data = int(request.form['max_word'])
        #contour color
        cont_color= request.form['contour_color']
        # scale input 
        scale_data = int(request.form['scale'])
        #image for masking upload
        image_storage = request.files['image'] 
        if (image_storage.filename==""):
            image_bt_io=None
        else:
            #image_name=image_storage.filename   # this is for filename in case I want to use it
            image_bt_io=BytesIO(image_storage.stream.read())


        # the flag is to read input type
        flag=request.form['request_index']
        if(flag=="1"):
            #file upload part
            file_storage = request.files['file']
            file_name = file_storage.filename
            if (file_name==""):                                                    # for user not providing any file
                src=None
                flash('You must provide a file in order to generate a wordcloud, taking you back to home screen!')
            elif (file_name.endswith('.txt')):
                stg=get_string_from_text(file_storage)
                buf=image_return(stg,image_bt_io,bg=color_name,c_color=cont_color,max_words=max_word_data,s=scale_data)
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                #return f"<img src='data:image/png;base64,{data}'/>"
                src = 'data:image/png;base64,'+data
            elif (file_name.endswith('.pdf')):
                stg=get_string_from_pdf(file_storage)
                buf=image_return(stg,image_bt_io,bg=color_name,c_color=cont_color,max_words=max_word_data,s=scale_data)
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                src = 'data:image/png;base64,'+data
        elif(flag=="2"):
            #text box input
            text_storage = request.form['modal_text']
            if (text_storage==""):                                                  # for user not providing any text
                src=None
                flash('You must provide some text in order to generate a wordcloud, taking you back to home screen!')
            else:
                stg=text_storage
                buf=image_return(stg,image_bt_io,bg=color_name,c_color=cont_color,max_words=max_word_data,s=scale_data)
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                #return f"<img src='data:image/png;base64,{data}'/>"
                src = 'data:image/png;base64,'+data
        elif(flag=="3"):
            #web url input
            url = request.form['url_data']
            if (url==""):                                                               # for user not providing any url
                src=None
                flash('You must provide a valid url in order to generate a wordcloud, taking you back to home screen!')
            else:
                html=get_bytes_from_url(url)
                stg=text_from_html(html)
                buf=image_return(stg,image_bt_io,bg=color_name,c_color=cont_color,max_words=max_word_data,s=scale_data)
                data = base64.b64encode(buf.getbuffer()).decode("ascii")   
                src = 'data:image/png;base64,'+data
        return src


@app.route('/',methods=['GET','POST'])
def home_page():
    source=None
    try:
        source=form_for_image()   #calling the form to print 
    except Exception:
        flash('Unknown request taking you back to home screen!')
    if source==None:
        url="https://www.espn.com/soccer/"
        html=get_bytes_from_url(url)
        stg=text_from_html(html)
        buf=image_return(stg,None)   # None is for no mask 
        data = base64.b64encode(buf.getbuffer()).decode("ascii")   
        source = 'data:image/png;base64,'+data
    return render_template('index.html',title="word_app",source=source)


import os
from flask import render_template, url_for,request
from wd_app import app
#from wd_app import db
from wd_app import forms
from wd_app.forms import Data_upload
#from wd_app.models import Userdata
from wd_app.wd_cloud import image_return # this is the randomw filename created for the image to be displayed
from wd_app.wd_cloud import pdf_text_extractor 
import base64
import io
from io import BytesIO

'''
def my_form_post():
    if request.method=='POST':
        bg = request.form['favcolor']
        file_data = request.form['file']
    print(bg,file_data)
'''

@app.route('/',methods=['GET','POST'])
def home_page():
    source="" # can be later chnaged by setting a default image 
    form = Data_upload() # for the upload of file
    file_data=""
    file_name=""
    stg=""
    #my_form_post()   #calling the form to print 
    if form.validate_on_submit(): # validation does not happen unless you add form.csrf
        if (form.document.data.filename.endswith('txt')):
            file_data=form.document.data.stream.read().decode()
            stg=file_data
            buf=image_return(stg)
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            #return f"<img src='data:image/png;base64,{data}'/>"
            source = 'data:image/png;base64,'+data
        elif (form.document.data.filename.endswith('pdf')):
            file_pdf=form.document.data
            text=pdf_text_extractor((io.BytesIO(file_pdf.read())))
            stg=text
            buf=image_return(stg)
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            source = 'data:image/png;base64,'+data
    return render_template('index.html',title="word_app",form=form,source=source)
















################################################ignore below#############################################################################
'''
@app.route('/',methods=['GET','POST'])
def home_page():
    form = Data_upload()
    file_data=""
    file_name=""
    stg=""
    if form.validate_on_submit(): # validation does not happen unless you add form.csrf
        if (form.document.data.filename.endswith('txt')):
            file_data=form.document.data.stream.read().decode()
            stg=file_data
            _,file_name=image_return(stg)
        elif (form.document.data.filename.endswith('pdf')):
            file=form.document.data
            text=pdf_text_extractor((io.BytesIO(file.read())))
            stg=text
            _,file_name=image_return(stg)
    return render_template('index.html',title="word_app",form=form, file_name=file_name)
'''
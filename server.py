from flask import Flask,render_template
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from pdfextract import pdftext
from image_to_text import simple_image_extract
from adharcard_long import QRcode,adhar
from QRreader import Decode

import cv2
import os
import sys
app = Flask(__name__)



@app.route('/')  # page 1
def to():
    return redirect(url_for('home1'))#-----|
#                                                                       |
@app.route('/home1' ) # page 2  <-------|
def home1():
    return render_template('homepage.html')


@app.route('/home' ,methods=['POST']) # page 2
def home():
    if request.method=='POST':
        return render_template('homepage.html')

#=============================================
@app.route('/qrcode')#                                                      ||
def qrcode():#                                                                        ||
    return render_template('qcode.html')#<----|             ||
#                                                                                 |             ||
#                                                                                 |             ||
@app.route('/qr',methods=['POST'])#-----------|            ||
def QR():#                                                                                ||
    if request.method=='POST':#                                           ||
        return redirect(url_for('qrcode'))#                             ||
#=============================================
#=============================================
@app.route('/getfiles')#                                                      ||
def getfiles():#                                                                         ||
    return render_template('simpleimg.html')#<---|      ||
#                                                                                       |       ||
@app.route('/imgfiles',methods=['POST'])#--------|      ||
def imfiles():#                                                                         ||
    if request.method=='POST':#                                          ||
        return redirect(url_for('getfiles'))#                            ||
#                                                                                               ||
#=============================================


@app.route('/upload_image',methods=['POST'])
def upload_image():
    if request.method=='POST':
       f = request.files['img']
       
    if not f:
        return "<p align='center'><h1>please upload a file</h1></p>"
    fname=f.filename
    ch=request.form['Document type']
    if ch=='non document':
       f.save(os.path.join('r','..','static','plainimg',fname))
       fpath=os.path.join('r','..','static','plainimg',fname)
       text=simple_image_extract(fpath)
       return render_template('simpleimg.html',impath=fpath,extext=text)
    elif ch=='Adhar card':
        f.save(os.path.join('r','..','static','adhar',fname))
        fpath=os.path.join('r','..','static','adhar',fname)
        text=QRcode(fpath)
        return render_template('simpleimg.html',impath=fpath,extext=text)
    else:
        return render_template('simpleimg.html')
            
#===========================================================================

@app.route('/PDF',methods=['POST'])
def PDF():
    if request.method=='POST':
        return render_template('pdftext.html')
    


@app.route('/pdf',methods=['POST'])
def pdf():
    if request.method=='POST':
        pf = request.files['pdf']
        if not pf:
            return "<h1>please upload PDF file</h1>"
        fname=pf.filename
        pf.save(os.path.join('r','..','static','pdfiles',fname))
        pfpath=os.path.join('r','..','static','pdfiles',fname)
        pn=request.form['pgno']
        if not pn:
            return """<!DOCTYPE html>
<html>

	
	
	<script >
	alert("please upload pgno")	
	</script>

<body>
</body>

</html>     """
        text=pdftext(pfpath,str(int(pn)-1))
        return render_template('pdftext.html',ptext=text)
##
##
##
##
@app.route('/down', methods=['POST'])  # page 1
def down():    
    if request.method=='POST':
        f=request.files['img']
        fname=f.filename
        if not fname:
            return """<html>

	
	
	<script >
	alert("please upload pgno")	
	</script>

<body>
</body>

</html>     """
        f.save(os.path.join('r','..','static','QRCODE',fname))
        fpath=os.path.join('r','..','static','QRCODE',fname)
        imh=cv2.imread(fpath)
        h,w,_=imh.shape
        imh=cv2.resize(imh,(h-30,w-30))
        cv2.imwrite(fpath,imh)
        qtext=Decode(fpath)
        return render_template('qcode.html', qimg=fpath,qtext=qtext)
##            


         


   

if __name__ == "__main__":
    app.run(debug=True)

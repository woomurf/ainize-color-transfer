from flask import Flask, render_template, request, send_file, Response
from transfer import runTransfer
import os 
from PIL import Image
import cv2 
from io import BytesIO

app = Flask(__name__,template_folder="./templates/")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/transfer", methods = ['GET','POST'])
def trans_color():
    if request.method == "POST":
        try:
            source = Image.open(request.files['source'].stream).convert('RGB')
            target = Image.open(request.files['target'].stream).convert('RGB')
        except Exception as e: 
            return Response("fail", status=400)   

        resultImage = runTransfer(source, target)
        
        # cv2 image convert to PIL image 
        # and PIL image to bytes 
        im_pil = Image.fromarray(resultImage)
        img_io = BytesIO()
        im_pil.save(img_io, 'PNG')
        img_io.seek(0)

    return send_file(img_io, mimetype="image/jpeg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)

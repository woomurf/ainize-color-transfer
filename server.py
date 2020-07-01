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
            source = request.files['source']
            target = request.files['target']
        except Exception as e: 
            return Response("fail", status=400)  

        source_path = "./static/" + source.filename 
        target_path = "./static/" + target.filename
        source.save(source_path)
        target.save(target_path)

        resultImage = runTransfer(source_path, target_path)
        
        # cv2 image convert to PIL image 
        # and PIL image to bytes 
        im_pil = Image.fromarray(resultImage)
        img_io = BytesIO()
        im_pil.save(img_io, 'PNG')
        img_io.seek(0)

        deleteLocalImage()

    return send_file(img_io, mimetype="image/jpeg")

def deleteLocalImage():
    for filename in os.listdir('./static'):
        file_path = os.path.join('./static', filename)
        try:
            os.remove(file_path)
        except:
            print("file delete fail")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)

from flask import Flask, render_template, request
from example import runExample
import os 

app = Flask(__name__,template_folder="./templates/")

@app.route("/")
def index():
    for filename in os.listdir('./static'):
        file_path = os.path.join('./static', filename)
        try:
            os.remove(file_path)
        except:
            print("file delete fail")
        
    return render_template('index.html')


@app.route("/transfer", methods = ['GET','POST'])
def trans_color():
    if request.method == "POST":
        source = request.files['source']
        target = request.files['target']

        source_path = "./static/" + source.filename 
        target_path = "./static/" + target.filename
        source.save(source_path)
        target.save(target_path)
        result = source.filename + '_' + target.filename
        # result = 'result.jpg'
        runExample(source_path, target_path, result)
        
    return render_template('result.html', value=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)

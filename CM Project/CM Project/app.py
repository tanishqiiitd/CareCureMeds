from flask import Flask
from flask import render_template
from flask import request
import os
from flask import url_for
from flask import redirect
from model import getPrediction
from Hospital import createGraph


app =Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["CACHE_TYPE"] = "null"
app.config["params"] = {}
app.config['SECRET_KEY'] = "f14585fdcdba1a1d41dfcead63d12f3c"
app.config['count'] = 0
image_folder = os.path.join('static/images')
app.config['image'] = image_folder

css_folder = os.path.join('static/style')
app.config['css'] = css_folder

map_folder = os.path.join('static/map/')
app.config['map'] = css_folder



@app.route("/")
@app.route("/Home")
def Home():
    return render_template('Home.html')

@app.route("/HeatMap")
def HeatMap():
    return render_template('HeatMap.html')


@app.route("/search",methods = ['GET','POST'])
def search():
    for filename in os.listdir('static/map/'):
        if filename.startswith('map'):  
            os.remove('static/map/' + filename)
    

    if(request.method == 'POST'): 
        for filename in os.listdir('static/map/'):
            if filename.startswith('map'):  
                os.remove('static/map/' + filename)

        app.config['count'] += 1
        lists = list(request.form.lists())
        print(lists)
        address = lists[0][1][0]
        radius = lists[1][1][0]
        symptoms = lists[2][1]
        disease = None
        data = None
        if(len(symptoms) > 0):
            disease,prob = getPrediction(symptoms)
            data = createGraph(address,radius,app.config['count'])
        disease = "The Predicted Disease is "+str(disease)+"  with Predicted Probability "+str(prob)
        print(disease)
        app.config["params"] = {"disease":disease,"tables":[data.to_html()],"titles":[''],'count':app.config['count']}
        return redirect(url_for('output'))
    return render_template('search.html')

@app.route("/output")
def output():
    params = app.config["params"]
    return render_template('output.html',disease = params["disease"],tables=params["tables"],titles = params["titles"])


if __name__ == '__main__':
    app.run(debug = True)
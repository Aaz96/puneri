from flask import Flask, render_template, url_for, request
import pandas as pd
import string
import numpy as np
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
lemmatizer= WordNetLemmatizer()
import re

app = Flask(__name__)

app.config['SECRET_KEY'] = "cd5eb45d91c760c4"

final_1 = pd.read_csv('trip_ad.csv', index_col=[0])
dict1 = defaultdict(lambda :defaultdict(list))

def places(input):
    # flag = True
    word = str(input).lower()
    lem_word= lemmatizer.lemmatize(word)
    for i in range(len(final_1['places'])):  
        if lem_word in final_1['tags'][i]:
            # flag = True
            dict1["places"][i].append(final_1[final_1['tags']==final_1['tags'][i]]['places'][i])
            dict1["places"][i].append(str(final_1[final_1['tags']==final_1['tags'][i]]['tags'][i]))
            dict1["places"][i].append(final_1[final_1['tags']==final_1['tags'][i]]['ratings'][i])
            dict1["places"][i].append(final_1[final_1['tags']==final_1['tags'][i]]['review'][i])  


        elif lem_word in final_1['places'][i]:
            # flag = False
            df1 = final_1[final_1['places'].str.contains(lem_word)]
            df1 = df1.reset_index(drop =True)
            for i in range(len(df1)):
                dict1["places"][i].append(df1['places'][i])
                dict1["places"][i].append(str(df1['tags'][i]))
                dict1["places"][i].append(df1['ratings'][i])
                dict1["places"][i].append(df1['review'][i])
        else:
            pass
    for i in dict1.keys():
        for j in dict1[i].keys():
            dict1[i][j].append(int(str(dict1[i][j][2]).split(".")[0]))
            dict1[i][j].append(int(str(dict1[i][j][2]).split(".")[1]))
    return dict1
    

    

@app.route('/')
def home():
    # form = Search_tag()
    return render_template('home.html', title = 'Home')

@app.route('/query',methods=['POST'])
def home_return():
    text = request.form["u"]
    return render_template("query.html",places = places(text))

@app.route('/about')
def about():
    # form = Search_tag()
    return render_template('about.html', title = 'About')

if __name__ == '__main__':
    app.static_folder = 'static'
    app.run(debug=False)
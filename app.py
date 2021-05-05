from flask import Flask,render_template,request,jsonify
import os
from wsgiref import simple_server
import pickle
import gunicorn
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app=Flask(__name__)
model=pickle.load(open('liver_classification.pkl','rb'))

@app.route('/')

def home():
    return render_template('index.html')


scaling=StandardScaler()

@app.route('/predict',methods=['POST'])

def predict():
    if request.method == 'POST':
        Age=int(request.form['Age'])

        Gender = (request.form['Gender'])
        if (Gender=='Male'):
            Gender=0
        else:
            Gender=1

        Total_Bilirubin = float(request.form['Total_Bilirubin'])


        #Direct_Bilirubin = float(request.form(['Direct_Bilirubin']))

        Alkaline_Phosphotase = float(request.form['Alkaline_Phosphotase'])

        Alamine_Aminotransferase = float(request.form['Alamine_Aminotransferase'])

        #Aspartate_Aminotransferase = float(request.form(['Aspartate_Aminotransferase']))

        Total_Proteins = float(request.form['Total_Proteins'])

        #Albumin = float(request.form(['Albumin']))

        Albumin_and_Globulin_Ratio = float(request.form['Albumin_and_Globulin_Ratio'])

        scaled_input=scaling.fit_transform([[Age,Gender,Total_Bilirubin,Alkaline_Phosphotase,Alamine_Aminotransferase,Total_Proteins,Albumin_and_Globulin_Ratio]])
        prediction=model.predict(scaled_input)
        output=round(prediction[0],2)

        if output==0:
            return render_template('index.html',prediction_text='You dont have Liver Disease')
        else:
            return render_template('index.html', prediction_text='You have Liver Disease')

    else:
        return render_template('index.html',test='Something went wrong')

###############Files needed for deployment###############
##procfile
##manifest.yml
##runtime.txt
##########################################################


#port=int(os.getenv("PORT"))
if __name__=='__main__':
    ###############Below line are used to remove flask warning of wsgi##################
    #host='0.0.0.0'
    #app.run(debug=True,port=port)
    #httpd=simple_server.make_server(host,port,app)
    #httpd.serve_forever
    ######################################
    app.run(debug=True)


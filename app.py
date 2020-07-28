from flask import Flask,render_template,request,jsonify
import pickle
import gunicorn
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app=Flask(__name__)
model=pickle.load(open('liver_forest_classification.pkl','rb'))

@app.route('/')

def home():
    return render_template('index.html')


standard_to=StandardScaler()
@app.route('/predict',methods=['POST'])

def predict():
    if request.method == 'POST':
        Age=int(request.form['Age'])

        Gender = (request.form['Gender'])
        if (Gender=='Male'):
            Gender_Male=1
            Gender_Female=0
        else:
            Gender_Female=1
            Gender_Male = 0

        Total_Bilirubin = float(request.form['Total_Bilirubin'])


        #Direct_Bilirubin = float(request.form(['Direct_Bilirubin']))

        Alkaline_Phosphotase = float(request.form['Alkaline_Phosphotase'])

        Alamine_Aminotransferase = float(request.form['Alamine_Aminotransferase'])

        #Aspartate_Aminotransferase = float(request.form(['Aspartate_Aminotransferase']))

        Total_Protiens = float(request.form['Total_Protiens'])

        #Albumin = float(request.form(['Albumin']))

        Albumin_and_Globulin_Ratio = float(request.form['Albumin_and_Globulin_Ratio'])


        prediction=model.predict([[Age,Total_Bilirubin,Alkaline_Phosphotase,Alamine_Aminotransferase,Total_Protiens,Albumin_and_Globulin_Ratio,Gender_Female,Gender_Male]])
        output=round(prediction[0],2)
        if output==0:
            return render_template('index.html',prediction_text='You dont have Liver Disease')
        else:
            return render_template('index.html', prediction_text='You have Liver Disease')

    else:
        return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)
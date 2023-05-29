#this script is used for AWS deployment
from flask import Flask, request, render_template

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipline

application = Flask(__name__)
# app = application #comment out to deploy on EB

#Route for a home page

@application.route('/')
def index():
    return render_template('index.html')

# @app.get("/health")
# def health():
#     response.status = 200
#     return response

@application.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html') #simple input data field will be here
    
    else: #POST request
        data=CustomData(
            gender=request.form.get('gender'), 
            race_ethnicity=request.form.get('race_ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=request.form.get('reading_score'),
            writing_score=request.form.get('writing_score')
        )

        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline=PredictPipline()
        results = predict_pipeline.predict(pred_df)
        return render_template('home.html', results=results[0])
    
if __name__=="__main__":
    application.run(host='0.0.0.0', debug=True) #run on http://127.0.0.1:5000 deafualt
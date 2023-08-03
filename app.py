from flask import Flask, render_template, request
import joblib

app = Flask(__name__)
import sklearn
print(sklearn.__version__)

model = joblib.load('cmodel_filename.joblib')

@app.route('/', methods=['GET', 'POST'])
def churn_prediction():
    if request.method == 'POST':
        try:
            credit_score = int(request.form['credit'])
            geography = request.form['Geography']
            gender = request.form['Gender']
            age= int(request.form['age'])
            tenure = int(request.form['Tenure'])
            balance = float(request.form['Balance'])
            num_of_products = int(request.form['nop'])
            credit_card = request.form['creditcard']
            active_member = request.form['isactive']
            estimated_salary = float(request.form['estimated_salary'])
        except ValueError as e:
            return "Error: Invalid input. Please check your form data."

        d={'France': 0,'Spain':2, 'Germany': 1}
        geography=d[geography]
        g={'Male':1,'Female':0}
        gender=g[gender]
        a={'Yes':1,'No':0}
        credit_card=a[credit_card]
        active_member=a[active_member]
        churn_prediction_result =model.predict([[credit_score, geography, gender,age,tenure,
                                                        balance, num_of_products, credit_card,
                                                        active_member, estimated_salary]])

        churn_prediction_result = int(churn_prediction_result[0])
        
        # Determine the prediction result message
        if churn_prediction_result == 1:
            churn_result_message = "The customer is Exited."
        else:
            churn_result_message = "The customer is Not Exited."

        return render_template('result.html', churn_result_message=churn_result_message)

    return render_template('home.html')

    

if __name__ == '__main__':
    app.run(debug=True)


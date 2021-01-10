from flask import Flask, render_template, flash, request, jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import pickle
import os

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '703841'

# To use our pickle


model = pickle.load(open('model.pkl', 'rb'))
tab=[]
class OurForm(Form):
    intercolumnar = FloatField('Please put an intercolumar distance between -3.49 and 11.8', validators=[DataRequired()])
    upperMargin = FloatField('Put an upper margin value between -2,4 and 2', validators=[DataRequired()])
    lowerMargin = FloatField('Put an lower margin value between -3,2 and 3', validators=[DataRequired()])
    exploitation = FloatField('Put an exploitation value between -5,4 and 3,9', validators=[DataRequired()])
    rowNumber = FloatField('Put a row number value between -4,9 and 1', validators=[DataRequired()])
    submit = SubmitField('Submit')

def predict(tab):
    prediction= model.predict(np.array(list(tab)).reshape(1, -1))
    return prediction

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = OurForm(request.form)
    intercolumnar=0
    if request.method == 'POST':
        intercolumnar=request.form['intercolumnar']
        print (intercolumnar)

        upperMargin=request.form['upperMargin']
        print (upperMargin)

        lowerMargin=request.form['lowerMargin']
        print (lowerMargin)

        exploitation=request.form['exploitation']
        print (exploitation)
        rowNumber=request.form['rowNumber']
        print (rowNumber)
        data = [intercolumnar, upperMargin, lowerMargin, exploitation, rowNumber, 0.8, 0.5, 0.9, 0.4, 0.8/0.5]
        prediction=predict(data)
        return render_template('index1.html', form=form, prediction_text = 'The class we predict is : {}'.format(prediction))
    if form.validate():
        # Save the comment here.
        flash('Hello ' + intercolumnar)
    else:
        flash('All the form fields are required. ')

    return render_template('index1.html', form=form)





if __name__ == "__main__":
    app.run()

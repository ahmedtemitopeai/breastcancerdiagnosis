from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField
from wtforms.validators import ValidationError, InputRequired
import json
import numpy as np
import pickle
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)

class BreastCancerForm(FlaskForm):
    perimeter = FloatField('Perimeter Mean', validators=[InputRequired()])
    concave_points_mean = FloatField('Concave Points Mean', validators=[InputRequired()])
    texture_mean = FloatField('Texture Mean', validators=[InputRequired()])
    smoothness_worst = FloatField('Smoothness Worst', validators=[InputRequired()])
    symmetry_worst = FloatField('Symmetry Worst', validators=[InputRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = BreastCancerForm()
    prediction = None
    if form.validate_on_submit():
        perimeter = form.perimeter.data
        concave_points_mean = form.concave_points_mean.data 
        texture_mean = form.texture_mean.data   
        smoothness_worst = form.smoothness_worst.data 
        symmetry_worst = form.symmetry_worst.data

        data = [[((perimeter - 91.969033) / 24.298981), ((concave_points_mean - 0.048919)/0.038803), ((texture_mean - 19.289649) / 4.301036), ((smoothness_worst - 0.132369) / 0.022832), ((symmetry_worst - 0.290076)/0.061867)]]

        session['prediction'] = np.array2string(model.predict(data))
        print(session['prediction'])
        return redirect(url_for('index'))
    return render_template('index.html', form=form, prediction=session.get('prediction'))

if __name__ == '__main__':
    modelfile = 'breast_cancer_prediction.pickle'
    model = pickle.load(open(modelfile, 'rb'))
    print(model)
    app.run(debug=True)
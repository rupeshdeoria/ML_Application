from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
import pandas as pd
from sklearn.linear_model import LinearRegression
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
#app = Flask(__name__, template_folder='template')


class DataForm(FlaskForm):
    homeArea = StringField('Home Area',[validators.Length(min=4, message=('Your message is too short.'))])
    bedRoom = StringField('Bed Rooms',[validators.Length(min=4, message=('Your message is too short.'))])
    bathRoom = StringField('Age',[validators.Length(min=4, message=('Your message is too short.'))])
    pridict = StringField('Result')
    submit = SubmitField('Pridict')

@app.route('/',methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        form = DataForm(request.form)
        form.pridict.data = prediction(form.homeArea.data,form.bedRoom.data,form.bathRoom.data)
    else:
        form = DataForm()
    
    return render_template('home.html',form=form);

def prediction(*argv):
    df = pd.read_csv('homeprices.csv')
    df.head()
    df.bedrooms = df.bedrooms.fillna(df.bedrooms.median())
    newdf = df.drop('price',axis='columns')
    reg = LinearRegression()
    reg.fit(newdf,df.price)
    result = reg.predict([[int(argv[0]), int(argv[1]), int(argv[2])]])
    #result = reg.predict([[3000, 3, 40]])
    return result[0]
    #return 10

if __name__ == '__main__':
    app.run(debug=True)
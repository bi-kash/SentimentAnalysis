from flask import Flask, render_template,jsonify,request,abort
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

from naive_bayes_classifier import NB

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234252333' # some secret key

# load the model.pickle  file 
# model = pickle.load(open('model.pickle','rb'))
# p_in = open("model.pkl","rb")  # it needs class def, so dont' forget -> from naive_bayes_classifier import NB
# classifier = pickle.load(p_in)
import pickle
p_in = open("model.pkl","rb")  # it needs class def, so dont' forget -> from naive_bayes_classifier import NB
classifier = pickle.load(p_in)


@app.route('/', methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def index():   
    pred = None
    form = reviewForm()
    if form.validate_on_submit():
        review = form.review.data
        pred = getSentiment(review)
        # pred = classifier.test(review) #use the classifier
    return render_template('home.html', form=form, pred=pred)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/api")
def api():
    return render_template("api.html")


# ------------------------------ Basic API  ---------------------------
@app.route("/api/v1.0/", methods=['POST'])
def process():   
    if not request.json:
        abort(400)

    r = request.json  # receive the data from client
    polarity="error"

    if len(r) == 0:
        return jsonify({'result':'Empty Payload'})  
    if len(r) == 1:
        polarity = getSentiment(r[0])
    if len(r) > 1:
        polarity = []
        for review in r:
            polarity.append(getSentiment(review))
   
    return jsonify({'result': polarity}), 201

# ---------------------------Basic API Ends--------------------------------------
# for handling errors -------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
# ----------------------------------------------------

class reviewForm(FlaskForm):
    # text = TextAreaField('Text', render_kw={"rows": 70, "cols": 11})
    review = TextAreaField('Review',validators=[DataRequired()])
    submit = SubmitField('Analyze')

# ----------------------------------------------------
def getSentiment(review):
    return classifier.test(review)


if __name__ == '__main__':   

    app.run(debug=1,port=5001)
from datetime import datetime
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jha.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b'JobHazardAnalysis101'
db = SQLAlchemy(app)

class Jha(db.Model): #replace nullable = false on last few fields
    JHAid = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    activityDescription = db.Column(db.String(200))
    hazardDescription = db.Column(db.String(200))
    hazardControl = db.Column(db.String(200))
    steps = db.relationship('Step', backref='jha', lazy=True)

    def __repr__(self):
        return f"Jha('{self.JHAid}','{self.author}','{self.activityDescription}','{self.hazardDescription}','{self.hazardControl}')"

class Step(db.Model):
    Stepid = db.Column(db.Integer, primary_key=True)
    stepDescription = db.Column(db.String(200), nullable=False)
    JHAid_id = db.Column(db.Integer, db.ForeignKey('jha.JHAid'),
        nullable=False)

@app.route('/home')# creates route to home page
def home():
    return render_template('home.html')

@app.route('/toSteps', methods=['POST', 'GET'])# creates route to steps page
def toSteps():
    stepQuery = Step.query.order_by(Step.JHAid_id).all()
    return render_template('steps.html', steps=stepQuery)

@app.route('/hazardList', methods=['POST', 'GET'])# creates route to list of Hazards
def hazardL():
    jha = Jha.query.order_by(Jha.date_created).all()
    return render_template('hazards.html', jha=jha)

@app.route('/', methods=['POST', 'GET'])#route to post JHA
def index():
    if request.method =='POST':
        jha_author = request.form['author']
        jha_activityDescription = request.form['activityDescription']
        jha_hazardDescription = request.form['hazardDescription']
        jha_hazardControl = request.form['hazardControl']
        bulkJhaInsert =Jha(author=jha_author, activityDescription=jha_activityDescription, hazardDescription=jha_hazardDescription, hazardControl=jha_hazardControl)
       
        try:
            db.session.add(bulkJhaInsert)
            db.session.commit()
            flash('Job Hazard Analysis form added succesfully')
            return redirect('/')
        except: # pylint: disable=bare-except
            return "error adding Job Hazard Analysis"
    else:
        jha = Jha.query.order_by(Jha.date_created).all()
        return render_template('index.html', jha=jha)

@app.route('/delete/<int:id>')
def delete(id):
    JHA_to_delete = Jha.query.get_or_404(id)

    try:
        db.session.delete(JHA_to_delete)
        db.session.commit()
        return redirect('/hazardList')
    except: # pylint: disable=bare-except
        return "Problem deleting Job Hazard Analysis."


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    JHA_to_update = Jha.query.get_or_404(id)

    if request.method == 'POST':
        JHA_to_update.author = request.form['author']
        JHA_to_update.activityDescription = request.form['activityDescription']
        JHA_to_update.hazardDescription = request.form['hazardDescription']
        JHA_to_update.hazardControl = request.form['hazardControl']

        #This sends current tasks content to form of the update box
        try:
            db.session.commit()
            return redirect('/hazardList')
        except: # pylint: disable=bare-except
            return "Error updating Job Hazard Analysis"
    else:
        return render_template('update.html', jha=JHA_to_update)

@app.route('/steps/<int:id>', methods=['GET', 'POST'])
def steps(id):
    if request.method =='POST':
        step_stepDescription = request.form['stepDescription']
        stepInsert =Step(stepDescription=step_stepDescription)
       
        try:
            db.session.add(stepInsert)
            db.session.commit()
            flash('Job Hazard Step inserted successfully!')
            return redirect('/toSteps')
        except: # pylint: disable=bare-except
            return "error adding Job Hazard step"
    else:
        stepQuery = Step.query.order_by(Step.JHAid_id).all()
        return render_template('steps.html', steps=stepQuery)

if __name__ =="__main__":
    app.run(debug=True)
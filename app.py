from datetime import datetime
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jha.db'
db = SQLAlchemy(app)

class Todo(db.Model): #Delete when new DB is finished
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
        #Function returns a string everytime a new element is created.(returns ID of that task)

class Jha(db.Model): #replace nullable = false on last few fields
    JHAid = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    activityDescription = db.Column(db.String(200))
    hazardDescription = db.Column(db.String(200))
    hazardControl = db.Column(db.String(200))
    steps = db.relationship('Step', backref='jha', lazy=True)

    def __repr__(self):
        return '<Jha %r>' % self.JHAid

class Step(db.Model):
    Stepid = db.Column(db.Integer, primary_key=True)
    stepDescription = db.Column(db.String(200), nullable=False)
    JHAid_id = db.Column(db.Integer, db.ForeignKey('jha.JHAid'),
        nullable=False)

@app.route('/home')# creates route to home page
def home():
    return render_template('home.html')

@app.route('/newHazard')#Creates route to new hazard page (index.html)
def newHazard():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method =='POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except: # pylint: disable=bare-except
            return "error adding task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/postJHA', methods=['POST', 'GET'])#route to post JHA
def author():
    if request.method =='POST':
        jha_content = request.form['author']
        new_jha = Jha(author=jha_content)

        try:
            db.session.add(new_jha)
            db.session.commit()
            return redirect('/postJHA')
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
        return redirect('/postJHA')
    except: # pylint: disable=bare-except
        return "Problem deleting Job Hazard Analysis."


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    JHA_to_update = Jha.query.get_or_404(id)

    if request.method == 'POST':
        Jha.author = request.form['author']
        #This sends current tasks content to form of the update box
        try:
            db.session.commit()
            return redirect('/postJHA')
        except: # pylint: disable=bare-except
            return "Error updating Job Hazard Analysis"
    else:
        return render_template('update.html', jha=JHA_to_update)

if __name__ =="__main__":
    app.run(debug=True)
    
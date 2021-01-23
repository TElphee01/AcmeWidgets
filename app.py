from datetime import datetime
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jha.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
        #Function returns a string everytime a new element is created.(returns ID of that task)

@app.route('/home')# creates route to home page
def home():
        return render_template('home.html')

@app.route('/newHazard')#Creates route to new hazard page (index.html)
def newHazard()
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

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except: # pylint: disable=bare-except
        return "Problem deleting task."


@app.route('/update/<int:id>', methods=['GET', 'POST']) 
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        #This sends current tasks content to form of the update box
        try:
            db.session.commit()
            return redirect('/')
        except: # pylint: disable=bare-except
            return "Error updating task"
    else:
        return render_template('update.html', task=task)


if __name__ =="__main__":
    app.run(debug=True)
    
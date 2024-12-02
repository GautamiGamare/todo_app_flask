from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f'{self.title} - {self.desc}'

@app.route('/',methods=['GET','POST'])
def welcome():
    if request.method == 'POST':
        todo = Todo(title=request.form['title'],desc=request.form['desc'])
        db.session.add(todo)
        db.session.commit()
    all_todo = db.session.query(Todo).all()
    return render_template('index.html', all_todo=all_todo)

@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    todo = db.session.query(Todo).filter(Todo.id==id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    if request.method == 'GET':
        todo = db.session.query(Todo).filter(Todo.id==id).first()
        return render_template('update.html',todo=todo)
    else:
        title = request.form['title']
        desc = request.form['desc']
        todo = db.session.query(Todo).filter(Todo.id==id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

@app.route('/completed/<int:id>', methods=['GET','POST'])
def completed(id):
    todo = db.session.query(Todo).filter(Todo.id==id).first()
    todo.completed = True 
    db.session.add(todo)
    db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
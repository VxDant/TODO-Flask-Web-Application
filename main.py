from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.sno}-{self.title}'


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = ToDo(title=title, desc=desc)

        db.session.add(todo)
        db.session.commit()

    alltodos = ToDo.query.all()
    return render_template('index.html', alltodos=alltodos)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo1 = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo1)
    db.session.commit()
    return redirect("/")


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo2 = ToDo.query.filter_by(sno=sno).first()
        todo2.title = title
        todo2.desc = desc
        db.session.add(todo2)
        db.session.commit()
        return redirect("/")
        
    todo2 = ToDo.query.filter_by(sno=sno).first()
        
    return render_template("update.html", todo2=todo2)


@app.route('/events')
def events():
    return 'There are no upcoming events!'


if __name__ == "__main__":
    app.run(debug=True)

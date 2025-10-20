from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    introduction = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return f'<Note {self.title}>'


@app.route('/notes')
@app.route('/')
def index_page():
    all_notes = Note.query.order_by(Note.date.desc()).all()
    return render_template('posts.html', notes=all_notes, title='Все заметки')


@app.route('/create_note', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        introduction = request.form['introduction']
        text = request.form['text']
        
        note = Note(title=title, introduction=introduction, text=text)
        db.session.add(note)
        db.session.commit()
        return redirect('/notes')
    
    return render_template('create_note.html', title='Создание заметки')


@app.route('/note/<int:id>')
def note_details(id):
    note = Note.query.get_or_404(id)
    return render_template('note_details.html', note=note, title=note.title)


@app.route('/note/<int:id>/update', methods=['GET','POST'])
def update_note_page(id):
    note = Note.query.get_or_404(id)
    if request.method == 'POST':
        
        note.title = request.form['title']
        note.introduction = request.form['introduction']
        note.text = request.form['text']
        
        db.session.commit()
        return redirect('/notes')
    else:
        return render_template('update_note.html', note=note, title='Изменение заметки')



@app.route('/note/<int:id>/delete')
def delete_note_page(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=True, reloader_type='stat')
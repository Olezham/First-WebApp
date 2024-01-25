from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'

db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/coding')
def coding():
    return render_template('coding.html')

@app.route('/news')
def news():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('news.html', articles=articles)

@app.route('/news/<int:id>')
def news_det(id):
    article = Article.query.get(id)
    return render_template('news_det.html', article=article)

@app.route('/add_article', methods=['POST', 'GET'])
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro,text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/news')
        except:
            print('Что-то пошло не так')
    else:
        return render_template('add_article.html')

if __name__ == "__main__":
    app.run(debug=True)

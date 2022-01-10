from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float(120), nullable=False)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.create_all()

# admin = User(title="Harry Potter", author="J. K. Rowling", rating=4.3)
# db.session.add(admin)
# db.session.commit()
all_books = []


@app.route('/')
def home():
    all_books = db.session.query(User).all()
    # return f"{all_books}"
    return render_template("index.html", books=all_books, length=len(all_books))


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book_details = User(title=request.form["book"], author=request.form["author"], rating=request.form["rating"])
        db.session.add(book_details)
        db.session.commit()
        # new_dict = {
        #     "title": request.form["book"],
        #     "author": request.form["author"],
        #     "rating": int(request.form["rating"])
        # }
        # all_books.append(new_dict)

        return redirect(url_for('home'))
    else:
        return render_template("add.html")


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    book = User.query.get(id)
    if request.method == 'POST':
        book.rating = float(request.form["new_rating"])
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template("edit.html", book=book)


@app.route('/delete/<ide>')
def delete(ide):
    book = User.query.get(ide)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)


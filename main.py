from flask import Flask, render_template, request, redirect

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)


@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.id)).scalars()
    all_books = list(result)
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book = Book(
            name=request.form["name"],
            author=request.form["author"],
            rating=request.form["rating"],
        )
        with app.app_context():
            db.session.add(book)
            db.session.commit()

        return redirect('/')
    return render_template('add.html')


@app.route('/edit/<book_id>', methods=['GET', 'POST'])
def edit(book_id):
    if request.method == 'POST':
        with app.app_context():
            book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
            book_to_update.rating = float(request.form["new_rating"])
            db.session.commit()
        return redirect('/')

    book = db.get_or_404(Book, book_id)
    return render_template('edit.html', book_data=book)


@app.route('/delete/<book_id>', methods=['GET', 'POST'])
def delete(book_id):
    book = db.get_or_404(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    print(book_id)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)


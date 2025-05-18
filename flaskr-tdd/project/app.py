import os
from functools import wraps
from pathlib import Path
from flask_migrate import Migrate
from flask import (
    Flask,
    render_template,
    request,
    session,
    flash,
    redirect,
    url_for,
    abort,
    jsonify,
)
from project.extensions import db


basedir = Path(__file__).resolve().parent
app = Flask(__name__)


app.config.update({
    'DATABASE': os.getenv("DATABASE_NAME", "flaskr.db"),
    'SECRET_KEY': os.getenv("SECRET_KEY", "change_me"),
    'SQLALCHEMY_DATABASE_URI': os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{basedir.joinpath('flaskr.db')}"
    ),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
})


if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace(
        "postgres://", "postgresql://", 1
    )


db.init_app(app)
migrate = Migrate(app, db)


from project.models import Post, User


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please log in.")
            return jsonify({"status": 0, "message": "Please log in."}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    """Отображает все записи из базы данных."""
    entries = Post.query.all()
    return render_template("index.html", entries=entries)


@app.route("/add", methods=["POST"])
def add_entry():
    """Добавляет новую запись в базу данных."""
    if not session.get("logged_in"):
        abort(401)

    try:
        new_entry = Post(
            title=request.form["title"],
            text=request.form["text"]
        )
        db.session.add(new_entry)
        db.session.commit()
        flash("New entry was successfully posted")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}")

    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if not user:
            error = "Invalid username"
        elif not user.verify_password(request.form["password"]):
            error = "Invalid password"
        else:
            session["logged_in"] = True
            flash("You were logged in")
            return redirect(url_for("index"))
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    """Завершает сеанс пользователя."""
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("index"))


@app.route("/delete/<int:post_id>", methods=["GET"])
@login_required
def delete_entry(post_id):
    """Удаляет запись из базы данных."""
    result = {"status": 0, "message": "Error"}
    try:
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        result = {"status": 1, "message": "Post Deleted"}
        flash("The entry was deleted.")
    except Exception as e:
        db.session.rollback()
        result["message"] = str(e)

    return jsonify(result)


@app.route("/search/", methods=["GET"])
def search():
    """Поиск записей по ключевому слову."""
    query = request.args.get("query")
    entries = Post.query
    if query:
        entries = entries.filter(Post.text.contains(query) | Post.title.contains(query))
    return render_template("search.html", entries=entries, query=query)


@app.cli.command("init-db")
def init_db_command():
    """Инициализирует базу данных с начальными данными."""
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", email="admin@example.com")
            admin.password = "admin"
            db.session.add(admin)
            print("✅ Admin user created")

        if not Post.query.first():
            post = Post(title="First Post", text="First Post content")
            db.session.add(post)
            print("✅ Initial post created")

        db.session.commit()
    print("🗄️ Database initialized!")


if __name__ == "__main__":
    app.run()

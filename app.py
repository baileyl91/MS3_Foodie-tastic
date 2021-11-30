import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_paginate import Pagination, get_page_args
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'


mongo = PyMongo(app)


def collection(recipes, offset=0, per_page=8):
    """
    Give pagination information about recipes
    """
    recipes = list(mongo.db.recipes.find())
    return recipes[offset: offset + per_page]


@app.route("/")
@app.route("/home")
def home():
    """
    First page to load when user registers to site
    """
    quotes = list(mongo.db.quotes.find())
    return render_template("home.html", quotes=quotes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for('register'))

        register = {
            "username": request.form.get("username".lower()),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                flash("Incoreect Username and/or Password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/get_recipe")
def get_recipe():
    recipe = list(mongo.db.recipes.find())
   # Pagination
    # pylint: disable=unbalanced-tuple-unpacking
    # page, per_page, offset = get_page_args(page_parameter='page',
    #                                        per_page_parameter='per_page')
    page = int(request.args.get('page', 1))

    per_page = 8

    offset = (page - 1) * per_page
    # pylint: enable=unbalanced-tuple-unpacking
    total = len(recipe)
    pagination_recipes = collection(recipe, offset=offset, per_page=8)
    pagination = Pagination(page=page, per_page=8, total=total)
    return render_template("recipes_collection.html", recipes=pagination_recipes, page=page, per_page=per_page, pagination=pagination)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "serves": request.form.get("serves"),
            "cooking_time": request.form.get("cooking_time"),
            "image": request.form.get("image"),
            "description": request.form.get("description"),
            "ingredients": request.form.get("ingredients").splitlines(),
            "steps": request.form.get("steps").splitlines(),
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Added Successfully!")
        return redirect(url_for("get_recipe"))
    
    recipe = mongo.db.recipes.find().sort("recipe_name", 1)
    return render_template("add_recipe.html", recipes=recipe)


@app.route("/recipe/<recipes_id>")
def recipe(recipes_id):
    if 'username' in session:
        return render_template('recipe.html', username=session['username'],
        recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipes_id)}))
    else:
        return render_template('recipe.html', username='',
        recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipes_id)}))


@app.route("/edit_recipe/<recipes_id>", methods=["GET", "POST"])
def edit_recipe(recipes_id):
    if request.method == "POST":
        edit = {
            "recipe_name": request.form.get("recipe_name"),
            "serves": request.form.get("serves"),
            "cooking_time": request.form.get("cooking_time"),
            "image": request.form.get("image"),
            "description": request.form.get("description"),
             "ingredients": request.form.get("ingredients").splitlines(),
            "steps": request.form.get("steps").splitlines(),
            "created_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipes_id)}, edit)
        flash("Recipe Edited Successfully!")

    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipes_id)})
    return render_template("edit_recipe.html", recipes=recipe)


@app.route("/delete_recipe/<recipes_id>")
def delete_recipe(recipes_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipes_id)})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("get_recipe"))


def search_recipes(offset=0, per_page=8):
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return recipes[offset: offset + per_page]


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    searches DB for recipes that user types into search field.
    """
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    # Pagination
    # pylint: disable=unbalanced-tuple-unpacking
    # page, per_page, offset = get_page_args(page_parameter='page',
    #                                        per_page_parameter='per_page')
    page = int(request.args.get('page', 1))
    per_page = 8
    offset = (page - 1) * per_page
    # pylint: enable=unbalanced-tuple-unpacking
    total = len(recipes)
    pagination_recipes = search_recipes(offset=offset, per_page=8)
    pagination = Pagination(page=page, per_page=8, total=total)
    
    return render_template(
        "recipes_collection.html", recipes=pagination_recipes,
        page=page, per_page=per_page, pagination=pagination)




if __name__ == "__main__":
    app.secret_key = 'super secret key'
    
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
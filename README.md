# Foodie-tastic!

[View the live project here.](https://flask-recipe-cookbook.herokuapp.com/)

This project was created as part of my Milestone Project 3 with Code Institute Web Application Development course. 

For the project and to demonstrate what I have learned in the course, have decided to create an online recipe cookbook application called ‘Foodie-tastic!’. The inspiration was provided by Code Institute in the project assessment handbook.

The main goal of the site is to be a recipe-sharing site. Allowing users to create and share their own recipes with the community. 


## User Stories

First Time Visitor Goals

* As a first-time user, want to understand what the website is about 
* As a first-time user can clearly see how it works
* As a first-time user, want to see the recipes on offer
* As a first-time user, want to visit the web application social media pages
* As a first-time user clearly can see where they can register for an account

Returning Visitor Goals

* As a returning user, able to add new recipes to the community
* As a returning user, able to edit their own recipes
* As a returning user, able to delete their own recipes
* As a returning user, able to see recipes created by others in the community
* As a returning user, able to see recipes created/promoted  by the site owner
* As a returning user can identify where and easily log in
* As a returning user, once logged in can easily navigate through the site

Site Owner Goals

* As a site owner, able to add and promote their own recipes
* As a site owner, able to keep website content clean
* As a site owner, able to delete any recipes
* As a site owner, able to edit recipes to fix any mistakes

## Design

**Color Scheme**

The site comprises two different shades of green with white text. 
The navbar and the footer would be a dark shade of green while the body is a light shade of green. 
The recipe cards would have a background color of white and the delete buttons red to identify as a danger.

**Typograpghy**

The main font I have used is the ‘Poppins’ for its clean and minimal look with the backup font as sans-serif font if there were any problems using the first choice. 

**Imagery**

The hero image was sourced from Unsplash and was chosen because I felt it captures the gathering of a community coming together to share foods as the aim of the site is for the community to share their recipes.

**Database Structure**

The database is not a relational database and was created using MongoDB. 
There are only two databases in the collection, named:

* Users
* Recipes

**Wireframes**

## Features

There are a number of features that have been implemented into the website which are:

* Navbar to allow users to navigate through the site
* Footer to store social media links 
* Social media links to connect users to the site social media
* Responsive on all devices
* Register to create an account
* View recipes created by the community show as cards
* Users can add their own recipes to the collection
* User can edit their own recipes 
* User can delete their own recipes
* Admin account created for the site owner
* Admin can add, edit or delete any recipes in the collection to keep things clean
* Search bar 
* Recipes card showing the full detail of a particular recipe

**Future Implementations**

There were a few more ideas that I had for the site that could be implemented in the future.

* Profile page account, showing their own collection of their own recipes
* Live count of their own recipes on the profile page.
* Live count of recipes in the community collection on the home page
* Accept images files as an alternative to URL links
* User can delete their own account


## Technology Used

**Language Used**

* HTML5
* CSS3
* JavaScript
* Python

**Frameworks, Libraries, and Programs Used**

* [Google Font](https://fonts.google.com/)
    * The font 'Poppins' was imported from Google Font.
* [Font Awesome](https://fontawesome.com/)
    * Used to get some icons for the site.
* [Gitpod](https://www.gitpod.io/)
    * Gitpod is the development environment used to develop the project.
* [GitHub](https://github.com/)
    * GitHub is used to store the code for the site.
* [Git](https://git-scm.com/)
    * Git was used as version control, to add, commit and push Git and GitHub.
* [Balsamiq](https://balsamiq.com/)
    * Used to create wireframes for the website.
* [Google Developer Chrome Tools](https://developers.google.com/web/tools/chrome-devtools)
    * Used to inspect elements of the page and debug any potential problems within the website.
* [Unsplash](https://unsplash.com/)
    * Used to get stock-free images for the project.
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
    * Used as an application framework
* [Materialize](https://materializecss.com/)
    * Used to create a responsive site.
* [MongoDB](https://www.mongodb.com/)
    * Used to create and store content as a database.
* [jQuery](https://jquery.com/)
    * Used to work with Materialize framework
* [PyMongo](https://pypi.org/project/pymongo/)
    * Used to work with MongoDB.
* [Flask-PyMongo](https://pypi.org/project/Flask-PyMongo/)
    * Used as a bridge to communicate between Flask and PyMongo.
* [Flask-Paginate](https://pypi.org/project/flask-paginate/)
    * Used to provide pagination functionality.
* [Jinja](https://jinja.palletsprojects.com/)
    * Used as a templating language for Python to display backend data to HTML.
* [Werkzeug](https://werkzeug.palletsprojects.com/en/2.0.x/utils/#module-werkzeug.security)
    * Used to get protection for passwords.
* [Coolors](https://coolors.co/)
    * Used to create a cohesive color scheme for the website.
* [Heroku](https://www.heroku.com/)
    * Used to deploy the website.

 ## Issues

 There is a known issue with the footer that is not completely sticking to the bottom. As shown in the screenshot below:

![Screenshot of issue with footer.](static/image/readme/footer-issue.png "Screenshot of footer issue.")

There is a known issue with the search bar buttons when viewed on mobile. 
There is no spacing between the buttons. As shown in the screenshot below:

![Button issue on mobile.](static/image/readme/button-issue.png "Button issue.")

This was solved by creating a row for just the buttons. 

![Solved button issue on mobile.](static/image/readme/solved-button-issue.png "Solved button issue.")

As part of developing the site, wanted to create a live counter to display the number of recipes in the database as part of promoting the site on its home page.
It displays incorrectly, therefore have decided to delete the code from the site.
The code is shown below:

In app.py
```
@app.route("/number")
def number():
   result = mongo.db.recipes.find().count()
   return result
```

In home.html page
```
{{ url_for('number') }}
```

It displays as “/number” instead of an actual number of recipes.

As part of developing the site, I wanted to limit what the user can edit or delete a recipe.
The user can only edit or delete their own recipes but not of other recipes created by other users. I wanted to check if the username is in session and if the recipe is created by said username, the user can delete/edit. If they are not logged in or the recipe is not created by the said username, it does not authorize the user to delete. The code is shown below, 

```
@app.route("/delete_recipe/<recipes_id>")
def delete_recipe(recipes_id):
   if "username" in session:
       user = session["username"]
       recipes = mongo.db.recipes.find_one({"_id": ObjectId(recipes_id)})
       if recipes["created_by"] == user:
               mongo.db.recipes.remove({"_id": ObjectId(recipes_id)})
               flash("Recipe Successfully Deleted")
       else:
           flash("Sorry, you are not allowed to do this")
           return redirect(url_for("get_recipe"))
   else:
       flash("Sorry, you must log in")
       return redirect(url_for("login"))
   return redirect(url_for("get_recipe"))
```

The problem was that it bypass it straight to “sorry, you must log in” as it does not check if the username is in session. But thanks to another student named Manni, he provided his own code on a similar feature. So I could compare, the problem was that the `username` needed to be `user` and it solved the issue.


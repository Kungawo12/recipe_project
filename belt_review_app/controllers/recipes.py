from flask import render_template,request, redirect,session,flash
from belt_review_app import app
from belt_review_app.models.recipe import Recipe
from belt_review_app.models.user import User

@app.route('/recipe/new')
def new_recipe():
    data = {
        'id': session['user_id']
    }
    user = User.show_user(data)
    return render_template("new_recipe.html", user = user)

@app.route('/create/new', methods= ['POST'])
def create_recipe():
    under_30_minutes = request.form['under_30_minutes'] =="Yes"
    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "under_30_minutes": under_30_minutes,
        "date_cooked": request.form['date_cooked'],
        "user_id": request.form["user_id"]
    }
    Recipe.save_recipe(data)
    return redirect('/recipe')


@app.route('/recipe/<int:id>')
def show_recipe(id):
    data={
        "id":id
    }
    user_data = {
        'id': session['user_id']
    }
    recipe_data = Recipe.show_one_recipe(data)
    return render_template("recipe_board.html",recipe = recipe_data,user= User.show_user(user_data))

@app.route("/recipe/edit/<int:id>")
def edit_recipe(id):
    data={
        "id":id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template("edit_recipe.html",recipe= Recipe.show_one_recipe(data), user= User.show_user(user_data))

@app.route('/update/recipe', methods= ['POST'])
def update_recipe():
    under_30_minutes = request.form['under_30_minutes'] =="Yes"
    recipe_id = request.form['recipe_id']
    
    data = {
        "id": recipe_id,
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "under_30_minutes": under_30_minutes,
        "date_cooked": request.form['date_cooked'],
        "user_id": request.form["user_id"]
    }
    Recipe.update_recipe(data)
    return redirect('/recipe')

@app.route("/recipe/delete/<int:id>")
def delete_recipe(id):
    data={
        "id": id
    }
    print(data)
    Recipe.delete_recipe(data)
    return redirect('/recipe')


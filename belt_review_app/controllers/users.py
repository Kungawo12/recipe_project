from flask import render_template,request, redirect,session,flash
from belt_review_app.models.user import User
from belt_review_app.models.recipe import Recipe
from belt_review_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("login.html")



@app.route('/recipe')
def recipe():
    if 'user_id' not in session:
        flash('Please log in to view this page', "login")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    all_recipe= Recipe.get_all_recipe()
    return render_template('recipe.html', user= User.show_user(data),recipes = all_recipe)


@app.route('/user/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    user_data = {
        "email": request.form['email']
    }
    user = User.get_by_email(user_data)
    if user:
        flash("Email already in use, please log in", 'email')
        return redirect('/')
    data={
        'first_name': request.form['first_name'], 
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']) 
    }
    id = User.save(data)
    session['user_id'] = id
    print(user)
    return redirect('/recipe')

@app.route('/user/login', methods = ['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    data = {
        "email": request.form['log_email']
    }
    user = User.get_by_email(data)
    
    if not user:
        flash('Invalid Email', "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['log_password']):
        flash('Invalid Password', "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/recipe')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
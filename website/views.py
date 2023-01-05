from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, session, url_for
from flask_login import login_user, login_required, current_user, logout_user
from .functions import *
from .forms import *
from .crud import *
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint("views", __name__)


@views.route('/', defaults={'path': ''})
@views.route('/<string:path>')
@views.route('/<path:path>')
def catch_random_paths(path):
    """
    Catches all URL paths that aren't specified and sends to the home page.
    """
    return redirect(url_for("views.home"))


@views.route('/', methods=['POST', 'GET'])
def home():
    register_form = RegisterForm()
    login_form = LoginForm()
    return render_template("homepage.html", login_form=login_form, register_form=register_form)


@views.route('/about')
def about():
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template("about.html", login_form=login_form, register_form=register_form)


@views.route('/register', methods=["POST", "GET"])
def register():
    register_form = RegisterForm()
    if request.method == "POST":
        print(register_form.password.data)
        print(register_form.confirm_password.data)
        if not valid_email(register_form.email.data):
            flash(u"Invalid e-mail address!", 'error')
            return '<script>document.location.href = document.referrer</script>'

        elif not register_form.number.data.isdigit():
            flash(u"Invalid phone number!", 'error')
            return '<script>document.location.href = document.referrer</script>'
        elif register_form.password.data != register_form.confirm_password.data:
            flash(u"Password and Confirm Password did not match!", 'error')
            return '<script>document.location.href = document.referrer</script>'

        else:
            user = User.query.filter_by(email=register_form.email.data).first()
            if user:
                flash(u"You are already signed up with that email, log in instead!", 'error')
                return '<script>document.location.href = document.referrer</script>'
            user = User.query.filter_by(number=register_form.number.data).first()
            if user:
                flash(u"Someone is already using this phone number! Please enter a different one.", 'error')
                return '<script>document.location.href = document.referrer</script>'
            hash_and_salted_password = generate_password_hash(
                register_form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            user = create_user(
                register_form.email.data,
                hash_and_salted_password,
                int(register_form.number.data)
            )

            login_user(user)
            flash(u'Successfully created new account!', 'success')
            return '<script>document.location.href = document.referrer</script>'
    return redirect(url_for('views.home'))


@views.route('/login', methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if request.method == "POST":
        print("working login")
        print(login_form.email.data)
        email = login_form.email.data
        password = login_form.password.data

        # Find user by email
        user = User.query.filter_by(email=email).first()

        # Email doesn't exist
        if not user:
            flash(u"That e-mail does not exist, please try again.", 'error')
            return '<script>document.location.href = document.referrer</script>'
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash(u'Password incorrect, please try again.', 'error')
            return '<script>document.location.href = document.referrer</script>'
        # Email exists and password correct
        else:
            login_user(user)
            flash(u'Valid user. Successfully logged in.', 'success')
            return '<script>document.location.href = document.referrer</script>'
    return redirect(url_for("views.home"))


@views.route('/logout', methods=["POST", "GET"])
@login_required
def logout():
    if request.method == "POST":
        logout_user()
        flash("Successfully logged out.", "neutral")
        return '<script>document.location.href = document.referrer</script>'
    return redirect(url_for("views.home"))


@views.route('/search_recipe', methods=["GET", "POST"])
def search_recipe():
    if request.method == 'POST':

        print("post dziala")
        given_ingredients = request.form["ingredients"]
        session['given_ingredients'] = given_ingredients
        print("ingredient dziala")

        sort = None
        vegetarian = None
        gluten_free = None

        try:
            sort = request.form["sort"]
            session['sort'] = sort
            print("sort dziala")
        except Exception as e:
            session['sort'] = None
            print("sort " + str(e))

        try:
            vegetarian = request.form["vegetarian"]
            session['vegetarian'] = vegetarian
            print("vegetarian dziala")
        except Exception as e:
            session['vegetarian'] = None
            print("veg " + str(e))

        try:
            gluten_free = request.form["gluten_free"]
            session['gluten_free'] = gluten_free
            print("gluten_free dziala")
        except Exception as e:
            session['gluten_free'] = None
            print("glu " + str(e))

        return redirect(url_for("views.show_recipes"))


@views.route('/search-results', methods=["GET", "POST"])
def show_recipes():
    print("show recipes work")
    sort = None
    vegetarian = None
    gluten_free = None

    register_form = RegisterForm()
    login_form = LoginForm()
    given_ingredients = session.get('given_ingredients', None)
    print("show recipes work")
    try:
        sort = session.get('sort', None)
        print("sort 2 dziala")
        print(sort)
    except Exception as e:
        print(str(e))

    try:
        vegetarian = session.get('vegetarian', None)
    except Exception as e:
        print(str(e))

    try:
        gluten_free = session.get('gluten_free', None)
    except Exception as e:
        print(str(e))

    print(sort)
    recipe_results = getRecipes(given_ingredients, sort=sort, vegetarian=vegetarian, gluten_free=gluten_free)
    if not current_user.is_anonymous:
        saved_ids = {saved['recipe_id'] for saved in get_saved_recipes(current_user.email)}
    else:
        saved_ids = []

    return render_template('search-recipe.html', recipes=recipe_results, login_form=login_form,
                           register_form=register_form, saved_ids=saved_ids)


@views.route('/to-add-recipe/<int:id>/<todo>', methods=['POST', "GET"])
def to_add_recipe(id, todo):
    print(todo)

    sort = None
    vegetarian = None
    gluten_free = None

    try:
        sort = session.get('sort', None)
    except Exception as e:
        print(str(e))

    try:
        vegetarian = session.get('vegetarian', None)
    except Exception as e:
        print(str(e))

    try:
        gluten_free = session.get('gluten_free', None)
    except Exception as e:
        print(str(e))

    # It's to prevent error when entering route through saved recipes
    if todo == "toView":
        print("toView dziala")
        todo = id
        session['todo'] = todo
        return redirect(url_for('views.recipe_info'))

    session['todo'] = todo
    given_ingredients = session.get('given_ingredients', None)
    all_recipes = getRecipes(given_ingredients, sort=sort, vegetarian=vegetarian, gluten_free=gluten_free)

    lista_recipes = [recipe['recipe_id'] for recipe in all_recipes]
    print(lista_recipes)
    for recipe in all_recipes:
        if recipe['recipe_id'] == id:
            session['recipe'] = recipe
            return redirect(url_for('views.add_recipe_to_db'))
    print("działam6")
    return '<script>document.location.href = document.referrer</script>'


@views.route('/add-recipe', methods=["POST", "GET"])
def add_recipe_to_db():
    print("add-recipe działa")
    # """Add selected recipe to recipes table in db."""
    recipe_details = session.get('recipe', None)
    todo = session.get('todo', None)
    recipe_id = recipe_details['recipe_id']

    # find if recipe already exists in db
    existing_recipe = quick_get_recipe(recipe_id)

    if existing_recipe != None:
        if todo == "toSave":
            return redirect(url_for('views.save_recipe'))
        elif todo == "toShow":
            return redirect(url_for('views.recipe_info'))
        else:
            return redirect(url_for('views.home'))

    print('\n new recipe, adding to db \n')
    title = recipe_details['title']
    image = recipe_details['image']
    servings = recipe_details['servings']
    sourceUrl = recipe_details['sourceUrl']
    cooking_mins = recipe_details['cooking_mins']
    prep_mins = recipe_details['prep_mins']
    ready_mins = recipe_details['ready_mins']
    vegetarian = recipe_details['vegetarian']
    gluten_free = recipe_details['gluten_free']
    # add recipe's title, image, and servings to recipes table in db
    create_recipe(recipe_id=recipe_id, title=title, image=image, servings=servings, sourceUrl=sourceUrl,
                  cooking_mins=cooking_mins, prep_mins=prep_mins, ready_mins=ready_mins, vegetarian=vegetarian,
                  gluten_free=gluten_free)

    # add each individual ingredient of recipe to db.
    for ingredient in recipe_details['ingredients']:
        ingredient_id = ingredient['ingredient_id']
        name = ingredient['name']
        amount = ingredient['amount']
        unit = ingredient['unit']
        add_recipe_ingredient(recipe=recipe_id, ingredient_id=ingredient_id, amount=amount, unit=unit, name=name)

    for ingredient in recipe_details['missing_ingredients']:
        ingredient_id = ingredient['ingredient_id']
        name = ingredient['name']
        amount = ingredient['amount']
        unit = ingredient['unit']
        add_recipe_missing_ingredient(recipe=recipe_id, ingredient_id=ingredient_id, amount=amount, unit=unit,
                                      name=name)

    # add each instructions step and string to db
    try:
        for i, instruction in enumerate(recipe_details['instructions']):
            # set step_num by adding 1 to indices
            step_num = i + 1
            step_instruction = instruction
            add_instructions(recipe=recipe_id, step_num=step_num, step_instruction=step_instruction)
    except Exception as e:
        print(str(e))

    try:
        # add each key of equipment to db
        for equipment in recipe_details['equipment']:
            add_equipment(recipe=recipe_id, equipment=equipment)
    except Exception as e:
        print(str(e))

    if todo == "toSave":
        return redirect(url_for('views.save_recipe'))
    elif todo == "toShow":
        return redirect(url_for('views.recipe_info'))
    else:
        return redirect(url_for('views.home'))


@views.route('/recipe_info')
def recipe_info():
    todo = str(session.get('todo', None))

    # When we enter from 'saved list' page, a 'to-do' variable is a digit. It is done to skip all processes when the
    # recipe is already saved in db.
    if todo.isdigit():
        recipe_id = todo
    else:
        recipe_details = session.get('recipe', None)
        recipe_id = recipe_details['recipe_id']
    print(recipe_id)
    recipe = get_recipe(recipe_id)
    register_form = RegisterForm()
    login_form = LoginForm()

    if not current_user.is_anonymous:
        saved_ids = {saved['recipe_id'] for saved in get_saved_recipes(current_user.email)}
    else:
        saved_ids = []
    print(recipe)

    session['recipe_id'] = recipe.recipe_id
    return render_template('recipe-info.html', recipe=recipe, login_form=login_form, register_form=register_form,
                           saved_ids=saved_ids)


@views.route('/save-recipe', methods=["POST", "GET"])
@login_required
def save_recipe():
    """Add selected recipe to saved recipes table in db

    Only logged-in users can save one recipe at a time (one recipe_id passed in POST request body)."""

    recipe = session.get('recipe', None)
    recipe_id = recipe['recipe_id']
    users_saved_recipes = get_saved_recipes(current_user.email)

    # if user's saved recipes db has data
    if len(users_saved_recipes) > 0:
        # iterate and check if recipe already saved
        for saved in users_saved_recipes:
            if saved['recipe_id'] == recipe_id:
                flash('Recipe already exists in your saved list.', "neutral")
                return '<script>document.location.href = document.referrer</script>'

    # if selected recipe NOT in saved, or user's saved recipes is empty
    print('\nselected recipe NOT in db, or user\'s saved recipes is empty\n')
    user = get_user_by_email(current_user.email)
    save_a_recipe(user=user.user_id, recipe=recipe_id, is_favorite=False)
    flash(u'Recipe saved!', "success")

    return '<script>document.location.href = document.referrer</script>'


@views.route('/remove-saved-recipe/<int:id>', methods=['POST', "GET"])
@login_required
def remove_saved_recipe(id):
    if request.method == "GET":
        print("removing recipe...")
        remove_recipe(id, current_user.email)
        flash(u'Recipe deleted!', "error")
        session['recipe_id'] = id
        return '<script>document.location.href = document.referrer</script>'


@views.route('/saved-recipes')
@login_required
def saved_recipes():
    users_saved_recipes = get_saved_recipes(current_user.email)
    saved_ids = {saved['recipe_id'] for saved in users_saved_recipes}
    print(saved_ids)

    recipes = [get_saved_recipe(x) for x in saved_ids]

    for x in saved_ids:
        recipe = get_saved_recipe(x)

    print(recipes)

    return render_template("saved-recipes.html", recipes=recipes)


@views.route('/send-to-phone', methods=["POST", "GET"])
@login_required
def send_to_phone():
    recipe_id = session.get('recipe_id', None)
    if request.method == 'POST':
        recipe = get_recipe(recipe_id)

        shop_list = []

        i = 1
        for x in range(len(recipe.missing_ingredients)):
            try:
                print(request.form[f"ingredient-{x}"])
                missing_ingredient = ("• " + request.form[f"ingredient-{x}"])

                shop_list.append(missing_ingredient)
                i += 1
            except Exception as e:
                print(str(e))

        print(shop_list)

        # Test number
        if current_user.number != 726396036:
            flash("For now it only works with the numbers set by me.", "error")
            return '<script>document.location.href = document.referrer</script>'

        response = sendSMS(current_user.number, shop_list, recipe.title)

        if response == 'success':
            flash("Successfully sent an SMS with the shopping list to your phone number!", "success")
            return '<script>document.location.href = document.referrer</script>'

        else:
            return jsonify({"error": response})

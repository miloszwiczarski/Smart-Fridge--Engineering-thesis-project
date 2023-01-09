"""CRUD operations
Create, Read, Update, Delete."""

from .models import db, User, Saved_Recipe, Recipe, Recipe_Ingredient, Instructions, Equipment, Missing_Ingredient



# ***** User class crud functions *****

def create_user(email, password, number):
    """Create a user."""

    # Instantiate a User
    user = User(email=email, password=password, number=number)

    # add new instance of user to db and commit
    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_email(email):
    """Retrieve user by email."""

    # Use .first() so if none, then won't throw error
    return db.session.query(User).filter_by(email=email).first()


def get_user_number(email):
    """Return user's phone number by email."""
    number = db.session.query(User.number).filter_by(email=email).first()

    return number


# ***** Saved Recipe class crud functions *****

def save_a_recipe(user, recipe):
    """Saves a recipe user picked."""

    # Instantiate a saved recipe
    saved_recipe = Saved_Recipe(user_id=user, recipe_id=recipe)

    # add to database
    db.session.add(saved_recipe)
    db.session.commit()

    return


def get_saved_recipes(email):
    """Show all of user's saved recipes.

    Return a list of user's saved recipes as objects."""

    # eagarly load query so can access each saved recipe's ingredients, details, and instructions

    # some recipes do not have instructions due to sth
    try:
        user = User.query.filter_by(email=email).join(Saved_Recipe, Recipe, Recipe_Ingredient, Instructions).first()
        print()
    except Exception as e:
        print(str(e))
        user = User.query.filter_by(email=email).join(Saved_Recipe, Recipe, Recipe_Ingredient).first()

    # if user does not have any saved_recipes
    if user == None:
        return []

    saved_list = [saved.as_dict() for saved in user.saved_recipes]

    return saved_list


def get_a_saved_recipe(recipe_id, email):
    """Return saved recipe object given id and user's email."""

    saved_recipe = db.session.query(Saved_Recipe).filter(User.email == email).group_by(Saved_Recipe.recipe_id,
                                                                                       Saved_Recipe.saved_id).having(
        Saved_Recipe.recipe_id == recipe_id).join(User, Recipe,
                                                  Recipe_Ingredient,
                                                  Instructions).first()

    return saved_recipe


# ***** Recipe class crud functions *****

def create_recipe(recipe_id, title, image, servings, sourceUrl, cooking_mins, prep_mins, ready_mins, vegetarian,
                  gluten_free):
    """Create a recipe."""

    # Instantiate a recipe
    recipe = Recipe(recipe_id=recipe_id, title=title, image=image, servings=servings, sourceUrl=sourceUrl,
                    cooking_mins=cooking_mins, prep_mins=prep_mins, ready_mins=ready_mins, vegetarian=vegetarian,
                    gluten_free=gluten_free)

    # add to database
    db.session.add(recipe)
    db.session.commit()

    return


def get_saved_recipe(recipe_id):
    """Retrieve a recipe from database."""

    # some recipes do not have instructions due to sth
    recipe = db.session.query(Recipe).filter(Recipe.recipe_id == recipe_id).join(Saved_Recipe, User,
                                                                                 Recipe_Ingredient, Instructions,
                                                                                 Missing_Ingredient).first()
    if not recipe:
        recipe = db.session.query(Recipe).filter(Recipe.recipe_id == recipe_id).join(Saved_Recipe, User,
                                                                                     Recipe_Ingredient,
                                                                                     Missing_Ingredient).first()
    return recipe


def get_recipe(recipe_id):
    """Retrieve a recipe from database."""
    print("Get recipe w CRUD dziala")
    # some recipes do not have instructions due to sth
    recipe = db.session.query(Recipe).filter(Recipe.recipe_id == recipe_id).join(Recipe_Ingredient, Instructions,
                                                                                 Missing_Ingredient).first()

    if not recipe:
        try:
            recipe = db.session.query(Recipe).filter(Recipe.recipe_id == recipe_id).join(Recipe_Ingredient,
                                                                                         Missing_Ingredient).first()
        except Exception as e:
            print(str(e))

    return recipe


def quick_get_recipe(id_num):
    """Return recipe_id if exists in db."""

    # some recipes do not have instructions due to sth

    recipe = Recipe.query.filter_by(recipe_id=id_num).first()

    return recipe


def add_recipe_ingredient(recipe, ingredient_id, amount, unit, name):
    """Add a recipe's ingredient to database."""

    # Instantiate a recipe's ingredient

    recipe_ingredient = Recipe_Ingredient(recipe_id=recipe, ingredient_id=ingredient_id, amount=amount, unit=unit,
                                          name=name)

    # add to database
    db.session.add(recipe_ingredient)
    db.session.commit()

    return


def add_recipe_missing_ingredient(recipe, ingredient_id, amount, unit, name):
    """Add a recipe's ingredient to database."""

    # Instantiate a recipe's ingredient
    missing_ingredient = Missing_Ingredient(recipe_id=recipe, ingredient_id=ingredient_id, amount=amount, unit=unit,
                                            name=name)

    # add to database
    db.session.add(missing_ingredient)
    db.session.commit()

    return


def add_instructions(recipe, step_num, step_instruction):
    """Add recipe's instructions, one by one, to databasee."""

    # Instantiate a recipe's instructions
    instructions = Instructions(recipe_id=recipe, step_num=step_num, step_instruction=step_instruction)

    # add to database
    db.session.add(instructions)
    db.session.commit()

    return


def add_equipment(recipe, equipment):
    """Add recipe's equipment, one by one, to database."""

    # Instantiate a recipe's equipment
    equipment = Equipment(recipe_id=recipe, equipment=equipment)

    # add to database
    db.session.add(equipment)
    db.session.commit()

    return


def remove_recipe(recipe_id, email):
    """Remove recipe from user's saved recipes."""

    saved_recipe = db.session.query(Saved_Recipe).filter(Saved_Recipe.recipe_id == recipe_id,
                                                         User.email == email).first()
    # recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()

    # delete from database
    # db.session.delete(recipe)
    db.session.delete(saved_recipe)
    db.session.commit()

    return True

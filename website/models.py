from . import db
from flask_login import UserMixin



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    saved_recipes = db.relationship('Saved_Recipe', lazy='joined')

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f'<User id={self.user_id} email={self.email}>'

    def as_dict(self):
        return {'user_id': self.user_id,
                'email': self.email,
                'number': self.number,
                'saved_recipes': self.saved_recipes}


class Saved_Recipe(db.Model):
    """User's saved recipes."""

    __tablename__ = 'saved_recipes'

    saved_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipes.recipe_id'))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))

    # recipe that was saved
    recipe = db.relationship('Recipe', lazy='joined')
    # user who saved the recipe
    user = db.relationship('User', lazy='joined')

    def __repr__(self):
        return f'<User\'s selected recipes recipe={self.recipe_id} user={self.user_id} is_favorite={self.favorite}>'

    def as_dict(self):
        return {'saved_id': self.saved_id,
                'recipe_id': self.recipe_id,
                'user_id': self.user_id,
                'recipe': self.recipe,
                'user': self.user}


class Recipe(db.Model):
    """A recipe."""

    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer,
                          primary_key=True)
    title = db.Column(db.String)
    image = db.Column(db.String)
    servings = db.Column(db.Integer)
    sourceUrl = db.Column(db.String)
    cooking_mins = db.Column(db.Integer)
    prep_mins = db.Column(db.Integer)
    ready_mins = db.Column(db.Integer)
    gluten_free = db.Column(db.Boolean)
    vegetarian = db.Column(db.Boolean)

    # list of recipe's ingredients
    ingredients = db.relationship('Recipe_Ingredient', lazy='joined')
    # list of recipe's ingredients
    missing_ingredients = db.relationship('Missing_Ingredient', lazy='joined')
    # list of recipe's instructions by steps (length is number of steps)
    instructions = db.relationship('Instructions', lazy='joined')
    # list of instances this recipe is saved by many different users
    saved_recipe_users = db.relationship('Saved_Recipe', lazy='joined')
    # list of recipe's equipment(s)
    equipment = db.relationship('Equipment', lazy='joined')

    def __repr__(self):
        return f'<Recipe recipe_id={self.recipe_id} title={self.title}>'

    def as_dict(self):
        return {'recipe_id': self.recipe_id,
                'title': self.title,
                'image': self.image,
                'servings': self.servings,
                'sourceUrl': self.sourceUrl,
                'cooking_mins': self.cooking_mins,
                'prep_mins': self.prep_mins,
                'ready_mins': self.ready_mins,
                'ingredients': self.ingredients,
                'instructions': self.instructions,
                'equipment': self.equipment}


class Recipe_Ingredient(db.Model):
    """A recipe's ingredient."""

    __tablename__ = 'recipe_ingredients'

    rec_ing_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipes.recipe_id'))
    ingredient_id = db.Column(db.Integer)
    amount = db.Column(db.Float(precision=2))
    unit = db.Column(db.String)
    name = db.Column(db.String)

    # the recipe the ingredient is part of
    recipe = db.relationship('Recipe', lazy='joined')

    def __repr__(self):
        return f'<Recipe Ingredient recipe={self.recipe_id} ingredient={self.name}>'

    def as_dict(self):
        return {'rec_ing_id': self.rec_ing_id,
                'recipe_id': self.recipe_id,
                'ingredient_id': self.ingredient_id,
                'amount': self.amount,
                'unit': self.unit,
                'name': self.name}


class Missing_Ingredient(db.Model):
    """A recipe's missing ingredient."""

    __tablename__ = 'missing_ingredients'

    rec_ing_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipes.recipe_id'))
    ingredient_id = db.Column(db.Integer)
    amount = db.Column(db.Float(precision=2))
    unit = db.Column(db.String)
    name = db.Column(db.String)

    # the recipe the missing ingredient is part of
    recipe = db.relationship('Recipe', lazy='joined')

    def __repr__(self):
        return f'<Recipe Ingredient recipe={self.recipe_id} ingredient={self.name}>'

    def as_dict(self):
        return {'rec_ing_id': self.rec_ing_id,
                'recipe_id': self.recipe_id,
                'ingredient_id': self.ingredient_id,
                'amount': self.amount,
                'unit': self.unit,
                'name': self.name}


class Instructions(db.Model):
    """A recipe's instructions."""

    __tablename__ = 'instructions'

    instruction_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipes.recipe_id'))
    step_num = db.Column(db.Integer)
    step_instruction = db.Column(db.String)

    # recipe the instructions are for
    recipe = db.relationship('Recipe', lazy='joined')

    def __repr__(self):
        return f'<Instructions recipe={self.recipe_id} step={self.step_num}>'

    def as_dict(self):
        return {'instruction_id': self.instruction_id,
                'recipe_id': self.recipe_id,
                'step_num': self.step_num,
                'step_instruction': self.step_instruction}


class Equipment(db.Model):
    """A recipe's equipment."""

    __tablename__ = 'equipment'

    equipment_id = db.Column(db.Integer,
                             autoincrement=True,
                             primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipes.recipe_id'))
    equipment = db.Column(db.String)

    # recipe the equipment is part of
    recipe = db.relationship('Recipe', lazy='joined')

    def __repr__(self):
        return f'<Equipment recipe={self.recipe_id} equipment={self.equipment}>'

    def as_dict(self):
        return {'equipment_id': self.equipment_id,
                'recipe_id': self.recipe_id,
                'equipment': self.equipment}

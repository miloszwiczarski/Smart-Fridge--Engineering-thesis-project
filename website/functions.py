import re
import requests
from flask import request
import json
import os
from twilio.rest import Client


def getRecipes(given_ingredients, sort, vegetarian, gluten_free):
    """ Sends a request to Spoonacular API for the recipes """

    SPOON_ENDPOINT = "https://api.spoonacular.com/recipes/complexSearch"
    SPOON_KEY = os.environ["SPOONACULAR_KEY"]
    params = {
        "includeIngredients": given_ingredients,
        "instructionsRequired": True,
        "fillIngredients": True,
        'limitLicense': False,
        "sort": "max-used-ingredients",
        # "sort": "min-missing-ingredients",
        "addRecipeInformation": True,
        "number": 15,
        "ignorePantry": True,
        # "vegetarian": vegetarian,
        # "glutenFree": gluten_free
    }

    if sort:
        params["sort"] = sort

    if vegetarian:
        params["vegetarian"] = vegetarian

    if gluten_free:
        params["gluten_free"] = gluten_free

    headers = {
        "x-api-key": SPOON_KEY,
    }
    print(sort)
    spoonacular_response = requests.get(SPOON_ENDPOINT, params, headers=headers)
    data = spoonacular_response.json()

    recipes_complex_data = data['results']
    #
    # with open("all_recipes.json") as f:
    #     to_read = f.read()
    #
    # x = json.loads(to_read)
    # recipes_complex_data = x['results']

    recipe_results = []
    # parse only details we need from api endpoint
    for recipe in recipes_complex_data:
        recipe_data = parse_API_recipe_details(recipe)
        recipe_results.append(recipe_data)

    return recipe_results


def valid_email(e_mail):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, e_mail):
        return True
    else:
        return False


def parse_API_recipe_details(complex_data):
    """Parse only details we need from bulk/complex API endpoint."""

    recipe_data = {
        'recipe_id': complex_data['id'],
        'title': complex_data['title'],
        'servings': complex_data['servings'],
        'sourceUrl': complex_data['sourceUrl'],
        'image': complex_data['image'],
        'prep_mins': complex_data.get('preparationMinutes', 0),
        'cooking_mins': complex_data.get('cookingMinutes', 0),
        'ready_mins': complex_data.get('readyInMinutes', 0),
        'vegetarian': complex_data['vegetarian'],
        'gluten_free': complex_data['glutenFree']
    }

    # parse ingredients list, each ingredient is dictionary of details
    ingredients = []
    for ingredient in complex_data['extendedIngredients']:
        ingredient_dict = {
            'ingredient_id': ingredient['id'],
            'name': ingredient['name'],
            'amount': round(ingredient['measures']['metric']['amount'], 2),
            'unit': (ingredient['measures']['metric']['unitShort']).lower()
        }

        if ingredient['measures']['metric']['unitShort'] == 'ml':
            amount = (round(ingredient['measures']['metric']['amount'] / 10)) * 10
            ingredient_dict['amount'] = amount

        elif ingredient['measures']['metric']['unitShort'] == 'qt':
            ingredient_dict['unit'] = "ml"
            amount = (round((ingredient['measures']['metric']['amount'] * 946.353) / 10)) * 10
            ingredient_dict['amount'] = amount

        if ingredient['measures']['metric']['unitShort'] == 'g':
            amount = (round(ingredient['measures']['metric']['amount'] / 10)) * 10
            ingredient_dict['amount'] = amount

        ingredients.append(ingredient_dict)
    recipe_data['ingredients'] = ingredients

    # parse instructions, as list of string instructions
    try:
        instructions = [step['step'] for step in complex_data['analyzedInstructions'][0]['steps']]
        recipe_data['instructions'] = instructions
    except Exception as e:
        print(str(e))

    # parse equipment as dictionary, no duplicate equipment
    try:
        equipment = {
            equipment['name']: equipment['name']
            for step in complex_data['analyzedInstructions'][0]['steps']
            for equipment in step['equipment']
        }
        recipe_data['equipment'] = equipment
    except Exception as e:
        print(str(e))

    missed_ingredients = []
    for ingredient in complex_data['missedIngredients']:
        ingredient_dict = {
            'ingredient_id': ingredient['id'],
            'name': ingredient['name'],
            'amount': round(ingredient['amount'], 2),
            'unit': (ingredient['unitShort']).lower()
        }

        if ingredient['unitShort'] == 'qt':
            ingredient_dict['unit'] = "ml"
            amount = (round((ingredient['amount'] * 946.353) / 10)) * 10
            ingredient_dict['amount'] = amount

        elif ingredient['unitShort'] == 'oz':
            ingredient_dict['unit'] = "g"
            amount = (round((ingredient['amount'] * 28.35) / 10)) * 10
            ingredient_dict['amount'] = amount

        elif ingredient['unitShort'] == 'lb':
            ingredient_dict['unit'] = "g"
            amount = (round((ingredient['amount'] * 0.45359237 * 1000) / 10)) * 10
            ingredient_dict['amount'] = amount

        elif ingredient['unitShort'] == 'g':
            ingredient_dict['unit'] = "g"
            amount = (round((ingredient['amount'] * 0.45359237 * 1000) / 10)) * 10
            ingredient_dict['amount'] = amount

        # elif ingredient['unitShort'] == 'cup':
        #     ingredient_dict['unit'] = "ml"
        #     amount = (round((ingredient['amount'] * 236.5882365)/10)) * 10
        #     ingredient_dict['amount'] = amount

        missed_ingredients.append(ingredient_dict)
    recipe_data['missing_ingredients'] = missed_ingredients

    return recipe_data


def sendSMS(number, shopping_list, title):
    # Set environment variables for your credentials
    # Read more at http://twil.io/secure
    account_sid = "ACbf36215fed1edc7330ce7b60bf9dd696"
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)
    shopping_list_ready = [x + "\n" for x in shopping_list]
    print(shopping_list_ready)
    sms_text = f"Thanks for using Smart Fridge!\n\n{title} shopping list:\n"
    for x in shopping_list_ready:
        sms_text += x
    print(sms_text)
    print(number)

    try:
        message = client.messages.create(
            body=sms_text,
            from_="SmartFridge",
            to=f"+48{number}"
        )
        print(message.sid)
        return "success"
    except Exception as e:
        print(str(e))
        return str(e)

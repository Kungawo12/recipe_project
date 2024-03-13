from belt_review_app.config.mysqlconnection import connectToMySQL
from .user import User
from flask import flash
class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30_minutes = data['under_30_minutes']
        self.date_cooked = data['date_cooked']
        self.user = None
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    
    @classmethod
    def save_recipe(cls,data):
        query = """INSERT INTO recipes(name,description,instructions,under_30_minutes,date_cooked, user_id)
                VALUES(%(name)s,%(description)s,%(instructions)s,%(under_30_minutes)s,%(date_cooked)s,%(user_id)s);
        """
        return connectToMySQL('recipe_db').query_db(query,data)
    
    @classmethod
    def get_all_recipe(cls):
        query= """SELECT * FROM recipes
                LEFT JOIN users on recipes.user_id = users.id;
            """
        results = connectToMySQL('recipe_db').query_db(query)
        
        user_with_recipe =[]
        for row in results:
            recipe_data = Recipe(row)
            user_data = User({
                "id": row["user_id"],
                "first_name": row["first_name"],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                "created_at": row["created_at"],
                "updated_at": row['updated_at']
            })
            recipe_data.user = user_data
            
            user_with_recipe.append(recipe_data)
        return user_with_recipe
    
    @classmethod
    def show_one_recipe(cls,data):
        query= """SELECT * FROM recipes JOIN
        users ON recipes.user_id = users.id
        WHERE recipes.id= %(id)s;
        """
        
        results = connectToMySQL('recipe_db').query_db(query,data)
        recipe_dict =results[0]
        recipe_obj = cls(recipe_dict)
        user_obj = User({
                "id": recipe_dict["user_id"],
                "first_name": recipe_dict["first_name"],
                'last_name': recipe_dict['last_name'],
                'email': recipe_dict['email'],
                'password': recipe_dict['password'],
                "created_at": recipe_dict["created_at"],
                "updated_at": recipe_dict['updated_at']
        })
        recipe_obj.user = user_obj
        return recipe_obj
    
    @classmethod
    def update_recipe(cls,data):
        query="""UPDATE recipes
        SET name= %(name)s,description = %(description)s,
        instructions= %(instructions)s,under_30_minutes= %(under_30_minutes)s,
        date_cooked= %(date_cooked)s, user_id= %(user_id)s
        WHERE id = %(id)s;
        """
        results = connectToMySQL('recipe_db').query_db(query,data)
        return results
    
    @classmethod
    def delete_recipe(cls,data):
        query= """DELETE FROM recipes
            WHERE recipes.id = %(id)s;
        """
        return connectToMySQL('recipe_db').query_db(query,data)
        
    
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("name of the recipe must be at least 3 characters.")
            is_valid = False
        
        if len(data["description"]) == 0:
            flash('Descriptions is required','recipe')
            is_valid= False
        elif len(data['description']) < 3:
            flash('description must be at least 3 characters','recipe')
            is_valid= False
        
        if len(data["instructions"]) == 0:
            flash('Instructions is required','recipe')
            is_valid= False
        elif len(data['instructions']) < 3:
            flash('Instructions must be at least 3 characters','recipe')
            is_valid= False
        if not "under_30_minutes" in data:
            flash('Recipe length required','recipe')
            is_valid= False
        
        return is_valid
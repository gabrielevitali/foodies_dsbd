from app.routes.food import food_routes


def register_blueprints(app):

    # registro blueprint con l'applicazione Flask
    app.register_blueprint(food_routes, url_prefix='/food')
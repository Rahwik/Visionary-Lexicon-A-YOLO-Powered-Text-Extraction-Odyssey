from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Set up configuration
    app.config['UPLOAD_FOLDER'] = 'uploads'  # Define your upload folder here

    # Import routes and register them
    from routes import register_routes
    register_routes(app)  # Call the function to register routes

    return app

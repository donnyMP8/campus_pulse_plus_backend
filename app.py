from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from config import db
from config import config

# Initialize extensions
db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)
ma = Marshmallow()

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    limiter.init_app(app)
    ma.init_app(app)
    CORS(app)  # Enable CORS for all routes
    Talisman(app)  # Add security headers

    # Register blueprints
    from routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    #from routes.analytics_routes import analytics_bp
    # app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

    # from routes.category_routes import category_bp
    # app.register_blueprint(category_bp, url_prefix='/api/categories')

    # from routes.comment_routes import comment_bp
    # app.register_blueprint(comment_bp, url_prefix='/api/comments')

    from routes.post_routes import post_bp
    app.register_blueprint(post_bp, url_prefix='/api')

    from routes.reaction_routes import reaction_bp
    app.register_blueprint(reaction_bp, url_prefix='/api/reactions')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

# For development
if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True)
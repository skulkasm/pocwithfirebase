from flask import current_app, Flask, redirect, url_for


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        model = get_model()
        model.init_app(app)

    from docpoc.crud import crud
    app.register_blueprint(crud, url_prefix='/')

    # Add a default root route.
    @app.route("/")
    def index():
        return redirect(url_for('crud.logged_in'))

    return app

def get_model():
    model_backend = current_app.config['DATA_BACKEND']

    model = ''
    if model_backend == 'firestore':
        from docpoc import firestore
        model = firestore

    return model

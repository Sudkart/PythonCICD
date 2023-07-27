from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Welcome to Python CI CD!'

if __name__ == '__main__':
    # Use Gunicorn as the production server with 4 worker processes
    from gunicorn.app.base import BaseApplication

    class FlaskApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super(FlaskApplication, self).__init__()

        def load_config(self):
            for key, value in self.options.items():
                self.cfg.set(key, value)

        def load(self):
            return self.application

    options = {
        'bind': '0.0.0.0:8000',  # Bind to all network interfaces on port 8000
        'workers': 4,  # Number of Gunicorn worker processes
    }

    FlaskApplication(app, options).run()

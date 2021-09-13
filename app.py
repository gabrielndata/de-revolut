from flask import Flask
from flask_restful import Api

import auth
from api import resources
from settings import API_PREFIX


app = Flask(__name__)
api = Api(app, prefix=API_PREFIX)

# Register api resources
api.add_resource(resources.Nestify, '/nestify')

# Register auth verification handlers
auth.auth.verify_password(auth.verify_auth_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

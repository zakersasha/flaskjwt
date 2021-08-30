from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, set_access_cookies,
    set_refresh_cookies, jwt_required, get_jwt_identity, unset_jwt_cookies,
    get_jwt)

app = Flask(__name__)

# Для cookie
# app.config['JWT_TOKEN_LOCATION'] = ['cookies']
# app.config['JWT_COOKIE_SECURE'] = False
# app.config['JWT_ACCESS_PATH'] = '/api/'
# app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh'
# app.config['JWT_COOKIE_CSRF_PROTECT'] = True

app.config['JWT_SECRET_KEY'] = 'my_secret_key'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)


# Меняет токен за 30 мин до устаревания
# @app.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError):


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "admin" and password != "123":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity="example_user", fresh=True)  # fresh=datetime.timedelta(minutes=15)
    refresh_token = create_refresh_token(identity="example_user")
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

    # set_access_cookies(resp, access_token)
    # set_refresh_cookies(resp, refresh_token)


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user = get_jwt_identity()
    access_token = create_access_token(identity=user, fresh=False)
    return jsonify(access_token=access_token)


@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.route('/api/example', methods=['GET'])
@jwt_required(fresh=True)
def protected():
    user = get_jwt_identity()
    return jsonify({'Hello': user}), 200


if __name__ == '__main__':
    app.run()

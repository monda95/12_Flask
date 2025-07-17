from flask import request, render_template, redirect, url_for
from user_model import users, add_user, add_post_to_user, get_user_posts, like_user_post, delete_user

def register_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html", users=users)

    @app.route("/users", methods=["GET", "POST"])
    def users_route():
        if request.method == "GET":
            return render_template("create_user.html")
        elif request.method == "POST":
            username = request.form["username"]
            add_user({"username": username})
            return redirect(url_for("index"))

    @app.route("/users/post/<string:username>", methods=["GET", "POST"])
    def user_posts(username):
        if request.method == "POST":
            request_data = request.get_json()
            return add_post_to_user(username, request_data)
        else:
            return get_user_posts(username)

    @app.route("/users/post/like/<string:username>/<string:title>", methods=["PUT"])
    def like_post(username, title):
        return like_user_post(username, title)

    @app.route("/users/<string:username>", methods=["DELETE"])
    def delete(username):
        return delete_user(username)
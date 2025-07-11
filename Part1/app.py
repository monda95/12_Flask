from flask import Flask, request, Response
import test

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, This is Main Page"

@app.route('/about')
def about():
    return "This isthe about page!"

#동적으로 URL 파라미터 값을 받아서 처리해준다.
# http://127.0.0.1:5000/user
@app.route('/user/username')
def user_profile(username):
    return f"UserName : {username}"

@app.route('/number/<int:number>')
def user_number(number):
    return f"Number : {number}"

#post요청 날리는법
# (1) postman
# (2) requests
import requests
@app.route('/test')
def test():
    url = 'http://127.0.0.1:5000/submit'
    data = 'test data'
    requests.post(url=url,)

@app.route('/submit', methods=['GET', 'POST', 'PUT', 'DELETE' ])
def submit():
    print(request.method)

    if request.method == "GET":
        print("GET method")

    if request.method == "POST":
        print("***POST method***", request.data)

    
    return Response('Sucessfully submitted', status=200)

if __name__ == "__main__":
    app.run()

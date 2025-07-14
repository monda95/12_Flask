from flask import Flask
from flask_smorest import Api
from api import book_blp

app = Flask(__name__)

app.config["API_TITLE"] = "Book API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(book_blp)

if __name__ == "__main__":
    app.run(debug=True)

# #####################################################################################
# 코드 상세 해설 및 작동 원리
# #####################################################################################
#
# 이 애플리케이션은 Flask와 Flask-Smorest를 사용하여 간단한 책(Book) 정보를 관리하는 REST API를 구축한 예제입니다.
# 총 3개의 파일(app.py, api.py, schemas.py)로 구성되어 있으며, 각 파일의 역할은 다음과 같습니다.
#
# ---
#
# ### 1. schemas.py: 데이터 유효성 검사 및 직렬화/역직렬화 정의
#
# `schemas.py` 파일은 Marshmallow 라이브러리를 사용하여 API가 주고받을 데이터의 형식을 정의합니다.
#
# - **`BookSchema` 클래스**:
#   - `Schema`를 상속받아 책 데이터의 구조를 정의합니다.
#   - **`id = fields.Int(dump_only=True)`**:
#     - `id` 필드는 정수(Integer) 타입입니다.
#     - `dump_only=True`는 이 필드가 '직렬화(dumping)' 과정, 즉 파이썬 객체에서 JSON으로 변환될 때만 사용된다는 의미입니다.
#     - 클라이언트가 서버로 데이터를 보낼 때(역직렬화, loading)는 `id` 값을 포함하지 않아도 되며, 포함하더라도 무시됩니다. 이는 `id`가 서버에서 자동으로 생성 및 관리되는 값임을 나타냅니다.
#   - **`title = fields.String(required=True)`**:
#     - `title` 필드는 문자열(String) 타입입니다.
#     - `required=True`는 클라이언트가 책을 생성하거나 수정할 때 반드시 이 필드를 포함해야 함을 의미합니다. 값이 없으면 유효성 검사에서 오류가 발생합니다.
#   - **`author = fields.String(required=True)`**:
#     - `author` 필드 역시 `title`과 마찬가지로 필수 문자열 필드입니다.
#
# ---
#
# ### 2. api.py: API 엔드포인트 및 비즈니스 로직 구현
#
# `api.py` 파일은 실질적인 API 로직을 담고 있습니다. `Blueprint`를 사용하여 관련 API들을 그룹화하고, `MethodView`를 통해 각 엔드포인트의 HTTP 메소드(GET, POST, PUT, DELETE)를 처리합니다.
#
# - **`book_blp = Blueprint(...)`**:
#   - `flask-smorest`의 `Blueprint`를 생성합니다. 이를 통해 API의 엔드포인트들을 모듈화하여 관리할 수 있습니다.
#   - `url_prefix="/books"`: 이 블루프린트에 속한 모든 API의 기본 URL 경로를 `/books`로 지정합니다.
#
# - **`books = []`**:
#   - 데이터베이스 대신, 책 데이터를 저장하기 위한 간단한 인메모리(in-memory) 리스트입니다. 애플리케이션이 재시작되면 데이터는 사라집니다.
#
# - **`@book_blp.route("/")` / `BookList(MethodView)`**:
#   - `/books` 경로에 대한 요청을 처리하는 클래스입니다.
#   - **`get(self)`**:
#     - `GET /books` 요청을 처리합니다.
#     - 저장된 모든 책의 목록(`books` 리스트)을 반환합니다.
#     - `@book_blp.response(200)`: 성공 시 HTTP 상태 코드 200(OK)을 반환함을 명시합니다.
#   - **`post(self, new_data)`**:
#     - `POST /books` 요청을 처리합니다.
#     - `@book_blp.arguments(BookSchema)`: 요청 본문(body)의 데이터가 `BookSchema`에 정의된 형식과 일치하는지 자동으로 유효성 검사를 수행합니다. 검사를 통과한 데이터가 `new_data` 매개변수로 전달됩니다.
#     - `new_data['id'] = len(books) + 1`: 새 책에 대한 `id`를 생성합니다.
#     - `books.append(new_data)`: 유효한 새 책 데이터를 `books` 리스트에 추가합니다.
#     - `@book_blp.response(201, BookSchema)`: 성공 시 HTTP 상태 코드 201(Created)과 함께 생성된 책의 정보를 `BookSchema` 형식으로 반환함을 명시합니다.
#
# - **`@book_blp.route("/<int:book_id>")` / `Book(MethodView)`**:
#   - `/books/<book_id>` 형태의 경로에 대한 요청을 처리하는 클래스입니다. `<int:book_id>`는 URL 경로에서 정수 형태의 `book_id`를 추출하여 메소드의 인자로 전달합니다.
#   - **`get(self, book_id)`**:
#     - `GET /books/<book_id>` 요청을 처리합니다.
#     - `next(...)`를 사용하여 `books` 리스트에서 해당 `book_id`를 가진 책을 찾습니다.
#     - 책이 없으면 `abort(404, ...)`를 통해 HTTP 404(Not Found) 오류를 반환합니다.
#     - `@book_blp.response(200, BookSchema)`: 성공 시 찾은 책의 정보를 `BookSchema` 형식으로 반환합니다.
#   - **`put(self, new_data, book_id)`**:
#     - `PUT /books/<book_id>` 요청을 처리합니다.
#     - `@book_blp.arguments(BookSchema)`: `POST`와 마찬가지로 요청 본문의 데이터 유효성을 검사합니다.
#     - 해당 `book_id`의 책을 찾아 `new_data`로 내용을 업데이트합니다.
#     - 책이 없으면 404 오류를 반환합니다.
#     - `@book_blp.response(200, BookSchema)`: 성공 시 업데이트된 책의 정보를 반환합니다.
#   - **`delete(self, book_id)`**:
#     - `DELETE /books/<book_id>` 요청을 처리합니다.
#     - 해당 `book_id`의 책을 찾아 `books` 리스트에서 제거합니다.
#     - 책이 없으면 404 오류를 반환합니다.
#     - `@book_blp.response(204)`: 성공 시 내용 없이(No Content) HTTP 204 상태 코드를 반환함을 명시합니다.
#
# ---
#
# ### 3. app.py: Flask 애플리케이션 설정 및 실행
#
# `app.py`는 Flask 애플리케이션의 진입점(entry point) 역할을 합니다. 앱을 생성하고, 필요한 설정을 적용하며, `api.py`에서 정의한 블루프린트를 등록합니다.
#
# - **`app = Flask(__name__)`**:
#   - Flask 애플리케이션 인스턴스를 생성합니다.
#
# - **`app.config[...]`**:
#   - API 문서 자동 생성을 위한 OpenAPI(Swagger) 관련 설정을 구성합니다.
#   - `API_TITLE`, `API_VERSION`: API 문서에 표시될 제목과 버전입니다.
#   - `OPENAPI_SWAGGER_UI_PATH`: Swagger UI가 제공될 URL 경로입니다. (예: `http://localhost:5000/swagger-ui`)
#
# - **`api = Api(app)`**:
#   - Flask 앱을 `flask-smorest`의 `Api` 객체와 연결합니다. 이를 통해 OpenAPI 기능이 활성화됩니다.
#
# - **`api.register_blueprint(book_blp)`**:
#   - `api.py`에서 생성한 `book_blp` 블루프린트를 애플리케이션에 등록합니다. 이 과정을 통해 `book_blp`에 정의된 모든 라우트(엔드포인트)가 앱에서 활성화됩니다.
#
# - **`if __name__ == "__main__":`**:
#   - 이 스크립트가 직접 실행될 때만 `app.run(debug=True)`를 호출하여 개발 서버를 실행합니다.
#   - `debug=True`는 개발 중에 코드가 변경될 때마다 서버가 자동으로 재시작되고, 오류 발생 시 디버깅 정보를 제공하는 등의 편의 기능을 활성화합니다.

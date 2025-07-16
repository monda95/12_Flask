from flask import request, jsonify, render_template               # Flask에서 요청 객체와 JSON 응답 생성을 위해 import
from flask_smorest import Blueprint, abort         # Flask-smorest에서 Blueprint와 HTTP 오류 처리를 위해 import


def create_posts_blueprint(mysql):                 # 게시글 관련 API를 위한 Blueprint를 생성하는 함수
    posts_blp = Blueprint(                         # Blueprint 객체 생성
        "posts",                                   # Blueprint의 이름
        __name__,                                  # 현재 모듈의 이름
        description="posts api",                   # API에 대한 설명
        url_prefix="/posts",                       # 이 Blueprint에 속한 모든 라우트의 URL 접두사
    )

    @posts_blp.route("/", methods=["GET", "POST"]) # "/posts/" 경로에 대한 라우트 설정, GET과 POST 요청 처리
    def posts():                                   # 게시글 목록 조회 및 생성 핸들러 함수
        cursor = mysql.connection.cursor()         # 데이터베이스와 상호작용하기 위한 커서 객체 생성

        # 게시글 조회
        if request.method == "GET":                # 요청 메소드가 GET일 경우
            sql = "SELECT * FROM posts"            # 모든 게시글을 선택하는 SQL 쿼리
            cursor.execute(sql)                    # SQL 쿼리 실행

            posts = cursor.fetchall()              # 쿼리 결과를 모두 가져옴
            cursor.close()                         # 커서 객체 닫기

            post_list = []                         # 게시글 목록을 담을 리스트 초기화

            for post in posts:                     # 각 게시글에 대해 반복
                post_list.append(                  # 리스트에 게시글 정보를 딕셔너리 형태로 추가
                    {
                        "id": post[0],             # 게시글 ID
                        "title": post[1],          # 게시글 제목
                        "content": post[2],        # 게시글 내용
                    }
                )
            return jsonify(post_list)              # 게시글 목록을 JSON 형태로 변환하여 반환

        # 게시글 생성
        elif request.method == "POST":             # 요청 메소드가 POST일 경우
            title = request.json.get("title")      # 요청 본문(JSON)에서 'title' 값을 가져옴
            content = request.json.get("content")  # 요청 본문(JSON)에서 'content' 값을 가져옴

            if not title or not content:           # 'title' 또는 'content'가 없는 경우
                abort(400, message="title 또는 content가 없습니다.") # 400 Bad Request 오류 발생

            sql = "INSERT INTO posts(title, content) VALUES(%s, %s)" # 새 게시글을 추가하는 SQL 쿼리
            cursor.execute(sql, (title, content))  # SQL 쿼리 실행 (값은 튜플 형태로 전달하여 SQL Injection 방지)
            mysql.connection.commit()              # 변경사항을 데이터베이스에 최종 반영

            return jsonify({"message": "success"}), 201 # 성공 메시지와 함께 201 Created 상태 코드 반환

    # 게시글 상세 조회
    # 게시글 수정 및 삭제
    @posts_blp.route("/<int:id>", methods=["GET", "PUT", "DELETE"]) # "/posts/<id>" 경로에 대한 라우트, id는 정수형
    def post(id):                                  # 특정 게시글 처리 핸들러 함수
        cursor = mysql.connection.cursor()         # 데이터베이스 커서 생성

        if request.method == "GET":                # 요청 메소드가 GET일 경우 (상세 조회)
            sql = f"SELECT * FROM posts WHERE id={id}" # 특정 ID의 게시글을 선택하는 SQL 쿼리 (f-string 사용)
            cursor.execute(sql)                    # 쿼리 실행
            post = cursor.fetchone()               # 쿼리 결과 하나를 가져옴

            if not post:                           # 해당 게시글이 없으면
                abort(404, message="해당 게시글이 없습니다.") # 404 Not Found 오류 발생
            return {                               # 게시글 정보를 딕셔너리 형태로 반환 (자동으로 JSON으로 변환됨)
                "id": post[0],
                "title": post[1],
                "content": post[2],
            }

        elif request.method == "PUT":              # 요청 메소드가 PUT일 경우 (수정)
            title = request.json.get("title")      # 요청 본문에서 'title' 값을 가져옴
            content = request.json.get("content")  # 요청 본문에서 'content' 값을 가져옴

            if not title or not content:           # 'title' 또는 'content'가 없으면
                abort(400, message="title 또는 content가 없습니다.") # 400 Bad Request 오류 발생

            sql = "SELECT * FROM posts WHERE id=%s" # 수정할 게시글이 존재하는지 확인하는 쿼리
            cursor.execute(sql, (id,))             # 쿼리 실행
            post = cursor.fetchone()               # 결과 가져오기

            if not post:                           # 게시글이 없으면
                abort(404, message="해당 게시글이 없습니다.") # 404 Not Found 오류 발생

            sql = "UPDATE posts SET title=%s, content=%s WHERE id=%s" # 게시글을 수정하는 SQL 쿼리
            cursor.execute(sql, (title, content, id)) # 쿼리 실행
            mysql.connection.commit()              # 변경사항을 데이터베이스에 최종 반영

            return jsonify({"message": "Successfully updated title & content"}) # 성공 메시지 반환

        elif request.method == "DELETE":           # 요청 메소드가 DELETE일 경우 (삭제)
            sql = "SELECT * FROM posts WHERE id=%s" # 삭제할 게시글이 존재하는지 확인하는 쿼리
            cursor.execute(sql, (id,))             # 쿼리 실행
            post = cursor.fetchone()               # 결과 가져오기

            if not post:                           # 게시글이 없으면
                abort(404, message="해당 게시글이 없습니다.") # 404 Not Found 오류 발생

            sql = "DELETE FROM posts WHERE id=%s"  # 게시글을 삭제하는 SQL 쿼리
            cursor.execute(sql, (id,))             # 쿼리 실행
            mysql.connection.commit()              # 변경사항을 데이터베이스에 최종 반영

            return jsonify({"message": "Successfully deleted post"}) # 성공 메시지 반환

    return posts_blp                               # 설정이 완료된 Blueprint 객체 반환
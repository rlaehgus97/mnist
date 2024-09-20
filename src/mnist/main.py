from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import os
import pymysql.cursors
import json
from mnist.db import get_conn

app = FastAPI()


@app.post("/files/")
async def file_list():
    conn = get_conn()
    with conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    return result


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # 파일 저장
    img = await file.read()
    file_name = file.filename
    file_ext = file.content_type.split('/')[-1]  #'png'만 받기

    # 디렉토리가 없으면 오류, 코드에서 확인 및 만들기 추가
    upload_dir = "/home/dohyun/codes/mnist/img"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    import uuid

    file_full_path = os.path.join(upload_dir, f'{uuid.uuid4()}.{file_ext}')
    
    with open(file_full_path, "wb") as f:
        f.write(img)
    
    # 파일 저장 경로 DB INSERT
    # tablename : image_processing
    # 컬럼 정보 : num (초기 인서트, 자동증가)
    # 처음 컬럼 정보 : 파일이름, 파일경로, 요청시간 (초기 인서트), 요청사용자(n00)
    # 컬럼 정보 : 예측모델, 예측결과, 예측시간 (추후 업데이트)
    sql = "INSERT INTO image_processing(file_name, file_path, request_time, request_user) VALUES(%s, %s, %s, %s)"

    from datetime import datetime, timedelta
    from pytz import timezone
    import pytz

    seoul_tz = pytz.timezone('Asia/Seoul')
    jiguem = datetime.now(seoul_tz).strftime('%Y-%m-%d %H:%M:%S')

    import jigeum.seoul
    from mnist.db import dml

    insert_row = dml(sql, file_name, file_full_path, jigeum.seoul.now(), 'n99')

    return {
            "filename": file.filename,
            "content_type":file.content_type,
            "file_full_path": file_full_path,
            "insert_row_count": insert_row
            }

@app.get("/all")
def all():
    # DB 연결 SELECT ALL
    from mnist.db import select

    sql = "SELECT * FROM image_processing"

    # 결과값 리턴 
    result = select(query=sql, size=-1)
    return result

@app.get("/one")
def one():
    # DB 연결 SELECT 값 중 하나만 리턴
    from mnist.db import select

    sql = """
            SELECT * FROM image_processing 
            WHERE prediction_time IS NULL ORDER BY num LIMIT 1
            """
    result = select(query=sql, size=1)
    # 결과값 리턴
    return result[0]

@app.get("/many/")
def many(size: int = -1):
    from minist.db import get_conn

    sql = "SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num"
    conn = get_conn()

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchmany(size)

    return result

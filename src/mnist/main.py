from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import datetime
import os
import pymysql.cursors
import json
from mnist.utils.db import get_db_connection
from mnist.utils.util import get_now_time

app = FastAPI()

username = "n09"

@app.get("/")
def hello():
    return {"msg": "hello"}

def save_db(file, file_name, path, current_time):
    
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO
                image_processing (
                                    file_name,
                                    file_path,
                                    request_time,
                                    request_user
                                ) VALUES (%s, %s, %s, %s)
                """
            file_path = os.path.join(os.path.dirname(path), file_name)
            cursor.execute(
                    sql,
                    (
                        file.filename, #원본 파일명
                        file_path, #저장전체 경로 및 uuid 변환 파일명
                        current_time, #요청 시간
                        username,
                    ),
                )
        connection.commit()
    except Exception as e:
        print(e)
        return {"error": str(e)}
    finally:
        connection.close()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # 파일 저장
    img = await file.read()
    file_name = file.filename
    file_ext = file.content_type.split('/')[-1]  #'png'만 받기

    # 디렉토리가 없으면 오류, 코드에서 확인 및 만들기 추가
    upload_dir = os.getenv('UPLOAD_DIR', "/home/dohyun/codes/mnist/img")

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    import uuid

    formatted_name = f'{uuid.uuid4()}.{file_ext}'
    file_full_path = os.path.join(upload_dir, formatted_name)
    
    # 시간
    current_time = get_now_time()    

    with open(file_full_path, "wb") as f:
        f.write(img)
    
    # 파일 저장 경로 DB INSERT
    # tablename : image_processing
    # 컬럼 정보 : num (초기 인서트, 자동증가)
    # 처음 컬럼 정보 : 파일이름, 파일경로, 요청시간 (초기 인서트), 요청사용자(n00)
    # 컬럼 정보 : 예측모델, 예측결과, 예측시간 (추후 업데이트)

    # 데이터베이스에도 파일에대한 정보 저장
    save_db(file, formatted_name, file_full_path, current_time)
    
    return {
            "filename": file.filename,
            "content_type":file.content_type,
            "file_full_path": file_full_path,
            "time": current_time,
            }

@app.get("/files/")
async def get_files(size: int = 10):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT *
                FROM image_processing
                ORDER BY request_time DESC
                LIMIT %s
                """
            cursor.execute(sql, size)
            rows = cursor.fetchall()

            # 필드 이름을 키로 매핑하여 데이터를 변환
            result = [
                {
                    "id": row[0],
                    "file_name": row[1],
                    "file_path": row[2],
                    "request_time": row[3],
                    "request_user": row[4],
                    "prediction_model": row[5],
                    "prediction_result": row[6],
                    "prediction_time": row[7],
                }
                for row in rows
            ]
        return {"files": result}
    except Exception as e:
        print(e)
        return {"error": str(e)}
    finally:
        if connection and connection.open:
            connection.close()

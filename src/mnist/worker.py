from jigutime import jigu
from mnist.db import select, dml
import random
import os
import requests

import numpy as np
from PIL import Image
from keras.models import load_model

#모델 로드
model = load_model('mnist240924.keras')

def get_job_img_task():
   sql = """
   SELECT 
    num, file_name, file_path
   FROM image_processing
   WHERE prediction_result IS NULL
   ORDER BY num -- 가장 오래된 요청
   LIMIT 1 -- 하나씩
   """
   r = select(sql, 1)

   if len(r) > 0:
       return r[0]
   else:
       return None

# 사용자 이미지 불러오기 및 전처리
def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')
    img = img.resize((28,28)) #크기 조정

    # 흑백반전
    img = 255 - np.array(img)
    img = np.array(img)
    img = img.reshape(1,28,28,1) #모델 입력 형태 맞게 변형
    img = img/255.0 #정규화

    return img

def prediction(file_path, num):
    sql = """UPDATE image_processing
    SET prediction_result=%s,
        prediction_model='n77',
        prediction_time=%s
    WHERE num=%s
    """
    img = preprocess_image(file_path)
    prediction = model.predict(img)
    presult = np.argmax(prediction)
    dml(sql, presult, jigu.now(), num)

    return presult


def run():
  """image_processing 테이블을 읽어서 가장 오래된 요청 하나씩을 처리"""
  
  # STEP 1
  # image_processing 테이블의 prediction_result IS NULL 인 ROW 1 개 조회 - num 갖여오기
  job = get_job_img_task()
    
  if job is None:
      print(f"{jigu.now()} - jos is None")
      return 

  num = job['num']
  file_name = job['file_name']
  file_path = job['file_path']

  # STEP 2
  # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
  # 동시에 prediction_model, prediction_time 도 업데이트
  presutl = prediction(file_path, num) 

  # STEP 3
  # LINE 으로 처리 결과 전송
  send_line_noti(file_name, presutl)

  print(jigu.now())

def send_line_noti(file_name, presutl):
    #KEY = os.environ.get('API_TOKEN')
    api = "https://notify-api.line.me/api/notify"
    token = os.getenv('LINE_NOTI_TOKEN', 'NULL')
    h = {'Authorization':'Bearer ' + token}
    msg = {
       "message" : f"{file_name} => {presutl} 성공적으로 저장했습니다!"
    }
    response = requests.post(api, headers=h , data=msg)
    print(response.text)
    print("SEND LINE NOTI")





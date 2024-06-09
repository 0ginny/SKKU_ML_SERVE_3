# -*- coding: utf-8 -*-
"""IP.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ivo_3umb2dggIvYcfwaCfCqs3Q6AF9b6
"""

# !pip freeze >> requirments.txt

# !pip install fastapi uvicorn
# !pip install  nest-asyncio pyngrok

# from google.colab import drive
# drive.mount("/content/gdrive")
# %cd /content/gdrive/MyDrive/Colab Notebooks/skku_python_repo-main/08. 유형별로 실습하는 딥러닝

"""# 모델 불러오기"""

import pickle
import pandas as pd

# 서버 관리용 fastapi 의존 라이브러리
import uvicorn

# fast api 라이브러리
from fastapi import FastAPI

# 인터페이스 데이터 관리를 위한 라이브러리
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
origins = ["*"]

app = FastAPI(title="ML API")

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

with open("dlmodel_240608.pickle","rb") as fr:
    loadedRef = pickle.load(fr)

# 모델과 스케일러 정의
model = loadedRef['model']
scaler = loadedRef['scaler']

class InDataset(BaseModel):
    inResinTemp : int
    inMoldTemp : int
    inTime : float

@app.post("/predict", status_code=200)
async def predictDl(x:InDataset):
    print(x)
    # 화면입력데이터 변수 할당
    inResinTemp = x.inResinTemp
    inMoldTemp = x.inMoldTemp
    inTime =x.inTime
    print("step1")
    # 예측을 위한 데이터셋 생성
    InjectionData = pd.DataFrame([[inResinTemp, inMoldTemp, inTime]])
    # 예측
    # print(InjectionData)
    predictValue = model.predict(scaler.transform(InjectionData))
    # print("prediction : ", predictValue)
    result = {"prediction":predictValue,
              "resintempgraph" : []}
    return result

@app.get("/")
async def root():
    return {"message":"onine"}

import uvicorn
if __name__ == "__main__":
  # IP:Injection Pressure (해석 사출압)
  uvicorn.run("ip:app", host="0.0.0.0", port=9999, log_level="debug",
    proxy_headers=True, reload=True)


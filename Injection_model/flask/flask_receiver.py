from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# 모델 로드
with open("dlmodel_240608.pickle", "rb") as fr:
    loadedRef = pickle.load(fr)

# 모델과 스케일러 정의
model = loadedRef['model']
scaler = loadedRef['scaler']


def resin_graph_data(inResinTemp, inMoldTemp, inTime):
    # 설정할 범위 및 개수
    changeRanges = [10, 5, 0.5]
    num_values = 5

    # 각 parameter에 대한 값 생성 함수
    def generate_values(param, change_range):
        min_val = param - change_range
        max_val = param + change_range
        return np.linspace(min_val, max_val, num_values).reshape(-1, 1)

    # inResinTemp만 변경하여 데이터프레임 생성 및 예측
    resin_temps = generate_values(inResinTemp, changeRanges[0])
    InjectionData1 = pd.DataFrame(
        np.hstack([resin_temps, np.full((num_values, 1), inMoldTemp), np.full((num_values, 1), inTime)]),
        columns=['RESIN_TEMPERATURE', 'MOLD_TEMPERATURE', 'INJECTION_TIME'])
    predictions1 = model.predict(scaler.transform(np.array(InjectionData1)))

    # inMoldTemp만 변경하여 데이터프레임 생성 및 예측
    mold_temps = generate_values(inMoldTemp, changeRanges[1])
    InjectionData2 = pd.DataFrame(
        np.hstack([np.full((num_values, 1), inResinTemp), mold_temps, np.full((num_values, 1), inTime)]),
        columns=['RESIN_TEMPERATURE', 'MOLD_TEMPERATURE', 'INJECTION_TIME'])
    predictions2 = model.predict(scaler.transform(np.array(InjectionData2)))

    # inTime만 변경하여 데이터프레임 생성 및 예측
    times = generate_values(inTime, changeRanges[2])
    InjectionData3 = pd.DataFrame(
        np.hstack([np.full((num_values, 1), inResinTemp), np.full((num_values, 1), inMoldTemp), times]),
        columns=['RESIN_TEMPERATURE', 'MOLD_TEMPERATURE', 'INJECTION_TIME'])
    predictions3 = model.predict(scaler.transform(np.array(InjectionData3)))

    labels = [resin_temps.flatten().tolist(), mold_temps.flatten().tolist(), times.flatten().tolist()]
    predictions = [predictions1.flatten().tolist(), predictions2.flatten().tolist(), predictions3.flatten().tolist()]

    return labels, predictions


@app.route("/predict", methods=["POST"])
def predictDl():
    try:
        data = request.json
        inResinTemp = data['inResinTemp']
        inMoldTemp = data['inMoldTemp']
        inTime = data['inTime']

        # 예측을 위한 데이터셋 생성
        InjectionData = pd.DataFrame([[inResinTemp, inMoldTemp, inTime]])
        # 예측
        predictValue = model.predict(scaler.transform(InjectionData))[0][0]

        labels, predictions = resin_graph_data(inResinTemp, inMoldTemp, inTime)

        result = {
            'Rtemp_labels': labels[0],
            'Mtemp_labels': labels[1],
            'Time_labels': labels[2],
            'Rtemp_predictions': predictions[0],
            'Mtemp_predictions': predictions[1],
            'Time_predictions': predictions[2],
            'prediction': round(float(predictValue), 2)
        }
    except Exception as e:
        print(f"Error: {e}")
        result = {"prediction": 0}

    return jsonify(result)


@app.route("/")
def root():
    return jsonify({"message": "online"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999, debug=True)

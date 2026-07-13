from fastapi import FastAPI,Path
import json
app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)

    return data

@app.get("/")
def hello():
    return {'message':'hello world !'}


@app.get("/about")
def about():
    return {'message':'your in about page !'}


@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/view/{patient_id}")
def fetchpatient(patient_id:str=Path(...,description='id of patient in DB',example='P001')):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    return {'error':'patient not found '}


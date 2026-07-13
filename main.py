from fastapi import FastAPI,Path,HTTPException,Query
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
    raise HTTPException(status_code=404,detail='patient id not found in DB')

@app.get('/sort')
def sort_patients(sort_by:str=Query(...,detail='sort on basis of key'),order_by:str=Query('asc',detail='sort in either ascending or descending')):
    data=load_data()
    valid_fields=['height','age','bmi']
    valid_sort=['asc','desc']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail='choose valid field')
    if order_by not in valid_sort:
        raise HTTPException(status_code=400,detail='choose valid order by option either asc or desc')
    if order_by =='desc':
        order_by=False
    else:
        order_by=True


    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=order_by)
    return sorted_data






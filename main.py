from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field,model_validator
from typing import Annotated,Literal,Optional
app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='id of patient',examples=['P001'])]
    name:Annotated[str,Field(...,description='name of patient',examples=['moosa'])]
    city:Annotated[str,Field(...,description='city of patient',examples=['faislabad'])]
    age:Annotated[int,Field(...,description='age of patient',examples=['30'],gt=0)]
    gender:Annotated[Literal['male','female','other'],Field(...,description='gender of patient')]
    height:Annotated[float,Field(...,gt=0.0,description='height of patient in ms')]
    weight:Annotated[float,Field(...,gt=0,description='weight of patient in kgs')]
 

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi

    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
        

class patientupdate(BaseModel):
  
    name:Annotated[Optional[str],Field(default=None,description='name of patient',examples=['moosa'])]
    city:Annotated[Optional[str],Field(default=None,description='city of patient',examples=['faislabad'])]
    age:Annotated[Optional[int],Field(default=None,description='age of patient',examples=['30'],gt=0)]
    gender:Annotated[Optional[Literal['male','female','other']],Field(default=None,description='gender of patient')]
    height:Annotated[Optional[float],Field(default=None,gt=0.0,description='height of patient in ms')]
    weight:Annotated[Optional[float],Field(default=None,gt=0,description='weight of patient in kgs')]
 



def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)

    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

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
        order_by=True
    else:
        order_by=False


    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=order_by)
    return sorted_data

@app.post('/create')
def create_patient(patient:Patient):
    #load data from json
    data=load_data()
    # find if id already exsists
    if patient.id in data:
        raise HTTPException(status_code=400,detail='bad request already exsists')
    #serialize
    data[patient.id]=patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'patient added'})





from fastapi import FastAPI, File, UploadFile
import uvicorn
import pickle
import pandas as pd

tags = [
    {
        'name': 'Maths',
        'description': 'operations related to mathematical operations'
    },
    {
        'name': 'Models',
        'description': 'operations related to Models'
    }
]

app = FastAPI(
    title="FastApi api" ,
    description="simple app" ,
    version="0.0.1",
    openapi_tags=tags
)

@app.get("/", tags=["Models"])
def default_root():
    return "hello world"


@app.get("/square", tags=["Maths"])
def square(n: float) -> str:
    return str(n * n)

from pydantic import BaseModel
class Data(BaseModel):
    name:str="defaultValueName"
    city:str="defaultValueCity"

@app.post("/formulaire")
def formulaire(data:Data):
    data = dict(data)
    
    name = data['name']
    city = data['city']
    
    return f"Hello {name} from {city}"


@app.post('/upload')
def upload_file(file:UploadFile=File(...)):
    return file.filename


with open("model.pkl", "rb") as f:
    model = pickle.load(f)
    
class User(BaseModel):
    Gender:str = 'Male',
    Age:int = 22,
    Graduated:str = 'No',
    Profession:str = 'Healthcare',
    Work_Experience:int = 1.0,
    Spending_Score:str = 'Low',
    Family_Size:int = 4.0,
    Segmentation:str = 'D'

@app.post('/predict', tags=['Models'])
def predict(data:User):
    user = pd.DataFrame([dict(data)])
    y_pred = model.predict(user)[0]
    return int(y_pred)

@app.post('/predict_file')
def predict_file(file:UploadFile=File(...)):
    
    df = pd.read_csv(file.file)
    if 'Gender' not in df.columns or 'Graduated' not in df.columns:
        return False
    else :
        X = df.drop(["Ever_Married"], axis=1).dropna()
        y_pred = model.predict(X)
        print (y_pred)
        return [int(n) for n in model.predict(X)]



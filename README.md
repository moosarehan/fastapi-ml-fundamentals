<div align="center">

# ⚡ FastAPI — Patient Management API

> A fully functional REST API built with FastAPI for managing patient records — covering CRUD operations, path & query parameters, data validation, and auto-generated docs.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-V2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-499848?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Learning-F5A623?style=for-the-badge)

</div>

---

## 📚 Table of Contents

| # | Topic |
|---|-------|
| 1 | [What is FastAPI?](#-what-is-fastapi) |
| 2 | [Why FastAPI is Fast to RUN](#-why-fastapi-is-fast-to-run--asgi--uvicorn) |
| 3 | [Why FastAPI is Fast to CODE](#-why-fastapi-is-fast-to-code) |
| 4 | [Built on Two Pillars](#-built-on-two-pillars) |
| 5 | [Project Structure](#-project-structure) |
| 6 | [Data Models](#-data-models) |
| 7 | [API Endpoints](#-api-endpoints) |
| 8 | [Path Parameters](#-path-parameters) |
| 9 | [Query Parameters](#-query-parameters) |
| 10 | [GET — Read Data](#-get--read-data) |
| 11 | [POST — Create Data](#-post--create-data) |
| 12 | [PUT — Update Data](#-put--update-data) |
| 13 | [DELETE — Remove Data](#-delete--remove-data) |
| 14 | [Run the Project](#-run-the-project) |

---

## 🤔 What is FastAPI?

FastAPI is a **modern Python web framework** for building REST APIs — fast to run and fast to code.

```
Client (Browser / App)
         │
         │  HTTP Request
         ▼
    ┌─────────────┐
    │   Uvicorn   │  ← web server, listens on port
    │   (ASGI)    │  ← translates HTTP to Python
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │   FastAPI   │  ← your route logic runs here
    │   (Your     │  ← validates data via Pydantic
    │    Code)    │  ← returns JSON response
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │   Uvicorn   │  ← translates Python back to HTTP
    └──────┬──────┘
           │
           │  JSON Response
           ▼
Client receives and displays data
```

---

## 🚀 Why FastAPI is Fast to RUN — ASGI + Uvicorn

FastAPI runs on **Uvicorn**, an ASGI server. ASGI stands for **Asynchronous Server Gateway Interface** — it allows handling **multiple requests concurrently** without blocking.

```
OLD WAY — WSGI (Synchronous)
─────────────────────────────
Request 1 → handle → done
Request 2 → handle → done    ← waits for Request 1 to finish
Request 3 → handle → done    ← waits for Request 2 to finish

One at a time. Slow DB query? Everyone is BLOCKED.


NEW WAY — ASGI (Asynchronous)
──────────────────────────────
Request 1 → starts → waiting for DB...
Request 2 → starts → waiting for DB...  ← doesn't wait for Req 1
Request 3 → starts → waiting for DB...  ← doesn't wait for Req 2

DB replies to Req 1 → respond ✅
DB replies to Req 3 → respond ✅
DB replies to Req 2 → respond ✅

All handled concurrently. Nobody blocks anyone.
```

```
┌──────────────┬──────────────────────────────────────────┐
│              │  Role                                    │
├──────────────┼──────────────────────────────────────────┤
│ ASGI         │ specification/contract (not software)    │
│              │ defines HOW server and app communicate   │
├──────────────┼──────────────────────────────────────────┤
│ Uvicorn      │ ASGI server — listens on port, handles  │
│              │ concurrency, translates HTTP ↔ Python    │
├──────────────┼──────────────────────────────────────────┤
│ FastAPI      │ ASGI app — your routes and logic        │
│              │ never touches raw HTTP directly          │
└──────────────┴──────────────────────────────────────────┘

Both Uvicorn and FastAPI implement the ASGI spec
so they can communicate with each other ✅
```

---

## ⚡ Why FastAPI is Fast to CODE

### 1️⃣ Auto Generated Docs — Zero Extra Work

Just run your app and visit `/docs` — Swagger UI is automatically generated from your code. No configuration, no extra libraries, no manual writing.

```
@app.get("/view/{patient_id}")
def fetchpatient(patient_id: str = Path(..., description='id of patient')):
    ...

↓  FastAPI reads this and auto generates ↓

/docs shows:
┌─────────────────────────────────────────┐
│  GET /view/{patient_id}                 │
│  ─────────────────────────────────────  │
│  Parameters:                            │
│  • patient_id (path) — id of patient   │
│    Example: P001                        │
│                                         │
│  [ Try it out ] ← interactive button   │
└─────────────────────────────────────────┘
```

### 2️⃣ Automatic Input Validation via Pydantic

No manual type checking or if/else validation — declare your model once and FastAPI validates every incoming request automatically.

```python
# Without FastAPI — you write this manually
if "age" not in data:
    return {"error": "age required"}
if not isinstance(data["age"], int):
    return {"error": "age must be int"}
if data["age"] <= 0:
    return {"error": "age must be positive"}

# With FastAPI + Pydantic — done in one line
age: Annotated[int, Field(..., gt=0)]
```

```
Client sends wrong data
         │
         ▼
┌─────────────────────────────┐
│  Pydantic validates         │
│  automatically              │
└──────────────┬──────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
   PASS ✅        FAIL ❌
   route runs     422 Unprocessable
                  Entity — auto error
                  response sent back
                  your code never runs
```

> 📎 For a deep dive into Pydantic — check out my complete Pydantic notes:
> **[🔗 pydantic-fundamentals](https://github.com/moosarehan/pydantic-fundamentals)**

---

## 🏛️ Built on Two Pillars

FastAPI is not built from scratch — it stands on the shoulders of two powerful frameworks:

```
┌─────────────────────────────────────────────────────┐
│                     FastAPI                         │
└────────────────┬────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌───────────────┐  ┌───────────────────────────────┐
│  Starlette    │  │  Pydantic                     │
│               │  │                               │
│ web toolkit   │  │ data validation library       │
│ handles:      │  │ handles:                      │
│ • routing     │  │ • type checking               │
│ • middleware  │  │ • input validation            │
│ • requests    │  │ • serialization               │
│ • responses   │  │ • auto docs schema            │
│ • websockets  │  │ • computed fields             │
│ • ASGI layer  │  │ • nested models               │
└───────────────┘  └───────────────────────────────┘

Starlette  =  the engine   (HOW requests are handled)
Pydantic   =  the gatekeeper (WHAT data is accepted)
```

---

## 📁 Project Structure

```
fastapi-ml-fundamentals/
│
├── main.py            ← all routes and logic
├── patients.json      ← data storage (acts as DB)
├── requirements.txt   ← project dependencies
└── .gitignore         ← ignores venv, pycache
```

---

## 🧬 Data Models

### Patient (Create)
All fields required. BMI and verdict are auto-computed — client never sends them.

```python
class Patient(BaseModel):
    id:     Annotated[str,   Field(..., description='id of patient',    examples=['P001'])]
    name:   Annotated[str,   Field(..., description='name of patient',  examples=['moosa'])]
    city:   Annotated[str,   Field(..., description='city of patient',  examples=['faisalabad'])]
    age:    Annotated[int,   Field(..., description='age of patient',   gt=0)]
    gender: Annotated[Literal['male','female','other'], Field(...)]
    height: Annotated[float, Field(..., gt=0.0, description='height in meters')]
    weight: Annotated[float, Field(..., gt=0,   description='weight in kgs')]

    @computed_field
    def bmi(self) -> float:         # auto calculated
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    def verdict(self) -> str:       # auto calculated
        if self.bmi < 18.5: return 'Underweight'
        elif self.bmi < 30: return 'Normal'
        else:               return 'Obese'
```

### PatientUpdate (Edit)
All fields optional — client only sends what they want to change.

```python
class patientupdate(BaseModel):
    name:   Optional[str]   = None
    city:   Optional[str]   = None
    age:    Optional[int]   = None    # gt=0
    gender: Optional[Literal['male','female','other']] = None
    height: Optional[float] = None    # gt=0
    weight: Optional[float] = None    # gt=0
```

```
Patient          →  all fields required   (creating new record)
patientupdate    →  all fields optional   (editing existing record)
                    only send what changed
                    rest stays the same ✅
```

---

## 📡 API Endpoints

```
┌────────┬────────────────────────┬──────────────────────────────┐
│ Method │ Endpoint               │ Description                  │
├────────┼────────────────────────┼──────────────────────────────┤
│ GET    │ /                      │ health check                 │
│ GET    │ /about                 │ about page                   │
│ GET    │ /view                  │ fetch all patients           │
│ GET    │ /view/{patient_id}     │ fetch specific patient       │
│ GET    │ /sort                  │ sort patients by field       │
│ POST   │ /create                │ add new patient              │
│ PUT    │ /edit/{patient_id}     │ update existing patient      │
│ DELETE │ /delete/{patient_id}   │ remove patient               │
└────────┴────────────────────────┴──────────────────────────────┘
```

---

## 🔖 Path Parameters

Path parameters are **part of the URL itself** — used to identify a specific resource.

```
/view/P001
      ^^^^
      path parameter — tells API WHICH patient you want
```

```python
@app.get("/view/{patient_id}")
def fetchpatient(
    patient_id: str = Path(..., description='id of patient in DB', example='P001')
):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='patient id not found in DB')
```

```
GET /view/P001   →  returns patient P001  ✅
GET /view/P999   →  404 patient not found ❌
GET /view/       →  route doesn't match   ❌
```

---

## 🔎 Query Parameters

Query parameters come **after the `?` in the URL** — used for filtering, sorting, and searching.

```
/sort?sort_by=age&order_by=desc
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      query parameters — tell API HOW to return the data
```

```python
@app.get('/sort')
def sort_patients(
    sort_by:  str = Query(...,    description='sort on basis of key'),
    order_by: str = Query('asc', description='asc or desc')
):
    data       = load_data()
    valid_fields = ['height', 'age', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail='choose valid field')

    reverse = order_by == 'desc'
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=reverse)
    return sorted_data
```

```
GET /sort?sort_by=age               →  sorted by age ascending  ✅
GET /sort?sort_by=bmi&order_by=desc →  sorted by bmi descending ✅
GET /sort?sort_by=name              →  400 invalid field        ❌
```

```
┌──────────────────┬────────────────────────────────────────────┐
│                  │ Path Param          Query Param            │
├──────────────────┼────────────────────────────────────────────┤
│ URL position     │ /patients/P001      ?sort_by=age           │
│ Purpose          │ identify resource   filter / sort / search │
│ Required?        │ yes                 can be optional        │
│ FastAPI access   │ Path(...)           Query(...)             │
└──────────────────┴────────────────────────────────────────────┘
```

---

## 📥 GET — Read Data

```python
# Get all patients
@app.get("/view")
def view():
    data = load_data()
    return data

# Get one patient by ID
@app.get("/view/{patient_id}")
def fetchpatient(patient_id: str = Path(..., example='P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='patient id not found in DB')
```

```
GET /view        →  200 returns all patients
GET /view/P001   →  200 returns P001 data
GET /view/P999   →  404 patient not found
```

---

## 📤 POST — Create Data

```python
@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='already exists')

    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201, content={'message': 'patient added'})
```

```
Client sends JSON body:
{
    "id":     "P006",
    "name":   "Moosa",
    "city":   "Faisalabad",
    "age":    22,
    "gender": "male",
    "height": 1.75,
    "weight": 70
}
         │
         ▼
Pydantic validates all fields ✅
BMI and verdict auto computed ✅
Saved to patients.json ✅
         │
         ▼
201 Created → { "message": "patient added" }
```

---

## ✏️ PUT — Update Data

```python
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, update_patient: patientupdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='patient not found')

    exist_patient = data[patient_id]
    update = update_patient.model_dump(exclude_unset=True)  # only changed fields

    for key, value in update.items():
        exist_patient[key] = value

    exist_patient['id'] = patient_id
    patient = Patient(**exist_patient)           # re-validate full object
    data[patient_id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Ok'})
```

```
Client sends ONLY what changed:
PUT /edit/P001
{ "weight": 80 }      ← only weight updated
                          everything else stays the same

exclude_unset=True     ← key feature
                          only fields client actually sent
                          are included in the update ✅
```

---

## 🗑️ DELETE — Remove Data

```python
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='patient not found')

    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Ok'})
```

```
DELETE /delete/P001  →  200 patient deleted ✅
DELETE /delete/P999  →  404 patient not found ❌
```

---

## ▶️ Run the Project

```bash
# 1. Clone the repo
git clone https://github.com/moosarehan/fastapi-ml-fundamentals.git
cd fastapi-ml-fundamentals

# 2. Create virtual environment
python -m venv myenv
myenv\Scripts\activate        # Windows
source myenv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn main:app --reload
```

```
Server running at:

http://localhost:8000        ← API base URL
http://localhost:8000/docs   ← Swagger UI (auto generated) ✅
http://localhost:8000/redoc  ← ReDoc UI (auto generated)   ✅
```

---

<div align="center">

> 📎 **Pydantic Notes:** All Pydantic concepts used in this project are documented in detail here:
> **[🔗 pydantic-fundamentals](https://github.com/moosarehan/pydantic-fundamentals)**

![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/Powered%20by-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

</div>

from fastapi import FastAPI

app = FastAPI(title="konsulent-api")

KONSULENTER = [
    {"id": 1, "navn": "Anna K.", "ferdigheter": ["python", "fastapi"], "belastning_prosent": 40},
    {"id": 2, "navn": "Leo T.", "ferdigheter": ["python", "data"], "belastning_prosent": 20},
    {"id": 3, "navn": "Sara N.", "ferdigheter": ["java", "spring"], "belastning_prosent": 80},
]

@app.get("/konsulenter")
def get_konsulenter():
    return KONSULENTER
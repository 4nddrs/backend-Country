from fastapi import FastAPI

app = FastAPI(title="Mi API con FastAPI")


@app.get("/")
def root():
    return {"message": "¡Hola FastAPI!"}

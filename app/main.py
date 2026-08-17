from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Expense Tracker API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
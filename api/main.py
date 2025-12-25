# uvicorn main:app --reload --host 0.0.0.0 --port 8000

from fastapi import FastAPI
from run_predict import predict
import uvicorn

app = FastAPI(title="Lottery Engine")


@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/predict")
def predict_api(top_n: int = 10):
    predict(top_n)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

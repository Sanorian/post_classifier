from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import os
import numpy as np

app = FastAPI()

ARTIFACTS_DIR = "artifacts"
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "model.joblib")
VECTORIZER_PATH = os.path.join(ARTIFACTS_DIR, "vectorizer.joblib")
CATEGORIES_PATH = os.path.join(ARTIFACTS_DIR, "categories.joblib")

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    categories = joblib.load(CATEGORIES_PATH)
    print("Артефакты успешно загружены")
except Exception as e:
    print(f"Ошибка загрузки артефактов: {e}")
    model = None
    vectorizer = None
    categories = None

@app.get('/health')
def check_health():
    if model is None or vectorizer is None:
        return {"status": "error", "model_loaded": model is not None, "vectorizer_loaded": vectorizer is not None}
    return {"status": "ok", "num_classes": len(categories)}

class ClassifyPostRequest(BaseModel):
    text: str

@app.post('/classify')
def classify(request: ClassifyPostRequest):
    if model is None or vectorizer is None or categories is None:
        raise HTTPException(status_code=503, detail="Модель или векторизатор не загружены")
    if request.text=="":
        raise HTTPException(status_code=422, detail="Пустой текст не может быть классифицирован")
    try:
        X = vectorizer.transform([request.text])
        proba = model.predict_proba(X)[0]
        pred_id = int(np.argmax(proba))
        category = categories[pred_id]
        confidence = float(proba[pred_id])
        top_indices = np.argsort(proba)[::-1][:3]
        top3 = [
            {"category": categories[i], "probability": float(proba[i])}
            for i in top_indices
        ]
        return {"category": category, "confidence": confidence, "top3": top3}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
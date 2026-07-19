from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Merhaba, Vercel Python çalışıyor! 🚀"}

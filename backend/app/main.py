from fastapi import FastAPI

app = FastAPI(title="RemitCompare API")


@app.get("/api/health")
def health():
    return {"status": "ok"}

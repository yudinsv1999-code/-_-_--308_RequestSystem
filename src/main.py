from fastapi import FastAPI
from src.api.errors import register_error_handlers
from src.api import routes_requests, routes_comments, routes_refs

app = FastAPI(title="Система учёта заявок", version="1.0.0")
register_error_handlers(app)
app.include_router(routes_requests.router)
app.include_router(routes_comments.router)
app.include_router(routes_refs.router)

@app.get("/health")
def health():
    return {"status": "ok"}

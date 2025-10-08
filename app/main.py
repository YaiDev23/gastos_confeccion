from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from api.endpoints import router

app = FastAPI()

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)


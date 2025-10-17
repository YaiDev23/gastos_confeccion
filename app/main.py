from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from app.api.endpoints import router

app = FastAPI()

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

# Configurar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static_files")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)


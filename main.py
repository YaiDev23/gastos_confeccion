from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from app.api.delivery_endpoints import router as delivery_router
from app.api.endpoints_assistence import router as assistence_router
from app.api.worker_endpoints import router as worker_router
from app.api.templates_endpoints import router as templates_router
from app.api.factory_endpoints import router as factory_router
from app.api.auth_endpoints import router as auth_router
from app.api.user_endpoints import router as user_router
from app.api.admin_endpoints import router as admin_router
from app.api.endpoints import router

app = FastAPI()

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

# Configurar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static_files")

app.include_router(templates_router, prefix="", tags=["Templates"])
app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(user_router, prefix="", tags=["Users"])
app.include_router(router, prefix="", tags=["General"])
app.include_router(admin_router, prefix="", tags=["Admin"])
app.include_router(delivery_router, prefix="/api", tags=["Delivery"])  
app.include_router(assistence_router, prefix="/assistence", tags=["Assistence"])
app.include_router(worker_router, prefix="/api", tags=["Workers"])
app.include_router(factory_router, prefix="/api", tags=["Factories"])


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)


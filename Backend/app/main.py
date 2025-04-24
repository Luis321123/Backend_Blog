from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.settings import get_settings

settings = get_settings()

def create_application() -> FastAPI:
    application = FastAPI(
        title="Gestión de inventario",
        version="0.0.1",
        description="Bienvenido a Consuming.",
        docs_url="/docs",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "defaultModelExpandDepth": -1,
            "docExpansion": "none",
            "persistAuthorization": True,
            "tryItOutEnabled": True,
            "syntaxHighlight.theme": "obsidian",
            "displayOperationId": True,
            # Configuración clave para el login simple
            "initOAuth": {
                "useBasicAuthenticationWithAccessCodeGrant": True,
                "defaultUsername": settings.FIRST_ADMIN_EMAIL,
                "defaultPassword": settings.FIRST_ADMIN_PASSWORD
            }
        }
    )

    application.include_router(api_router, prefix="/api")
    
    return application

app = create_application()

# Configuración CORS
origins = [str(settings.FRONTEND_HOST)]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hi, I am Louis - Your app is done & working, if u have problems contact me (luis1233210e@gmail.com)."}
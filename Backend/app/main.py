from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import health
from app.api.api import api_router
import logging
from app.core.settings import settings

logging.basicConfig(level=logging.INFO)

def create_application():
    application = FastAPI(
        title=" Blog Backend ",
        version="0.0.1",
        description="Bienvenido a Blog.",
        docs_url="/docs", 
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1, 
            "defaultModelExpandDepth": -1,   
            "docExpansion": "none",
            "persistAuthorization": True,    
            "tryItOutEnabled":True,           
        }
    )

    application.include_router(api_router)
    return application

# Configura COR
app = create_application()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye routers
app.include_router(health.router)
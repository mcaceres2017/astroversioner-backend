import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from config import DATASETS_PATH, DATASETS_PATH_HOST
from routers.dataset_routes import dataset_router
from routers.users_routes import users_router
from database.db_connector import *
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json


app = FastAPI()


# Configuración de las políticas de CORS
origins = [
    "192.168.6.248",  # Reemplaza con la URL de tu aplicación web
    "http://astrocollab.inf.udec.cl",
    "https://astrocollab.inf.udec.cl",
    # Agrega más orígenes permitidos si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Puedes especificar los métodos HTTP permitidos
    allow_headers=["*"],  # Puedes especificar los encabezados permitidos
)


# Manejo de errores generales
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500, content={"message": "Error interno del servidor"}
    )


app.include_router(dataset_router, prefix="/versioner/dataset")
app.include_router(users_router, prefix="/versioner/users")


@app.get("/versioner/")
def index():
    return "Versioner 0.1.1"


@app.get("/versioner/features")
async def dataset_metadata_get():
    with open("utils/features_mockup.json", "r") as openfile:
        json_features = json.load(openfile)
        print(f"json_features: {json_features}")
        return json_features


if __name__ == "__main__":
    #    os.chdir(DATASETS_PATH_HOST)
    uvicorn.run(app, host="0.0.0.0", port=8003)

from fastapi import FastAPI
from src.general import general_routes
from src.cve_to_attack import cve_to_attack_routes

app = FastAPI()

app.include_router(general_routes.router)
app.include_router(cve_to_attack_routes.router)
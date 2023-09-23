from fastapi import FastAPI
from src.general import general_routes
from src.cve_to_attack import cve_to_attack_routes
from src.nl_to_sql import nl_to_sql_routes

app = FastAPI()

app.include_router(general_routes.router)
app.include_router(cve_to_attack_routes.router)
app.include_router(nl_to_sql_routes.router)
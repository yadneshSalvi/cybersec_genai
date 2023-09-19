from fastapi import FastAPI
from src.sample_stream import stream_routes
import uvicorn

app = FastAPI()

app.include_router(stream_routes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
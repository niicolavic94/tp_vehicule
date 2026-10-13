
import uvicorn
from fastapi import FastAPI

from parc_vehicule.routers.cars import router as cars_router
from parc_vehicule.routers.motors import router as motors_router

app = FastAPI()

app.include_router(cars_router)
app.include_router(motors_router)


@app.get("/")
async def home():
    return {"message": "Bienvenue dans la gestion du parc de véhicules"}


def main():
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    main()

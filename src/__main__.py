import uvicorn
from fastapi import FastAPI
from .routes.meals import router as meals_router

app = FastAPI()



app.include_router(meals_router, prefix="/v1/api")


def main():
    uvicorn.run(app, port=8100)


if __name__ == "__main__":
    main()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.assumptions_controller import router as assumptions_controller
from controllers.status_controller import router as status_controller

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assumptions_controller)
app.include_router(status_controller)

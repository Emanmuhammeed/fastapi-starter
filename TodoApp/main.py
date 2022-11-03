from fastapi import FastAPI,Depends
import models
from database import engine
from routers import auth, todos
from company import companyapis, dependences

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(
    companyapis.router,
    prefix="/company",
    tags=["company"],
    dependencies=[Depends(dependences.get_token_header)],
    responses={408: {"description": "Internal company only"}}
)


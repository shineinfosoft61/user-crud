from fastapi import FastAPI

from database import engine
import models
from router.admin.v1.api import router as user_router


app = FastAPI(
    title="User_crud",
    description="Fast_crud",
    version="1.0.0",
    redoc_url=None,
)

models.Base.metadata.create_all(bind = engine)

app.include_router(user_router)

"""heloo"""

"""hii"""
"""hello"""
"""hello parth patel how are you"""
"""hello ronak"""

# scheduler/main.py
from fastapi import FastAPI
from scheduler.agent_routes import router as agent_router
from scheduler.admin_routes import router as admin_router
from scheduler.log_routes import router as log_router
from scheduler.job_routes import router as job_router
from scheduler.job_visibility_routes import router as job_visibility_router
from scheduler.ui_routes import router as ui_router

app = FastAPI()
app.include_router(job_router)
app.include_router(job_visibility_router)
app.include_router(agent_router)
app.include_router(admin_router)
app.include_router(log_router)
app.include_router(ui_router)
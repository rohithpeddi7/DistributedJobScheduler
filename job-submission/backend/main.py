from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from typing import Annotated
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from file_handler import *
from db_handler import add_job_to_db, remove_job_from_db
import os
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

load_dotenv()
app = FastAPI()

MONGO_CONN_STR = os.getenv("DB_CONN_STR")
MONGO_DB_NAME = os.getenv("DB_NAME")
app.mongodb_client = AsyncIOMotorClient(MONGO_CONN_STR)
app.mongodb = app.mongodb_client[MONGO_DB_NAME]


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/jobs")
async def post_job(request: Request, cron_expression: Annotated[str, Form(description="Enter the cron expression for the job")], is_one_time: Annotated[bool, Form(description="If periodic or one-time")], scheduled_time: Annotated[str, Form(description="Scheduled time for one time job")],file: Annotated[UploadFile, File(description="Upload the dockerfile")],):
    print("Debug: filename: ", file.filename)
    print("Debug: cron expression: ", cron_expression)
    print("Debug: is one-time: ", is_one_time)
    print("Debug: scheduled time: ", scheduled_time)
    
    file_upload_res = await add_file(file)
    
    print("Debug: file name: ", file_upload_res["filename"])
    print("Debug: firebase path: ", file_upload_res["firebase_path"])
    print("Debug: public url: ", file_upload_res["public_url"])

    file_url = file_upload_res["public_url"]
    if is_one_time:
      cron_expression = scheduled_time
    res = await add_job_to_db(app.mongodb, file_url, cron_expression, is_one_time)
    return templates.TemplateResponse("success.html", {"request": request, "job_id": str(res.inserted_id)})

@app.post("/jobs/delete/{job_id}")
async def delete_job(job_id):

  res = await remove_job_from_db(app.mongodb, job_id)

  if res==0:
    return {"message": f"Successfully deleted the job with id {job_id}"}
  elif res==-1:
    return {"message": f"Couldn't find any job with id {job_id}"}
  else:
    return {"message": f"Some error occurred"}
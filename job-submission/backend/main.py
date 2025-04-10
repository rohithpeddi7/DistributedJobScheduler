from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from typing import Annotated
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from file_handler import *
from db_handler import add_job_to_db, remove_job_from_db
import os

load_dotenv()
app = FastAPI()

MONGO_CONN_STR = os.getenv("DB_CONN_STR")
MONGO_DB_NAME = os.getenv("DB_NAME")
app.mongodb_client = AsyncIOMotorClient(MONGO_CONN_STR)
app.mongodb = app.mongodb_client[MONGO_DB_NAME]


@app.get("/")
def root():
    content="""
    <!DOCTYPE html>
<html>
<head>
  <title>Job Scheduler</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f7f8;
      margin: 0;
      padding: 0;
    }

    form {
      max-width: 500px;
      margin: 50px auto;
      background: #fff;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: bold;
    }

    input[type="text"],
    input[type="file"],
    input[type="datetime-local"] {
      width: 100%;
      padding: 10px;
      margin-bottom: 20px;
      border: 1px solid #ccc;
      border-radius: 6px;
    }

    input[type="checkbox"] {
      margin-right: 10px;
    }

    #cron_expression_container,
    #scheduled_time_container {
      margin-bottom: 20px;
    }

    input[type="submit"] {
      background-color: #007BFF;
      color: white;
      border: none;
      padding: 12px 20px;
      font-size: 16px;
      border-radius: 6px;
      cursor: pointer;
    }

    input[type="submit"]:hover {
      background-color: #0056b3;
    }
  </style>
  <script>
    function toggleScheduleInputs() {
      const checkbox = document.getElementById('is_one_time_checkbox');
      const cronInput = document.getElementById('cron_expression_container');
      const dateTimeInput = document.getElementById('scheduled_time_container');

      if (checkbox.checked) {
        cronInput.style.display = 'none';
        dateTimeInput.style.display = 'block';
      } else {
        cronInput.style.display = 'block';
        dateTimeInput.style.display = 'none';
      }
    }

    window.onload = function() {
      toggleScheduleInputs();
      document.getElementById('is_one_time_checkbox').addEventListener('change', toggleScheduleInputs);
    };
  </script>
</head>
<body>
  <form action="/jobs" enctype="multipart/form-data" method="post">
    <label for="dockerfile_for_job_scheduling">Select your Dockerfile</label>
    <input name="file" type="file" id="dockerfile_for_job_scheduling">

    <input type="hidden" name="is_one_time" value="false">

    <label>
      <input name="is_one_time" type="checkbox" id="is_one_time_checkbox">
      One-time job?
    </label>
    <input type="hidden" name="cron_expression" value="">
    <div id="cron_expression_container">
      <label for="cron_expression">Cron Expression</label>
      <input name="cron_expression" type="text" id="cron_expression">
    </div>
    <input type="hidden" name="scheduled_time" value="">
    <div id="scheduled_time_container" style="display: none;">
      <label for="scheduled_time">Scheduled Time</label>
      <input name="scheduled_time" type="datetime-local" id="scheduled_time">
    </div>

    <input type="submit" value="Submit Job">
  </form>
</body>
</html>
    """
    return HTMLResponse(content=content)

@app.post("/jobs")
async def post_job(cron_expression: Annotated[str, Form(description="Enter the cron expression for the job")], is_one_time: Annotated[bool, Form(description="If periodic or one-time")], scheduled_time: Annotated[str, Form(description="Scheduled time for one time job")],file: Annotated[UploadFile, File(description="Upload the dockerfile")],):
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
    return {"message": f"Successful! Job id is {res.inserted_id}"}

@app.post("/jobs/delete/{job_id}")
async def delete_job(job_id):

  res = await remove_job_from_db(app.mongodb, job_id)

  if res==0:
    return {"message": f"Successfully deleted the job with id {job_id}"}
  elif res==-1:
    return {"message": f"Couldn't find any job with id {job_id}"}
  else:
    return {"message": f"Some error occurred"}
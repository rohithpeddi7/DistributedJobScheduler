from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime
from croniter import croniter
from bson import ObjectId
import time
import os
from kafka import KafkaProducer
from config import *

producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

load_dotenv()

MONGO_CONN_STR = os.getenv("DB_CONN_STR")
MONGO_DB_NAME = os.getenv("DB_NAME")

mongodb_client = AsyncIOMotorClient(MONGO_CONN_STR)
mongodb = mongodb_client[MONGO_DB_NAME]

async def job_fetcher(db):

    while True:

        time.sleep(40)

        collection = db.scheduled_jobs

        current_time = datetime.now()

        cursor = collection.find({"next_run_at":{"$lte": current_time}}).sort("next_run_at")
        for document in await cursor.to_list():
            producer.send(document)
            job_id = document["_id"]
            cron_expression = document["cron_expression"]
            next_run_at = croniter(croniter, current_time).next(datetime)
            result = await collection.replace_one({"_id": job_id}, {"next_run_at":next_run_at})



    



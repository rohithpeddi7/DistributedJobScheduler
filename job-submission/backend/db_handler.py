from bson import ObjectId

async def add_job_to_db(db, dockerfile_name, cron_expression, is_one_time):
    """
    Add a single job to the database.
    """

    document = {"dockerfile_name": dockerfile_name, 
                "is_one_time": is_one_time, 
                "cron_expression": cron_expression}

    collection = db.scheduled_jobs
    result = await collection.insert_one(document)
    print("Debug: ", result, result.inserted_id)
    return result

async def remove_job_from_db(db, job_id):

    collection = db.scheduled_jobs

    result = await collection.delete_one({"_id": ObjectId(job_id)})
    if result.deleted_count == 1:
        print(f"Debug: Job with job_id {job_id} deleted successfully.")
        return 0
    else:
        print(f"Debug: No job found with the ID {job_id}.")
        return -1

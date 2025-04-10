### Order of execution of diff files

1. python worker.py 
2. python worker.py (Another instance)
3. python job_status_listener.py
4. python job_scheduler.py (For simulating addition of jobs)
5. python coordinator.py

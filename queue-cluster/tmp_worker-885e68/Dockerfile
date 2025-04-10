FROM python:3.10-slim

# Download the script during build time
ADD https://firebasestorage.googleapis.com/v0/b/dockerfile-f6553.firebasestorage.app/o/uploads%2Fsimple_script.py?alt=media&token=9b969367-6262-47d9-b7eb-cb07d2f2d309 job-script.py

CMD ["python", "job-script.py"]

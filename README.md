# 🧠 Distributed Job Scheduler with Kafka and Docker

A scalable, fault-tolerant system that allows users to schedule and execute Docker-based jobs through a web interface. Jobs are processed by a pool of workers using Kafka for communication, with scheduling handled by a periodic service.

---

## 🚀 Features

- 🖥 **Web UI + FastAPI backend** for job submission  
- ⏱ **Job Scheduler** service that enqueues jobs at the correct time  
- 🧩 **Coordinator** assigns jobs to available workers  
- 🛠 **Worker** processes jobs by building and running Docker containers from remote Dockerfile URLs  
- 🔁 **Kafka topics** used for inter-service communication  
- 📡 **Heartbeat and availability** tracking for workers  
- ✅ **Status reporting** for job execution results  
- 🗃 **MongoDB** used to store job metadata

---

## 🧱 Architecture Overview

```
User → FastAPI + UI → MongoDB
                           ↓
                 [Scheduler - runs every min]
                           ↓
                    Kafka (jobs-queue)
                           ↓
               [Coordinator assigns jobs]
                           ↓
                Kafka (worker-{id} topic)
                           ↓
                      Worker nodes
                           ↓
                   Kafka (job-status)
```

---

## 🧰 Technologies Used

- 🐍 Python (FastAPI, threading, subprocess)
- 🐳 Docker (for executing submitted jobs)
- 🍃 MongoDB (for job metadata)
- 🐘 Apache Kafka (message queue for coordination)
- 🌐 Firebase (Dockerfile hosting)
- 🔄 Golang (for REST Execution Service)

---

## 📦 Kafka Topics

| Topic Name            | Purpose                               |
|-----------------------|----------------------------------------|
| `jobs-queue`          | Scheduler → Coordinator                |
| `worker-availability` | Worker → Coordinator                   |
| `worker-heartbeat`    | Worker → Coordinator                   |
| `worker-{id}`         | Coordinator → Worker                   |
| `job-status`          | Worker → Backend or Logger             |

---


## 🏁 Job Lifecycle

1. User submits job (with Dockerfile URL + scheduled time)
2. Scheduler enqueues job into Kafka at scheduled time
3. Coordinator assigns job to a free worker
4. Worker fetches Dockerfile, builds and runs it
5. Worker reports status to Kafka
6. (Optional) Backend stores the result in MongoDB

---

## 🔄 Scalability

- Stateless services → easy to scale horizontally
- Kafka handles high-throughput message delivery
- Workers can be autoscaled based on job volume
- MongoDB handles dynamic schemas and high insert rate
- Decoupled components make monitoring and fault isolation easy

---

## 🧑‍💻 Author

Team: __Flint and Steel__
🚨 **Money Muling Detection Engine**

Graph-Based Financial Crime Intelligence System
A graph-powered fraud detection engine designed to detect money muling networks, circular laundering chains, and suspicious transaction rings using transaction data.
This system converts raw financial records into risk-scored intelligence dashboards and interactive fraud network visualizations.


🔗 Live Demo URL

👉 Live Application (Render Hosted): https://rift-money-muling-aarf.onrender.com/


🛠 **Tech Stack**


🔹 Backend

-Python
-FastAPI
-pandas
-NumPy

🔹 Frontend

HTML
CSS
JavaScript
Cytoscape.js (Graph Visualization)
Chart.js (Analytics & Risk Gauges)
jsPDF (Executive Reports)


🔹 Deployment

Render (Cloud Hosting)

GitHub (Version Control & CI)



🏗** System Architecture**

High-Level Architecture
User Browser (Dashboard UI)
        │
        ▼
Render Cloud Deployment
        │
        ▼
FastAPI Backend (Fraud Engine API)
        │
        ├── Data Validation Layer
        ├── Graph Construction Module
        ├── Fraud Detection Engine
        ├── Suspicion Scoring Module
        │
        ▼
JSON Risk Intelligence Output
        │
        ▼
Interactive Fraud Dashboard + PDF Report




**Data Flow**

CSV Upload
   ↓
Transaction Parsing
   ↓
Graph Creation (Accounts → Nodes, Transfers → Edges)
   ↓
Pattern Detection
   ↓
Suspicion Score Calculation
   ↓
Fraud Network Visualization



🔍 **Algorithm Approach**

The system models transactions as a Directed Graph G(V, E):

V → Accounts

E → Transactions

Three primary detection mechanisms are implemented:

1️⃣ **Circular Fund Routing (Cycle Detection)**

Detects loops where funds return to the originating account through multiple intermediaries.

Method: Depth-First Search (DFS)

Complexity: O(N + E)

Used to detect laundering rings.

2️⃣ **Smurfing Detection (Fan-in / Fan-out)**

Identifies accounts that:

Receive many small transactions rapidly

Distribute funds to many accounts

Complexity: O(E)

Used to detect mule aggregators.

3️⃣ **Layered Shell Networks**

Detects multi-hop transaction chains used to obscure money trails.

Complexity: O(N × H)
(H = maximum hop depth)

Used to detect obfuscation chains.



📊 **Suspicion Score Methodology**

Each account is assigned a Suspicion Score (0–100).

Score Components:

Cycle Participation Weight

Transaction Velocity

Multi-hop Layering Depth

Network Centrality


**Scoring Formula:**

Final Score = w1(Cycle Participation) + w2(Transaction Velocity) + w3(Layering Depth) + w4(Network Centrality)

Accounts exceeding defined thresholds are flagged as high-risk mule accounts.

These scores power:

-Dashboard highlights

-Fraud ranking

-Risk gauge visualization



💻 **Installation & Setup**

1️⃣ Clone Repository

-git clone https://github.com/RamyaPat/money-muling-engine.git
-cd money-muling-engine

2️⃣ Create Virtual Environment

-python -m venv .venv
-source .venv/bin/activate      # Mac/Linux
-venv\Scripts\activate         # Windows

3️⃣ Install Dependencies

-pip install -r requirements.txt

4️⃣ Run Application
uvicorn main:app --reload

Open browser:

http://127.0.0.1:8000



🖱 **Usage Instructions**

-Upload a CSV file with the following format:

transaction_id, sender_id, receiver_id, amount, timestamp

Click Run Fraud Analysis

View:

Total accounts analyzed

Suspicious accounts flagged

Fraud rings detected

Processing time

Explore interactive fraud network graph.

Export Executive PDF Report.




⚠** Known Limitations**

-Uses heuristic-based detection (may produce false positives)

-Tested on datasets up to ~10,000 transactions

-No real-time streaming integration

-No direct banking API integration

-No persistent database (stateless processing)


👥 **Team Members**

Ramya P
Sai Amrutha K J


🏁 Hackathon Submission
Built for RIFT 2026 Hackathon
Track: Graph Theory / Financial Crime Detection

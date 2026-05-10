# 🚀 Smart-IP Auditor Engine
### **Advanced AI-Powered Patent Analysis System**

The **Smart-IP Auditor Engine** is a high-performance legal-tech solution designed to automate the process of patent auditing and similarity detection. Built for intellectual property authorities (like **SAIP**), it utilizes Large Language Models (LLMs) to understand the technical "spirit" of an invention rather than just keyword matching.

---

## 🌟 Key Features
* **Semantic Comparison:** Uses **Llama 3.3 (70B)** to compare two technical documents and generate a detailed similarity score.
* **Automated Claim Extraction:** Automatically identifies core technical claims and innovations.
* **Multi-Format Support:** Seamlessly processes **PDF, DOCX, and TXT** files.
* **Security First:** Architected with strict environment variable management to protect sensitive API keys.
* **Modern UI:** A clean, responsive dashboard built with **FastAPI** and **Next.js/Tailwind** concepts.

---

## 🛠️ Technical Stack
* **Language:** Python 3.12+
* **Framework:** FastAPI (Backend)
* **AI Engine:** Groq Cloud API (Llama-3.3-70b-versatile)
* **Document Parsing:** `pdfplumber`, `python-docx`
* **Environment:** `python-dotenv`

---

## 🚀 Quick Start

### 1. Prerequisites
- Python installed on your machine.
- A **Groq API Key** (Get it from [Groq Console](https://console.groq.com/)).

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/Eng-Osama-Sadek/saip-ai-auditor.git](https://github.com/Eng-Osama-Sadek/saip-ai-auditor.git)

# Navigate to project folder
cd saip-ai-auditor

# Install dependencies
pip install -r requirements.txt
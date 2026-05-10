import os
import pdfplumber
import docx
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from groq import Groq
from dotenv import load_dotenv

# 1. تحميل الإعدادات الأمنية من ملف .env
load_dotenv()

app = FastAPI()

# 2. إعداد اتصال جروك (التأكد من وجود المفتاح)
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("Error: GROQ_API_KEY is missing from .env file!")

client = Groq(api_key=api_key)

# 3. محرك استخراج النصوص (يدعم PDF, Docx, Text)
async def extract_text(file: UploadFile):
    filename = file.filename.lower()
    content = ""
    
    if filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            content = "".join([page.extract_text() for page in pdf.pages if page.extract_text()])
            
    elif filename.endswith(".docx"):
        doc = docx.Document(file.file)
        content = "\n".join([p.text for p in doc.paragraphs])
        
    else:
        # للملفات النصية العادية .txt أو .py
        read_content = await file.read()
        content = read_content.decode("utf-8")
        
    return content

# 4. مسار الصفحة الرئيسية (الواجهة)
@app.get("/", response_class=HTMLResponse)
async def home():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: index.html not found!</h1>"

# 5. مسار معالجة البيانات والذكاء الاصطناعي
@app.post("/analyze")
async def analyze_patent(
    file1: UploadFile = File(...), 
    file2: UploadFile = File(None), 
    action: str = Form(...)
):
    try:
        text1 = await extract_text(file1)
        
        # تحضير الـ Prompt بناءً على نوع العملية
        if action == "compare" and file2:
            text2 = await extract_text(file2)
            prompt = (
                f"Compare these two technical documents for patent similarity:\n\n"
                f"Document A: {text1[:3000]}\n\n"
                f"Document B: {text2[:3000]}\n\n"
                "Task: Provide a similarity score (0-100%), list overlapping claims, "
                "and identify unique innovations in each."
            )
        else:
            prompt = (
                f"Analyze this document for technical innovation and patentability:\n\n"
                f"{text1[:4000]}\n\n"
                "Task: Summarize core claims and evaluate potential for patent registration."
            )

        # إرسال الطلب لـ Groq (Llama-3.3)
        response = client.chat.completions.create(
            messages=[{
                "role": "system", 
                "content": "You are an expert Patent Examiner at SAIP (Saudi Authority for Intellectual Property)."
            }, {
                "role": "user", 
                "content": prompt
            }],
            model="llama-3.3-70b-versatile",
        )
        
        return {"report": response.choices[0].message.content}
        
    except Exception as e:
        return {"error": f"حدث خطأ أثناء المعالجة: {str(e)}"}

# 6. تشغيل السيرفر
if __name__ == "__main__":
    import uvicorn
    print("[*] Starting SAIP Smart Auditor Engine...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
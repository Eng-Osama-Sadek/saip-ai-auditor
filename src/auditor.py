import os
from groq import Groq
from datetime import datetime

# حط مفتاح جروك هنا
GROQ_API_KEY = "os.getenv"

class PatentAuditor:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        # الموديل الأحدث في 2026
        self.model = "llama-3.3-70b-versatile"

    def audit(self, file_path):
        if not os.path.exists(file_path):
            print(f"[-] File '{file_path}' not found.")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        print(f"[*] Analyzing content via Groq (Llama-3.3)...")
        
        prompt = (
            "Analyze the following text for technical innovation and potential "
            "similarities with existing patents. Identify the core 'claims' and "
            f"provide a logical audit:\n\n{content}"
        )

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            )
            report = chat_completion.choices[0].message.content
            self._save_report(file_path, report)
        except Exception as e:
            print(f"[-] Groq Error: {e}")

    def _save_report(self, file_name, report):
        if not os.path.exists('reports'): os.makedirs('reports')
        out_path = f"reports/patent_audit_{datetime.now().strftime('%H%M%S')}.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[+] SUCCESS! Report generated at: {out_path}")

if __name__ == "__main__":
    auditor = PatentAuditor(GROQ_API_KEY)
    target = input("Enter file to analyze: ").strip()
    if target:
        auditor.audit(target)
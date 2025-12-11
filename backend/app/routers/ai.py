from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI"])

class ChatRequest(BaseModel):
    question: str
    context: dict = {}

@router.post("/ask")
def ask_ai(req: ChatRequest):
    # Mock AI logic
    question = req.question.lower()
    answer = "I'm analyzing your request..."
    
    if "exploit" in question:
        answer = "This vulnerability can be exploited by injecting a malicious script into the 'callback' parameter. Since there is no input sanitization, the browser executes the script."
    elif "impact" in question:
        answer = "The business impact is CRITICAL. An attacker could steal session tokens, leading to account takeover of administrative users."
    elif "fix" in question:
        answer = "I recommend applying a WAF rule to block common XSS patterns immediately, and then scheduling a code fix to sanitize user input using a library like DOMPurify."
    else:
        answer = f"I analyzed the cluster security posture. Based on standard security practices, you should prioritize critical vulnerabilities in the production namespace."
        
    return {
        "answer": answer,
        "sources": ["OWASP Top 10", "CWE-79 Knowledge Base"],
        "confidence": 0.95
    }

@router.post("/explain/{threat_id}")
def explain_threat(threat_id: str):
    return {
        "summary": "This is a detailed AI explanation of the threat...",
        "exploitability": "High",
        "business_impact": "Critical",
        "remediation": "Apply WAF rules."
    }

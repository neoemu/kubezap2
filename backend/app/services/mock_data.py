from datetime import datetime, timedelta
from typing import List
from app.models.core import Cluster, Threat, Event, Severity, Status
import random

class MockDataService:
    def __init__(self):
        self.clusters = self._generate_clusters()
        self.threats = self._generate_threats()
        self.events = self._generate_timeline()
        self.notifications = self._generate_notifications()
        self.scan_history = self._generate_scan_history()

    def _generate_clusters(self) -> List[Cluster]:
        return [
            Cluster(id="prod-us", name="prod-us-east-1", provider="AWS EKS", namespace_count=47, pod_count=234, risk_score=78, status="connected", last_scan=datetime.now() - timedelta(minutes=3)),
            Cluster(id="prod-eu", name="prod-eu-west-1", provider="GKE", namespace_count=32, pod_count=156, risk_score=52, status="connected", last_scan=datetime.now() - timedelta(minutes=15)),
            Cluster(id="staging", name="staging-cluster", provider="AWS EKS", namespace_count=12, pod_count=89, risk_score=34, status="connected", last_scan=datetime.now() - timedelta(minutes=1)),
            Cluster(id="dev", name="dev-sandbox", provider="On-Prem", namespace_count=8, pod_count=45, risk_score=12, status="connected", last_scan=datetime.now() - timedelta(hours=1)),
        ]

    def _generate_threats(self) -> List[Threat]:
        common_ai_summary = "This vulnerability allows attackers to inject malicious scripts or commands. Because this pod handles sensitive PII data and has external ingress, the business impact is critical."
        
        return [
            Threat(
                id="T-1001", cluster_id="prod-us", title="Cross-Site Scripting (Reflected)", cwe_id="CWE-79", cve_id="CVE-2024-1234", severity=Severity.CRITICAL,
                target_namespace="payments", target_kind="Deployment", target_name="payment-api", zap_risk_score=92, status=Status.NEW,
                description="Reflected XSS in query parameter", ai_summary=common_ai_summary + " Specifically targeting the callback parameter.",
                attack_path_steps=["Internet", "Ingress", "payment-api", "User Browser"],
                zap_raw_output={"alert": "Reflected XSS", "param": "callback", "risk": "High"},
                fix_options=[{"type": "waf", "title": "Block XSS Patterns (WAF)", "desc": "Apply CloudArmor rule"}, {"type": "code", "title": "Sanitize Input", "desc": "Use DOMPurify"}]
            ),
             Threat(
                id="T-1002", cluster_id="prod-us", title="SQL Injection (Union Based)", cwe_id="CWE-89", severity=Severity.CRITICAL,
                target_namespace="users", target_kind="Service", target_name="user-svc", zap_risk_score=88, status=Status.IN_PROGRESS,
                description="SQL Injection in login form", ai_summary="Allows dumping entire database via UNION SELECT.",
                attack_path_steps=["Internet", "Ingress", "user-svc", "PostgreSQL"],
                zap_raw_output={"alert": "SQL Injection", "param": "username", "risk": "High"},
                fix_options=[{"type": "code", "title": "Use Parameterized Queries", "desc": "Switch to SQLAlchemy ORM"}]
            ),
            Threat(
                id="T-1003", cluster_id="prod-eu", title="SSRF via Webhook", cwe_id="CWE-918", severity=Severity.HIGH,
                target_namespace="integrations", target_kind="Deployment", target_name="webhook-sender", zap_risk_score=75, status=Status.NEW,
                description="Server Side Request Forgery allows accessing internal metadata service", ai_summary="Can exploit AWS Metadata service to steal IAM role credentials.",
                attack_path_steps=["Attacker", "webhook-sender", "AWS Metadata (169.254.169.254)"],
                fix_options=[{"type": "networkpolicy", "title": "Restrict Egress", "desc": "Block access to 169.254.169.254"}]
            ),
            Threat(
                id="T-1004", cluster_id="staging", title="Sensitive Data Exposure", cwe_id="CWE-200", severity=Severity.HIGH,
                target_namespace="logs", target_kind="Pod", target_name="fluentd-aggregator", zap_risk_score=70, status=Status.FIX_READY,
                description="API Keys found in environment variables", ai_summary="Hardcoded API keys visible in env vars.",
                fix_options=[{"type": "secret", "title": "Move to SealedSecrets", "desc": "Encrypt env var"}],
                attack_path_steps=["Internal Access", "Pod Describe", "Env Variables"]
            ),
             Threat(
                id="T-1005", cluster_id="prod-us", title="CORS Misconfiguration", cwe_id="CWE-942", severity=Severity.MEDIUM,
                target_namespace="frontend", target_kind="Ingress", target_name="web-app", zap_risk_score=55, status=Status.NEW,
                description="Access-Control-Allow-Origin: *", ai_summary="Allows any domain to make requests to the API.",
                fix_options=[{"type": "config", "title": "Restrict Origins", "desc": "Set specific domains"}],
                attack_path_steps=["Malicious Site", "CORS Request", "API"]
            ),
             Threat(
                id="T-1006", cluster_id="prod-us", title="Missing Security Headers", cwe_id="CWE-693", severity=Severity.LOW,
                target_namespace="frontend", target_kind="Service", target_name="landing-page", zap_risk_score=20, status=Status.IGNORED,
                description="Missing HSTS and CSP headers", ai_summary="Low risk but best practice to fix.",
                fix_options=[{"type": "config", "title": "Add Headers", "desc": "Configure Nginx headers"}],
                attack_path_steps=["Browser", "HTTP Response"]
            ),
            Threat(
                id="T-1007", cluster_id="prod-eu", title="Broken Authentication", cwe_id="CWE-287", severity=Severity.CRITICAL,
                target_namespace="auth", target_kind="Deployment", target_name="auth-server", zap_risk_score=95, status=Status.NEW,
                description="JWT token validated with 'none' algorithm", ai_summary="Anyone can forge admin tokens.",
                fix_options=[{"type": "code", "title": "Enforce RS256", "desc": "Reject none alg"}],
                attack_path_steps=["Attacker", "Forged JWT", "Admin Access"]
            ),
             Threat(
                id="T-1008", cluster_id="dev", title="Insecure Deserialization", cwe_id="CWE-502", severity=Severity.HIGH,
                target_namespace="worker", target_kind="Deployment", target_name="job-processor", zap_risk_score=80, status=Status.RESOLVED,
                description="Pickle deserialization of untrusted data", ai_summary="RCE possible via pickle payload.",
                fix_options=[{"type": "code", "title": "Use JSON", "desc": "Replace pickle with json"}],
                attack_path_steps=["Queue", "Malicious Payload", "RCE"]
            ),
            Threat(
                id="T-1009", cluster_id="staging", title="Stored XSS in Comments", cwe_id="CWE-79", severity=Severity.HIGH,
                target_namespace="social", target_kind="Service", target_name="comments-api", zap_risk_score=78, status=Status.NEW,
                description="Stored payload in database renders on page load", ai_summary="Persistent XSS affects all visitors.",
                fix_options=[{"type": "code", "title": "Sanitize Output", "desc": "Escape HTML on render"}],
                attack_path_steps=["Attacker Input", "Database", "User Browser"]
            ),
            Threat(
                id="T-1010", cluster_id="prod-us", title="SQL Injection (Boolean Blind)", cwe_id="CWE-89", severity=Severity.CRITICAL,
                target_namespace="analytics", target_kind="Deployment", target_name="report-gen", zap_risk_score=85, status=Status.NEW,
                description="Blind SQLi in sort parameter", ai_summary="Harder to exploit but allows data exfiltration.",
                fix_options=[{"type": "code", "title": "Use ORM", "desc": "Refactor raw SQL"}],
                attack_path_steps=["Attacker", "Sort Parameter", "Database"]
            ),
            # NEW THREATS for variety
            Threat(
                id="T-1011", cluster_id="prod-eu", title="XML External Entity (XXE)", cwe_id="CWE-611", severity=Severity.HIGH,
                target_namespace="services", target_kind="Deployment", target_name="xml-parser", zap_risk_score=82, status=Status.NEW,
                description="XXE vulnerability in XML parser", ai_summary="Allows reading local files and SSRF attacks.",
                fix_options=[{"type": "code", "title": "Disable External Entities", "desc": "Configure parser securely"}],
                attack_path_steps=["Malicious XML", "Parser", "File System"]
            ),
            Threat(
                id="T-1012", cluster_id="staging", title="Directory Traversal", cwe_id="CWE-22", severity=Severity.MEDIUM,
                target_namespace="files", target_kind="Service", target_name="file-server", zap_risk_score=65, status=Status.NEW,
                description="Path traversal in file download endpoint", ai_summary="Can access files outside intended directory.",
                fix_options=[{"type": "code", "title": "Validate Paths", "desc": "Use safe path joining"}],
                attack_path_steps=["Attacker", "../../etc/passwd", "File System"]
            ),
        ]

    def _generate_timeline(self) -> List[Event]:
        events = []
        templates = [
            ("SCAN_COMPLETED", "payment-api scanned in 34s → ZapRisk 84"),
            ("DEPLOY_BLOCKED", "Rollout blocked: user-svc exceeded threshold (92 > 80)"),
            ("THREAT_RESOLVED", "XSS in checkout fixed via PR #567"),
            ("FIX_GENERATED", "NetworkPolicy PR created for api-gateway"),
            ("AI_INSIGHT", "Unusual spike: 3 SQLi attempts in staging"),
            ("SCAN_COMPLETED", "webhook-sender scanned in 12s → ZapRisk 75"),
            ("THREAT_RESOLVED", "CORS issue fixed in web-app"),
            ("DEPLOY_BLOCKED", "Blocked deployment: auth-server has critical JWT flaw"),
            ("FIX_GENERATED", "WAF rule generated for payment-api XSS"),
            ("SCAN_COMPLETED", "All prod-eu namespaces scanned → Average Risk 52"),
        ]
        curr_time = datetime.now()
        for i in range(20):
             t_type, t_desc = templates[i % len(templates)]
             events.append(Event(id=i, cluster_id=random.choice(["prod-us", "prod-eu", "staging"]), type=t_type, description=t_desc, timestamp=curr_time - timedelta(minutes=i*15)))
        return events

    def _generate_notifications(self):
        """Generate realistic notifications"""
        now = datetime.now()
        return [
            {
                "id": 1,
                "type": "CRITICAL_THREAT",
                "title": "Critical: JWT Auth Bypass Detected",
                "message": "auth-server in prod-eu allows token forgery",
                "timestamp": now - timedelta(minutes=5),
                "read": False,
                "cluster": "prod-eu"
            },
            {
                "id": 2,
                "type": "DEPLOY_BLOCKED",
                "title": "Deployment Blocked",
                "message": "user-svc deployment blocked due to SQL injection",
                "timestamp": now - timedelta(minutes=30),
                "read": False,
                "cluster": "prod-us"
            },
            {
                "id": 3,
                "type": "FIX_READY",
                "title": "Fix PR Ready for Review",
                "message": "NetworkPolicy fix for webhook-sender is ready",
                "timestamp": now - timedelta(hours=2),
                "read": True,
                "cluster": "prod-eu"
            },
        ]

    def _generate_scan_history(self):
        """Generate historical scan data for trends"""
        now = datetime.now()
        history = []
        
        # Generate 30 days of data
        for i in range(30):
            date = now - timedelta(days=29-i)
            history.append({
                "date": date.strftime("%Y-%m-%d"),
                "risk_score": random.randint(50, 90),
                "threats_found": random.randint(5, 25),
                "threats_resolved": random.randint(3, 15),
                "scans_completed": random.randint(10, 50)
            })
        
        return history

mock_db = MockDataService()

# scanner.py
# Backend scanning logic using requests and BeautifulSoup
from bs4 import BeautifulSoup
import requests


def run_security_scan(target_url):
  """Scans a target URL for missing security headers and common vulnerabilities."""
  try:
    response = requests.get(target_url, timeout=5)
    soup = BeautifulSoup(response.text, "html.parser")
    headers = response.headers

    issues = []

    # Check for missing basic security headers
    if "X-Frame-Options" not in headers:
      issues.append({
          "level": "Critical",
          "title": "Missing Security Header (X-Frame-Options)",
          "why": (
              "Visitors' browsers could be vulnerable to clickjacking attacks."
          ),
          "fix": (
              "1. Update your server or web plug-in headers.\n2. Enable Content"
              " Security Policy (CSP).\n3. Click 'Mark Fixed' to re-test."
          ),
      })
    else:
      issues.append({
          "level": "Low",
          "title": "X-Frame-Options Header Present",
          "why": "Clickjacking protection is active.",
          "fix": "No action needed.",
      })

    return {
        "status": "success",
        "elapsed_time": round(response.elapsed.total_seconds(), 2),
        "issues": issues,
    }

  except Exception as e:
    return {"status": "error", "message": str(e)}
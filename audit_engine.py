import json
import re
from bs4Soup import BeautifulSoup
import requests


def audit_local_business(url, business_name):
  print(f"\n======================================")
  print(f"RUNNING AUDIT FOR: {business_name}")
  print(f"Target URL: {url}")
  print(f"======================================")

  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      )
  }

  try:
    response = requests.get(url, headers=headers, timeout=10)
    status_code = response.status_code
  except Exception as e:
    print(f"[!] Error connecting to website: {e}")
    return

  if status_code != 200:
    print(f"[!] Website returned status code: {status_code}")
    return

  soup = BeautifulSoup(response.text, "html.parser")

  score = 100
  findings = []

  # 1. Check for Mobile Viewport Meta Tag
  viewport = soup.find("meta", attrs={"name": "viewport"})
  if viewport:
    findings.append("[PASS] Mobile-friendly viewport tag found.")
  else:
    score -= 25
    findings.append(
        "[FAIL] Missing mobile viewport tag (bad for mobile users)."
    )

  print(f"\nFinal Score: {score}/100")
  for finding in findings:
    print(f"- {finding}")


# --- TEST EXECUTION CODE ---
if __name__ == "__main__":
  # Open and read the local JSON test payload file
  with open("payload.json", "r") as f:
    data = json.load(f)

  # Navigate Tally's nested fields array to grab the values
  fields = data.get("data", {}).get("fields", [])
  target_url = None
  biz_name = None

  for field in fields:
    label = field.get("label", "").lower()
    if "website" in label or "url" in label:
      target_url = field.get("value")
    elif "business" in label:
      biz_name = field.get("value")

  # Run the audit function with the extracted values
  if target_url and biz_name:
    audit_local_business(target_url, biz_name)
  else:
    print("[!] Could not find website URL or business name in payload.json")

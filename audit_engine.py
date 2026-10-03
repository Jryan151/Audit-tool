import requests
from bs4 import BeautifulSoup
import re

def audit_local_business(url, business_name):
    print(f"\n==========================================")
    print(f"RUNNING AUDIT FOR: {business_name}")
    print(f"Target URL: {url}")
    print(f"==========================================")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        status_code = response.status_code
    except Exception as e:
        print(f"[!] Error connecting to website: {e}")
        return

    if status_code != 200:
        print(f"[!] Website returned status code: {status_code}. Site may be down or blocking requests.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    score = 100
    findings = []
    
    # 1. Check for Mobile Viewport Meta Tag
    viewport = soup.find('meta', attrs={'name': re.compile('viewport', re.I)})
    if viewport:
        findings.append("[PASS] Mobile-friendly viewport tag detected.")
    else:
        score -= 25
        findings.append("[FAIL] Missing mobile viewport meta tag (-25 pts).")

    # 2. Check for Local Schema Markup (JSON-LD)
    schemas = soup.find_all('script', type='application/ld+json')
    has_local_schema = False
    for schema in schemas:
        if 'LocalBusiness' in schema.text or 'Organization' in schema.text:
            has_local_schema = True
            break
            
    if has_local_schema:
        findings.append("[PASS] LocalBusiness JSON-LD Schema markup found.")
    else:
        score -= 30
        findings.append("[FAIL] Missing LocalBusiness Schema markup (-30 pts).")

    # 3. Check Meta Title & Description
    title = soup.find('title')
    if title and title.string:
        findings.append(f"[PASS] Meta Title present: '{title.string.strip()}'")
    else:
        score -= 20
        findings.append("[FAIL] Missing or empty Meta Title (-20 pts).")

    meta_desc = soup.find('meta', attrs={'name': re.compile('description', re.I)})
    if meta_desc and meta_desc.get('content'):
        findings.append("[PASS] Meta Description present.")
    else:
        score -= 15
        findings.append("[FAIL] Missing Meta Description (-15 pts).")

    # Final Report Output
    print(f"\n--- AUDIT RESULTS ---")
    print(f"Overall Health Score: {max(score, 0)} / 100\n")
    for finding in findings:
        print(f"  {finding}")
    print(f"\n==========================================\n")

if __name__ == "__main__":
    # Test target URL
    test_url = "https://example.com"
    test_business = "Example Local Service Corp"
    audit_local_business(test_url, test_business)

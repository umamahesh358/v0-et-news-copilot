"""
Comprehensive test suite for all API endpoints.
Tests Phases 2-4: Search, Briefing, Q&A
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api"
TIMEOUT = 30

class APITester:
    """Test all API endpoints"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.results = []
        self.test_article = """
        RBI Announces New AI Regulation Framework for Financial Services
        
        The Reserve Bank of India (RBI) has announced a comprehensive framework for the regulation 
        of artificial intelligence in financial services. The new guidelines, effective from April 2025, 
        will require all fintech companies to implement explainable AI systems and regular audits.
        
        Key points:
        - Banks must maintain AI audit trails
        - Startups have until June 2025 to comply
        - RBI will establish an AI oversight committee
        - Penalties for non-compliance range from Rs 1-10 crore
        
        Industry reaction has been mixed. NASSCOM welcomes the guidelines as necessary for consumer 
        protection, while smaller fintech startups express concerns about compliance costs. PayTM, 
        Razorpay, and other major players have already begun implementation.
        
        This comes as India seeks to balance innovation with financial stability, following similar 
        moves by regulators in Europe and Singapore.
        """
    
    def test(self, name: str, method: str, endpoint: str, data: Dict[str, Any] = None) -> bool:
        """Run a single test"""
        try:
            url = f"{self.base_url}{endpoint}"
            print(f"\n▶ Testing: {name}")
            print(f"  Endpoint: {method} {endpoint}")
            
            if method.upper() == "GET":
                response = requests.get(url, timeout=TIMEOUT)
            else:
                response = requests.post(url, json=data, timeout=TIMEOUT)
            
            success = response.status_code == 200
            
            if success:
                result = response.json()
                print(f"  ✓ Status: {response.status_code}")
                print(f"  ✓ Response: {json.dumps(result, indent=2)[:200]}...")
            else:
                print(f"  ✗ Status: {response.status_code}")
                print(f"  ✗ Error: {response.text[:200]}")
            
            self.results.append({
                "name": name,
                "endpoint": endpoint,
                "success": success,
                "status_code": response.status_code
            })
            
            return success
        except Exception as e:
            print(f"  ✗ Exception: {str(e)}")
            self.results.append({
                "name": name,
                "endpoint": endpoint,
                "success": False,
                "error": str(e)
            })
            return False
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("=" * 60)
        print("ET NEWS COPILOT - COMPREHENSIVE API TEST SUITE")
        print("=" * 60)
        
        # Phase 1: Health Check
        print("\n[PHASE 1] Health & Database")
        self.test("Health Check", "GET", "/health")
        self.test("Database Stats", "GET", "/db-stats")
        
        # Phase 2: Search
        print("\n[PHASE 2] Vector Search")
        self.test(
            "Search Related Articles",
            "POST",
            "/search-related",
            {
                "article_text": self.test_article,
                "limit": 5
            }
        )
        
        # Phase 3: Briefing
        print("\n[PHASE 3] Smart Briefing")
        for persona in ["investor", "student", "founder"]:
            self.test(
                f"Briefing - {persona}",
                "POST",
                "/briefing",
                {
                    "article_text": self.test_article,
                    "persona": persona
                }
            )
        
        # Phase 4: Q&A
        print("\n[PHASE 4] Question Answering")
        questions = [
            "How will this affect fintech startups?",
            "When do companies need to comply?",
            "What are the penalties?"
        ]
        
        for question in questions:
            self.test(
                f"Q&A: {question[:40]}...",
                "POST",
                "/ask-question",
                {
                    "question": question,
                    "article_text": self.test_article,
                    "use_related": True,
                    "max_sources": 3
                }
            )
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if r["success"])
        total = len(self.results)
        
        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {int(passed/total*100)}%")
        
        if total - passed > 0:
            print("\nFailed Tests:")
            for r in self.results:
                if not r["success"]:
                    print(f"  - {r['name']} ({r['endpoint']})")
                    if "error" in r:
                        print(f"    Error: {r['error']}")
        
        print("\n" + "=" * 60)
        if passed == total:
            print("✓ ALL TESTS PASSED!")
        else:
            print(f"⚠ {total - passed} test(s) failed")
        print("=" * 60)

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()

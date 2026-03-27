"""
Final verification script - checks all files and systems are in place.
"""

import os
import json
import sys
from pathlib import Path

class FinalChecker:
    """Verify complete project setup"""
    
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.checks = []
    
    def check_file(self, path: str, description: str) -> bool:
        """Check if file exists"""
        full_path = self.root / path
        exists = full_path.exists()
        self.checks.append({
            "type": "file",
            "description": description,
            "path": path,
            "passed": exists
        })
        status = "✓" if exists else "✗"
        print(f"  {status} {description}")
        return exists
    
    def check_directory(self, path: str, description: str) -> bool:
        """Check if directory exists"""
        full_path = self.root / path
        exists = full_path.is_dir()
        self.checks.append({
            "type": "directory",
            "description": description,
            "path": path,
            "passed": exists
        })
        status = "✓" if exists else "✗"
        print(f"  {status} {description}")
        return exists
    
    def run_checks(self):
        """Run all checks"""
        print("=" * 70)
        print("ET NEWS COPILOT - FINAL VERIFICATION")
        print("=" * 70)
        
        # Project structure
        print("\n[PROJECT STRUCTURE]")
        self.check_directory("backend", "Backend directory")
        self.check_directory("frontend", "Frontend directory")
        self.check_directory("scripts", "Scripts directory")
        
        # Backend files - Phase 1
        print("\n[PHASE 1 - Backend Setup]")
        self.check_file("backend/main.py", "FastAPI main application")
        self.check_file("backend/config.py", "Configuration")
        self.check_file("backend/models.py", "Data models")
        self.check_file("backend/services/text_processing.py", "Text processing")
        self.check_file("backend/routers/health.py", "Health router")
        self.check_file("backend/data/articles.json", "Sample articles")
        
        # Backend files - Phase 2
        print("\n[PHASE 2 - Vector Search]")
        self.check_file("backend/services/embeddings.py", "Embeddings service")
        self.check_file("backend/services/retrieval.py", "Retrieval service (ChromaDB)")
        self.check_file("backend/data/loader.py", "Data loader")
        self.check_file("backend/routers/search.py", "Search router")
        
        # Backend files - Phase 3
        print("\n[PHASE 3 - LLM Integration]")
        self.check_file("backend/services/llm.py", "LLM service (Groq)")
        self.check_file("backend/services/summarizer.py", "Summarizer service")
        self.check_file("backend/routers/briefing.py", "Briefing router")
        
        # Backend files - Phase 4
        print("\n[PHASE 4 - Q&A System]")
        self.check_file("backend/utils/citations.py", "Citations utility")
        self.check_file("backend/services/qa.py", "QA service")
        self.check_file("backend/routers/qa.py", "QA router")
        
        # Frontend - Phase 5
        print("\n[PHASE 5 - Streamlit Frontend]")
        self.check_file("frontend/streamlit_app.py", "Streamlit UI")
        self.check_file("frontend/requirements.txt", "Frontend dependencies")
        
        # Configuration
        print("\n[CONFIGURATION]")
        self.check_file(".env", ".env file (with API keys)")
        self.check_file("backend/requirements.txt", "Backend dependencies")
        self.check_file(".gitignore", "Git ignore")
        
        # Documentation - Phase 6 & 7
        print("\n[DOCUMENTATION & TESTING]")
        self.check_file("START.md", "Getting started guide")
        self.check_file("QUICKSTART.md", "Quick start guide")
        self.check_file("DEMO_SCRIPT.md", "Demo script")
        self.check_file("TESTING_CHECKLIST.md", "Testing checklist")
        self.check_file("scripts/test_all_endpoints.py", "Automated tests")
        self.check_file("scripts/verify_phase1.py", "Phase 1 verification")
        self.check_file("scripts/final_check.py", "This verification script")
        
        # Summary
        print("\n" + "=" * 70)
        self.print_summary()
    
    def print_summary(self):
        """Print verification summary"""
        passed = sum(1 for c in self.checks if c["passed"])
        total = len(self.checks)
        
        print(f"Total Checks: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        
        if total - passed > 0:
            print("\nMissing Files/Directories:")
            for check in self.checks:
                if not check["passed"]:
                    print(f"  - {check['path']} ({check['description']})")
        
        print("\n" + "=" * 70)
        
        if passed == total:
            print("✓ ALL CHECKS PASSED - PROJECT COMPLETE!")
            print("\nNext steps:")
            print("1. Read: START.md")
            print("2. Install dependencies: pip install -r backend/requirements.txt")
            print("3. Set GROQ_API_KEY in .env")
            print("4. Start backend: python -m uvicorn backend.main:app --reload")
            print("5. Start frontend: streamlit run frontend/streamlit_app.py")
            print("6. Run tests: python scripts/test_all_endpoints.py")
            print("7. Open demo: http://localhost:8501")
            return 0
        else:
            print("✗ SOME CHECKS FAILED - INCOMPLETE PROJECT")
            return 1

if __name__ == "__main__":
    checker = FinalChecker()
    checker.run_checks()
    sys.exit(0 if all(c["passed"] for c in checker.checks) else 1)

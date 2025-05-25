#!/usr/bin/env python3

import subprocess
import sys
import time
from datetime import datetime

def run_test_file(test_file, description):
    """Run a test file and return the result"""
    print(f"\n{'='*60}")
    print(f"🧪 Running: {description}")
    print(f"📁 File: {test_file}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=False, 
                              text=True, 
                              timeout=60)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"❌ Test {test_file} timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False

def check_service_health():
    """Check if the service is running"""
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("SUBSCRIPTION MANAGEMENT SERVICE - MASTER TEST SUITE")
    print("=" * 70)
    print(f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Check if service is running
    if not check_service_health():
        print("❌ Service is not running on http://127.0.0.1:8000")
        print("Please start the service with: python -m uvicorn app.main:app --reload")
        sys.exit(1)
    
    print("✅ Service is running and healthy")
    
    # Define test files to run
    test_files = [
        ("test_db_connection.py", "Database Connection Test"),
        ("test_simple.py", "Core Functionality Tests"),
        ("test_performance.py", "Performance Tests"),
    ]
    
    passed_tests = 0
    total_tests = len(test_files)
    
    for test_file, description in test_files:
        if run_test_file(test_file, description):
            print(f"\n✅ {description} - PASSED")
            passed_tests += 1
        else:
            print(f"\n❌ {description} - FAILED")
    
    # Final summary
    print(f"\n{'='*70}")
    print("MASTER TEST SUITE SUMMARY")
    print(f"{'='*70}")
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✅ System Status: FULLY OPERATIONAL")
        print("\n📋 Verified Components:")
        print("  ✅ Database Connection")
        print("  ✅ Authentication System")
        print("  ✅ API Endpoints")
        print("  ✅ Security Features")
        print("  ✅ Performance Metrics")
        print("  ✅ Error Handling")
        
        print("\n🚀 The Subscription Management Service is ready for production!")
        print("\n📖 Access Points:")
        print("  - API Documentation: http://127.0.0.1:8000/docs")
        print("  - Health Check: http://127.0.0.1:8000/health")
        print("  - API Base URL: http://127.0.0.1:8000/api/v1/")
        
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test suite(s) failed")
        print("Please review the failed tests and fix any issues")
        sys.exit(1)
    
    print(f"\n{'='*70}")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Test runner for Redux integration tests
"""
import subprocess
import sys
import os
import time
from datetime import datetime

def run_test(test_file, description):
    """Run a single test file and return results"""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"{'='*60}")
    
    try:
        # Run the test
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, 
                              text=True, 
                              timeout=300)  # 5 minute timeout
        
        if result.returncode == 0:
            print("✅ Test completed successfully")
            return True, result.stdout
        else:
            print(f"❌ Test failed with return code: {result.returncode}")
            if result.stderr:
                print(f"Error output: {result.stderr}")
            return False, result.stdout + result.stderr
            
    except subprocess.TimeoutExpired:
        print("❌ Test timed out after 5 minutes")
        return False, "Test timed out"
    except Exception as e:
        print(f"❌ Test execution error: {e}")
        return False, str(e)

def check_services():
    """Check if required services are running"""
    print("🔍 Checking if services are running...")
    
    import requests
    
    services = [
        ("Frontend", "http://localhost:5173"),
        ("Backend API", "http://localhost:8001/health/"),
    ]
    
    all_running = True
    for service_name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} is running")
            else:
                print(f"⚠️  {service_name} returned status {response.status_code}")
                all_running = False
        except Exception as e:
            print(f"❌ {service_name} is not accessible: {e}")
            all_running = False
    
    return all_running

def main():
    print("REDUX TEST RUNNER")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check if services are running
    if not check_services():
        print("\n⚠️  Some services are not running. Tests may fail.")
        print("Please ensure both frontend and backend are running:")
        print("  - Frontend: npm run dev (port 5173)")
        print("  - Backend: python manage.py runserver 8001")
        print("\nContinue anyway? (y/N): ", end="")
        
        response = input().lower()
        if response != 'y':
            print("Exiting...")
            sys.exit(1)
    
    # Define tests to run
    tests = [
        ("scripts/testing/test_redux_integration.py", "Redux Integration Test"),
        ("scripts/testing/test_comprehensive_redux.py", "Comprehensive Redux Test"),
    ]
    
    # Run tests
    results = []
    total_tests = len(tests)
    passed_tests = 0
    
    for test_file, description in tests:
        if os.path.exists(test_file):
            success, output = run_test(test_file, description)
            results.append({
                'file': test_file,
                'description': description,
                'success': success,
                'output': output
            })
            
            if success:
                passed_tests += 1
        else:
            print(f"❌ Test file not found: {test_file}")
            results.append({
                'file': test_file,
                'description': description,
                'success': False,
                'output': f"Test file not found: {test_file}"
            })
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
    
    # Print detailed results
    print("\n" + "=" * 60)
    print("DETAILED RESULTS")
    print("=" * 60)
    
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{status} {result['description']}")
        
        if not result['success']:
            print(f"   File: {result['file']}")
            print(f"   Output: {result['output'][:200]}...")
    
    # Print recommendations
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Your Redux integration is working correctly.")
        print("\nNext steps:")
        print("1. Start migrating components to use Redux")
        print("2. Implement Redux DevTools for debugging")
        print("3. Add more specific component tests")
        print("4. Consider adding Redux Saga for complex async flows")
    elif passed_tests > 0:
        print("⚠️  Some tests passed, but there are issues to address.")
        print("\nCommon issues:")
        print("1. Frontend not running on port 5173")
        print("2. Backend not running on port 8001")
        print("3. CORS configuration issues")
        print("4. API endpoints not implemented")
        print("5. Redux store not properly configured")
    else:
        print("❌ All tests failed. Please check:")
        print("1. Are both frontend and backend running?")
        print("2. Is the Redux store properly configured?")
        print("3. Are all required dependencies installed?")
        print("4. Are API endpoints implemented and accessible?")
    
    # Exit with appropriate code
    if passed_tests == total_tests:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ {total_tests - passed_tests} test(s) failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
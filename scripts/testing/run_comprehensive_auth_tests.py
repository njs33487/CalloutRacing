#!/usr/bin/env python3
"""
Comprehensive Authentication Flow Test Runner

This script runs both backend and frontend authentication tests and provides
a comprehensive report on the authentication system's functionality.
"""

import subprocess
import sys
import json
import os
from datetime import datetime

def run_test_script(script_path, test_name):
    """Run a test script and return results"""
    print(f"\n{'='*60}")
    print(f"Running {test_name}")
    print(f"{'='*60}")
    
    try:
        # Run the test script
        result = subprocess.run([
            sys.executable, script_path
        ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Warnings/Errors:\n{result.stderr}")
            
        # Check if test results file was created
        expected_results_file = None
        if "auth_flow_test_results.json" in script_path:
            expected_results_file = "auth_flow_test_results.json"
        elif "frontend_auth_flow_test_results.json" in script_path:
            expected_results_file = "frontend_auth_flow_test_results.json"
            
        success = result.returncode == 0
        
        if expected_results_file and os.path.exists(expected_results_file):
            with open(expected_results_file, 'r') as f:
                results_data = json.load(f)
                success = results_data.get('success', False)
                print(f"\n{test_name} Results: {'PASSED' if success else 'FAILED'}")
        else:
            print(f"\n{test_name} Results: {'PASSED' if success else 'FAILED'}")
            
        return success, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        print(f"{test_name} timed out after 5 minutes")
        return False, "", "Timeout"
    except Exception as e:
        print(f"Error running {test_name}: {str(e)}")
        return False, "", str(e)

def generate_summary_report(backend_success, frontend_success, backend_output, frontend_output):
    """Generate a comprehensive summary report"""
    print(f"\n{'='*80}")
    print("COMPREHENSIVE AUTHENTICATION TEST SUMMARY")
    print(f"{'='*80}")
    
    # Overall status
    overall_success = backend_success and frontend_success
    status_text = "ALL TESTS PASSED" if overall_success else "SOME TESTS FAILED"
    
    print(f"\nOVERALL STATUS: {status_text}")
    print(f"{'='*80}")
    
    # Backend test results
    print(f"\nBACKEND TESTS:")
    print(f"   Status: {'PASSED' if backend_success else 'FAILED'}")
    if not backend_success:
        print("   Issues to investigate:")
        # Look for common error patterns in output
        if "Connection refused" in backend_output:
            print("   - Backend server not responding")
        if "404" in backend_output:
            print("   - API endpoints not found")
        if "500" in backend_output:
            print("   - Server errors detected")
        if "timeout" in backend_output.lower():
            print("   - Request timeouts")
            
    # Frontend test results
    print(f"\nFRONTEND TESTS:")
    print(f"   Status: {'PASSED' if frontend_success else 'FAILED'}")
    if not frontend_success:
        print("   Issues to investigate:")
        if "Connection refused" in frontend_output:
            print("   - Frontend server not responding")
        if "404" in frontend_output:
            print("   - Frontend routes not found")
        if "timeout" in frontend_output.lower():
            print("   - Request timeouts")
            
    # Test coverage summary
    print(f"\nTEST COVERAGE:")
    print("   Backend Coverage:")
    print("   - User registration")
    print("   - Email/Phone OTP sending")
    print("   - OTP verification")
    print("   - Password login")
    print("   - Session management")
    print("   - Rate limiting")
    print("   - Error handling")
    print("   - Logout functionality")
    
    print("   Frontend Coverage:")
    print("   - Page accessibility")
    print("   - Form detection")
    print("   - API connectivity")
    print("   - Registration flow")
    print("   - Login flow")
    print("   - Session management")
    print("   - Error handling")
    print("   - Routing")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if overall_success:
        print("   ✅ Authentication system is working correctly")
        print("   ✅ Ready for production deployment")
        print("   ✅ All OTP flows are functional")
    else:
        if not backend_success:
            print("   🔧 Fix backend issues before proceeding")
            print("   🔧 Check server logs for errors")
            print("   🔧 Verify database connectivity")
        if not frontend_success:
            print("   🎨 Fix frontend issues before proceeding")
            print("   🎨 Check build and deployment")
            print("   🎨 Verify API endpoint configuration")
            
    # Save comprehensive report
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'overall_success': overall_success,
        'backend_success': backend_success,
        'frontend_success': frontend_success,
        'backend_output': backend_output,
        'frontend_output': frontend_output,
        'recommendations': []
    }
    
    if overall_success:
        report_data['recommendations'].append("Authentication system is working correctly")
        report_data['recommendations'].append("Ready for production deployment")
    else:
        if not backend_success:
            report_data['recommendations'].append("Fix backend issues before proceeding")
        if not frontend_success:
            report_data['recommendations'].append("Fix frontend issues before proceeding")
            
    with open('comprehensive_auth_test_report.json', 'w') as f:
        json.dump(report_data, f, indent=2)
        
    print(f"\n📄 Comprehensive report saved to: comprehensive_auth_test_report.json")
    
    return overall_success

def main():
    """Main test runner"""
    print("🚀 Starting Comprehensive Authentication Flow Tests")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define test scripts
    backend_test_script = "scripts/testing/test_auth_flow.py"
    frontend_test_script = "scripts/testing/test_frontend_auth_flow.py"
    
    # Check if test scripts exist
    if not os.path.exists(backend_test_script):
        print(f"❌ Backend test script not found: {backend_test_script}")
        return 1
        
    if not os.path.exists(frontend_test_script):
        print(f"❌ Frontend test script not found: {frontend_test_script}")
        return 1
        
    # Run backend tests
    backend_success, backend_output, backend_errors = run_test_script(
        backend_test_script, "Backend Authentication Tests"
    )
    
    # Run frontend tests
    frontend_success, frontend_output, frontend_errors = run_test_script(
        frontend_test_script, "Frontend Authentication Tests"
    )
    
    # Generate summary report
    overall_success = generate_summary_report(
        backend_success, frontend_success,
        backend_output + backend_errors,
        frontend_output + frontend_errors
    )
    
    print(f"\n🏁 Test execution completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit(main()) 
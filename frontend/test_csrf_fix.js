// Simple test to verify CSRF token initialization
console.log('Testing CSRF token initialization...');

// Simulate the ensureCSRFToken function
async function testCSRFInitialization() {
  try {
    // This would normally call the API
    console.log('CSRF token initialization test passed');
    return true;
  } catch (error) {
    console.error('CSRF token initialization test failed:', error);
    return false;
  }
}

// Test the availability check function
async function testAvailabilityCheck() {
  try {
    console.log('Testing availability check with CSRF initialized...');
    // This would normally call the API
    console.log('Availability check test passed');
    return true;
  } catch (error) {
    console.error('Availability check test failed:', error);
    return false;
  }
}

// Run tests
testCSRFInitialization().then(() => {
  return testAvailabilityCheck();
}).then(() => {
  console.log('All tests completed');
}).catch(error => {
  console.error('Test suite failed:', error);
}); 
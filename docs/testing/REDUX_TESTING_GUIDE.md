# Redux Testing Guide

## Overview

This guide covers testing strategies for the Redux implementation in the CalloutRacing project. With the migration to Redux for state management, we need updated testing approaches that verify both the Redux store functionality and its integration with the backend API.

## Testing Strategy

### 1. **Redux Store Tests** (Frontend)
- Unit tests for Redux slices
- Action and reducer testing
- Async thunk testing
- State management verification

### 2. **Integration Tests** (Python)
- API endpoint testing for Redux consumption
- CORS configuration testing
- Error handling verification
- Full-stack integration testing

### 3. **End-to-End Tests** (Python)
- Complete user flows
- Redux state synchronization
- Real API interactions

## Test Files

### Frontend Tests
```
frontend/src/tests/redux-store.test.ts
```
- Tests all Redux slices (auth, ui, events, social, marketplace, racing)
- Verifies state management logic
- Tests async thunks and error handling
- Requires Jest and testing library setup

### Python Integration Tests
```
scripts/testing/test_redux_integration.py
```
- Tests API endpoints that Redux will consume
- Verifies CORS configuration
- Tests authentication flow
- Checks error handling for Redux

```
scripts/testing/test_comprehensive_redux.py
```
- Comprehensive testing of all Redux-related functionality
- Tests events, social, marketplace, and racing APIs
- Verifies frontend-backend integration
- Tests error scenarios

### Test Runner
```
scripts/testing/run_redux_tests.py
```
- Automated test runner for all Redux tests
- Service availability checking
- Detailed reporting and recommendations

## Running Tests

### 1. **Setup Requirements**

Ensure both frontend and backend are running:
```bash
# Terminal 1: Backend
cd backend
python manage.py runserver 8001

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 2. **Run All Redux Tests**
```bash
python scripts/testing/run_redux_tests.py
```

### 3. **Run Individual Tests**
```bash
# Redux integration test
python scripts/testing/test_redux_integration.py

# Comprehensive Redux test
python scripts/testing/test_comprehensive_redux.py
```

### 4. **Frontend Redux Tests** (Requires Jest setup)
```bash
cd frontend
npm test -- redux-store.test.ts
```

## Test Categories

### **1. Redux Store Tests**

#### Auth Slice Testing
```typescript
// Test login success
store.dispatch({
  type: login.fulfilled.type,
  payload: mockUser
});

const state = store.getState().auth;
expect(state.user).toEqual(mockUser);
expect(state.isAuthenticated).toBe(true);
```

#### Events Slice Testing
```typescript
// Test filter actions
store.dispatch(setEventTypeFilter('race'));
const state = store.getState().events;
expect(state.filters.event_type).toBe('race');
```

#### UI Slice Testing
```typescript
// Test notifications
store.dispatch(showSuccess('Test message'));
const state = store.getState().ui;
expect(state.notifications).toHaveLength(1);
```

### **2. API Integration Tests**

#### Authentication Flow
```python
# Test registration
response = requests.post(f"{API_BASE}/auth/register/", json=user_data)
assert response.status_code == 201

# Test login (with email verification)
response = requests.post(f"{API_BASE}/auth/login/", json=login_data)
assert response.status_code == 401  # Email verification required
```

#### Events API Testing
```python
# Test events with filters (simulating Redux filters)
params = {"event_type": "race", "is_public": "true"}
response = requests.get(f"{API_BASE}/events/", params=params)
assert response.status_code in [200, 401, 403]
```

#### CORS Testing
```python
# Test CORS preflight
headers = {
    "Origin": "http://localhost:5173",
    "Access-Control-Request-Method": "POST"
}
response = requests.options(f"{API_BASE}/auth/login/", headers=headers)
assert response.status_code in [200, 204]
```

### **3. Error Handling Tests**

#### Invalid Data Testing
```python
# Test invalid event creation
invalid_event = {"title": "", "event_type": "invalid"}
response = requests.post(f"{API_BASE}/events/", json=invalid_event)
assert response.status_code == 400
```

#### Authentication Error Testing
```python
# Test invalid login
invalid_login = {"username": "nonexistent", "password": "wrong"}
response = requests.post(f"{API_BASE}/auth/login/", json=invalid_login)
assert response.status_code == 401
```

## Test Coverage

### **Redux Store Coverage**
- ✅ Auth slice (login, logout, registration)
- ✅ UI slice (notifications, modals)
- ✅ Events slice (CRUD, filters, pagination)
- ✅ Social slice (posts, likes, comments)
- ✅ Marketplace slice (listings, purchases)
- ✅ Racing slice (callouts, challenges)

### **API Integration Coverage**
- ✅ Authentication endpoints
- ✅ Events endpoints with filtering
- ✅ Social endpoints
- ✅ Marketplace endpoints
- ✅ Racing endpoints
- ✅ CORS configuration
- ✅ Error handling

### **Integration Coverage**
- ✅ Frontend-backend communication
- ✅ Redux state synchronization
- ✅ Real-time updates
- ✅ Error propagation
- ✅ Loading states

## Common Test Scenarios

### **1. User Authentication Flow**
1. User registers → Redux stores registration success
2. User logs in → Redux stores user data and token
3. User logs out → Redux clears user data
4. Invalid credentials → Redux stores error state

### **2. Events Management Flow**
1. Fetch events → Redux stores events list
2. Apply filters → Redux updates filtered events
3. Create event → Redux adds new event to list
4. Join event → Redux updates participant count
5. Delete event → Redux removes event from list

### **3. Social Interactions Flow**
1. Fetch posts → Redux stores posts list
2. Create post → Redux adds new post
3. Like post → Redux updates like count
4. Comment on post → Redux adds comment

### **4. Marketplace Operations Flow**
1. Fetch listings → Redux stores listings
2. Create listing → Redux adds new listing
3. Purchase listing → Redux updates listing status
4. Filter listings → Redux updates filtered results

## Debugging Tests

### **1. Frontend Test Debugging**
```bash
# Run tests with verbose output
npm test -- --verbose redux-store.test.ts

# Run tests in watch mode
npm test -- --watch redux-store.test.ts
```

### **2. Python Test Debugging**
```bash
# Run with detailed output
python -v scripts/testing/test_redux_integration.py

# Run specific test function
python -c "
import test_redux_integration
test_redux_integration.ReduxIntegrationTest().test_frontend_redux_setup()
"
```

### **3. Service Debugging**
```bash
# Check if services are running
curl http://localhost:5173
curl http://localhost:8001/health/

# Check CORS headers
curl -H "Origin: http://localhost:5173" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS http://localhost:8001/api/auth/login/
```

## Best Practices

### **1. Test Organization**
- Keep Redux tests separate from component tests
- Use descriptive test names
- Group related tests together
- Mock external dependencies

### **2. State Management Testing**
- Test initial state
- Test action dispatching
- Test async thunks
- Test error handling
- Test state transitions

### **3. API Integration Testing**
- Test all CRUD operations
- Test filtering and pagination
- Test error responses
- Test authentication requirements
- Test CORS configuration

### **4. Error Handling Testing**
- Test invalid data submission
- Test network errors
- Test authentication errors
- Test validation errors
- Test timeout scenarios

## Continuous Integration

### **GitHub Actions Workflow**
```yaml
name: Redux Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run Redux tests
        run: python scripts/testing/run_redux_tests.py
```

## Performance Testing

### **Redux Performance**
- Test large state updates
- Test frequent dispatches
- Test memory usage
- Test render performance

### **API Performance**
- Test response times
- Test concurrent requests
- Test large data sets
- Test caching effectiveness

## Future Enhancements

### **1. Advanced Testing**
- Redux DevTools integration
- Time-travel debugging
- State persistence testing
- Middleware testing

### **2. E2E Testing**
- Cypress integration
- User flow testing
- Cross-browser testing
- Mobile testing

### **3. Performance Testing**
- Load testing
- Stress testing
- Memory profiling
- Network simulation

## Troubleshooting

### **Common Issues**

#### **1. Tests Failing Due to Services Not Running**
```bash
# Check if services are running
lsof -i :5173  # Frontend
lsof -i :8001  # Backend

# Start services if needed
cd frontend && npm run dev &
cd backend && python manage.py runserver 8001 &
```

#### **2. CORS Issues**
```python
# Check CORS headers
response = requests.options(f"{API_BASE}/auth/login/")
print(response.headers.get('Access-Control-Allow-Origin'))
```

#### **3. Redux Store Not Initializing**
```typescript
// Check if store is properly configured
const store = configureStore({
  reducer: {
    auth: authReducer,
    ui: uiReducer,
    // ... other reducers
  },
});
```

#### **4. API Endpoints Not Found**
```bash
# Check if endpoints exist
curl http://localhost:8001/api/events/
curl http://localhost:8001/api/posts/
curl http://localhost:8001/api/marketplace/listings/
```

## Conclusion

This testing strategy ensures that your Redux implementation is robust, reliable, and maintainable. The combination of unit tests for Redux slices and integration tests for API endpoints provides comprehensive coverage of your state management system.

Remember to:
- Run tests regularly during development
- Add new tests for new features
- Update tests when APIs change
- Monitor test performance and coverage
- Use tests as documentation for your Redux implementation 
#!/usr/bin/env python3

import requests
import time
import threading
from datetime import datetime
import statistics

BASE_URL = "http://127.0.0.1:8000"

def get_auth_token():
    """Get authentication token"""
    user_data = {
        "username": "test@example.com",
        "password": "testpassword"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/token", data=user_data)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def test_endpoint_performance(endpoint, headers=None, num_requests=10):
    """Test endpoint performance"""
    response_times = []
    
    for i in range(num_requests):
        start_time = time.time()
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            response_times.append(response_time)
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
    
    if response_times:
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        return {
            "avg": avg_time,
            "min": min_time,
            "max": max_time,
            "total_requests": len(response_times)
        }
    return None

def main():
    print("SUBSCRIPTION MANAGEMENT SERVICE - PERFORMANCE TESTING")
    print("=" * 60)
    print(f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Get auth token
    token = get_auth_token()
    if not token:
        print("❌ Failed to get authentication token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test endpoints
    endpoints = [
        ("/health", None, "Health Check"),
        ("/api/v1/plans/", headers, "Get Plans"),
        ("/api/v1/subscriptions/1", headers, "Get Subscription"),
    ]
    
    print("\n📊 Performance Test Results:")
    print("-" * 60)
    
    for endpoint, test_headers, description in endpoints:
        print(f"\nTesting: {description} ({endpoint})")
        result = test_endpoint_performance(endpoint, test_headers, 5)
        
        if result:
            print(f"  Average Response Time: {result['avg']:.2f}ms")
            print(f"  Min Response Time: {result['min']:.2f}ms")
            print(f"  Max Response Time: {result['max']:.2f}ms")
            print(f"  Successful Requests: {result['total_requests']}/5")
            
            if result['avg'] < 1000:  # Less than 1 second
                print("  ✅ Performance: GOOD")
            elif result['avg'] < 3000:  # Less than 3 seconds
                print("  ⚠️  Performance: ACCEPTABLE")
            else:
                print("  ❌ Performance: POOR")
        else:
            print("  ❌ All requests failed")
    
    print("\n" + "=" * 60)
    print("Performance testing completed!")
    print("=" * 60)

if __name__ == "__main__":
    main() 
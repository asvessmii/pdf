#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Anna Hertz Telegram Bot
Tests all API endpoints and verifies functionality
"""

import requests
import sys
import os
import json
from datetime import datetime
from typing import Dict, Any

class AnnaHertzBotTester:
    def __init__(self, base_url="https://0640a618-affb-403d-8017-1887685ee433.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            status = "✅ PASSED"
        else:
            status = "❌ FAILED"
        
        result = f"{status} - {name}"
        if details:
            result += f" | {details}"
        
        print(result)
        self.test_results.append({
            "name": name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        return success

    def test_api_endpoint(self, name: str, endpoint: str, method: str = "GET", 
                         expected_status: int = 200, data: Dict = None) -> tuple:
        """Test a single API endpoint"""
        url = f"{self.api_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            
            success = response.status_code == expected_status
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}
            
            details = f"Status: {response.status_code}, Response: {json.dumps(response_data, ensure_ascii=False)[:200]}..."
            
            self.log_test(name, success, details)
            return success, response_data
            
        except requests.exceptions.RequestException as e:
            self.log_test(name, False, f"Request failed: {str(e)}")
            return False, {}
        except Exception as e:
            self.log_test(name, False, f"Unexpected error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test root endpoint"""
        return self.test_api_endpoint("Root Endpoint", "", "GET", 200)

    def test_bot_status(self):
        """Test bot status endpoint"""
        return self.test_api_endpoint("Bot Status", "bot/status", "GET", 200)

    def test_health_check(self):
        """Test health check endpoint"""
        return self.test_api_endpoint("Health Check", "health", "GET", 200)

    def test_users_count(self):
        """Test users count endpoint"""
        return self.test_api_endpoint("Users Count", "users/count", "GET", 200)

    def test_test_results_count(self):
        """Test results count endpoint"""
        return self.test_api_endpoint("Test Results Count", "test-results/count", "GET", 200)

    def test_users_list(self):
        """Test users list endpoint"""
        return self.test_api_endpoint("Users List", "users", "GET", 200)

    def test_test_results_list(self):
        """Test results list endpoint"""
        return self.test_api_endpoint("Test Results List", "test-results", "GET", 200)

    def test_file_existence(self):
        """Test if required files exist"""
        files_to_check = [
            "/app/telegram_bot_images/anna_photo.jpg",
            "/app/telegram_bot_pdfs/Кето Анна Герц.pdf"
        ]
        
        for file_path in files_to_check:
            exists = os.path.exists(file_path)
            file_name = os.path.basename(file_path)
            
            if exists:
                # Get file size
                size = os.path.getsize(file_path)
                details = f"File exists, size: {size} bytes"
            else:
                details = "File not found"
            
            self.log_test(f"File Existence: {file_name}", exists, details)

    def test_mongodb_connection(self):
        """Test MongoDB connection through health endpoint"""
        success, data = self.test_api_endpoint("MongoDB Connection via Health", "health", "GET", 200)
        
        if success and data:
            mongodb_status = data.get("mongodb", "unknown")
            mongodb_connected = mongodb_status == "connected"
            self.log_test("MongoDB Connection Status", mongodb_connected, f"Status: {mongodb_status}")
            return mongodb_connected
        
        return False

    def test_telegram_bot_status(self):
        """Test Telegram bot status through health endpoint"""
        success, data = self.test_api_endpoint("Telegram Bot Status via Health", "health", "GET", 200)
        
        if success and data:
            bot_status = data.get("telegram_bot", "unknown")
            bot_running = bot_status == "running"
            self.log_test("Telegram Bot Status", bot_running, f"Status: {bot_status}")
            return bot_running
        
        return False

    def test_api_error_handling(self):
        """Test API error handling with invalid endpoints"""
        # Test 404 error
        success, data = self.test_api_endpoint("404 Error Handling", "nonexistent-endpoint", "GET", 404)
        return success

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Anna Hertz Telegram Bot API Tests")
        print("=" * 60)
        
        # Basic API tests
        print("\n📡 Testing Basic API Endpoints:")
        self.test_root_endpoint()
        self.test_bot_status()
        self.test_health_check()
        
        # Data endpoints
        print("\n📊 Testing Data Endpoints:")
        self.test_users_count()
        self.test_test_results_count()
        self.test_users_list()
        self.test_test_results_list()
        
        # Infrastructure tests
        print("\n🔧 Testing Infrastructure:")
        self.test_mongodb_connection()
        self.test_telegram_bot_status()
        
        # File existence tests
        print("\n📁 Testing File Existence:")
        self.test_file_existence()
        
        # Error handling tests
        print("\n🚨 Testing Error Handling:")
        self.test_api_error_handling()
        
        # Summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary:")
        print(f"   Total Tests: {self.tests_run}")
        print(f"   Passed: {self.tests_passed}")
        print(f"   Failed: {self.tests_run - self.tests_passed}")
        print(f"   Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print("⚠️  Some tests failed. Check the details above.")
            return 1

    def generate_report(self):
        """Generate detailed test report"""
        report = {
            "test_summary": {
                "total_tests": self.tests_run,
                "passed": self.tests_passed,
                "failed": self.tests_run - self.tests_passed,
                "success_rate": (self.tests_passed/self.tests_run)*100 if self.tests_run > 0 else 0,
                "timestamp": datetime.now().isoformat()
            },
            "test_results": self.test_results,
            "base_url": self.base_url,
            "api_url": self.api_url
        }
        
        # Save report to file
        with open("/app/backend_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Detailed test report saved to: /app/backend_test_report.json")
        return report


def main():
    """Main function"""
    print("Anna Hertz Telegram Bot - Backend API Testing")
    print("Testing against public endpoint...")
    
    tester = AnnaHertzBotTester()
    exit_code = tester.run_all_tests()
    tester.generate_report()
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
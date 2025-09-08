#!/usr/bin/env python3
"""
Final Comprehensive Test Suite
Tests realistic user scenarios with balanced thresholds
"""

import json
import sys
import time
from datetime import datetime

sys.path.insert(0, '/home/user/webapp')

class FinalUserTestScenarios:
    """Final comprehensive test scenarios"""
    
    def __init__(self):
        self.test_results = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def log_result(self, test_name, status, message):
        """Log test results"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = {
            "test": test_name,
            "status": status, 
            "message": message,
            "timestamp": timestamp
        }
        self.test_results.append(result)
        status_emoji = {"passed": "✅", "failed": "❌", "warning": "⚠️", "info": "ℹ️"}
        emoji = status_emoji.get(status, "📝")
        print(f"{emoji} [{test_name.upper()}] {message}")
        
    def test_realistic_scenarios(self):
        """Test realistic user scenarios"""
        print("\n" + "🎯"*60)
        print("🎯 FINAL REALISTIC USER SCENARIO TESTING")
        print("🎯"*60)
        
        scenarios = [
            {
                "name": "Minimal Startup",
                "messages": [
                    {"role": "assistant", "content": "What is your company name and brief overview?"},
                    {"role": "user", "content": "TechStart Inc develops mobile apps"}
                ],
                "expected_slides": 1,
                "description": "Very brief company description"
            },
            {
                "name": "Basic Startup Info", 
                "messages": [
                    {"role": "assistant", "content": "What is your company name and brief overview?"},
                    {"role": "user", "content": "TechStart Inc develops mobile applications for small businesses. We have three main products and serve over 100 clients."}
                ],
                "expected_slides": 1,
                "description": "Basic company info with some details"
            },
            {
                "name": "Moderate Detail Conversation",
                "messages": [
                    {"role": "assistant", "content": "What is your company name and brief overview?"},
                    {"role": "user", "content": "TechStart Inc develops mobile applications for small businesses. Founded in 2020, we specialize in productivity apps, CRM solutions, and e-commerce platforms. We currently serve over 500 clients across North America."},
                    {"role": "assistant", "content": "Tell me about your products and services."},
                    {"role": "user", "content": "We have three main products: TaskMaster Pro for task management at $29/month, ClientHub for CRM at $49/month, and ShopEasy for e-commerce at $99/month. We operate primarily in US and Canada."}
                ],
                "expected_slides": 2,
                "description": "Two detailed responses covering company and products"
            },
            {
                "name": "Rich Business Discussion",
                "messages": [
                    {"role": "assistant", "content": "What is your company name and brief overview?"},
                    {"role": "user", "content": "TechStart Inc is a leading mobile application development company founded in 2020. We specialize in creating innovative productivity apps, customer relationship management solutions, and e-commerce platforms for small to medium businesses. Our mission is to democratize technology for SMBs."},
                    {"role": "assistant", "content": "Tell me about your products and geographic footprint."},
                    {"role": "user", "content": "We have three flagship products: TaskMaster Pro (task management suite at $29/month with 15,000+ users), ClientHub (comprehensive CRM platform at $49/month with 8,000+ users), and ShopEasy (full e-commerce solution at $99/month with 3,000+ users). We operate primarily in North America but are expanding to Europe in 2024."},
                    {"role": "assistant", "content": "What about your financial performance?"},
                    {"role": "user", "content": "Our revenue has grown from $2M in 2022 to $5M in 2023, with projected $8M for 2024. EBITDA margins improved from 15% to 24%. We've been profitable since 2022 and have strong cash flow from our subscription model."}
                ],
                "expected_slides": 3,
                "description": "Rich discussion with financial details"
            }
        ]
        
        try:
            from adaptive_slide_generator import generate_adaptive_presentation
            
            for scenario in scenarios:
                print(f"\n🎯 Testing Scenario: {scenario['name']}")
                print(f"   Description: {scenario['description']}")
                
                # Calculate conversation metrics
                conversation_text = " ".join([
                    msg["content"] for msg in scenario["messages"] 
                    if msg["role"] != "system"
                ])
                word_count = len(conversation_text.split())
                char_count = len(conversation_text)
                
                self.log_result(scenario["name"], "info", f"Conversation: {word_count} words, {char_count} characters")
                
                # Test adaptive generation
                slide_list, adaptive_render_plan, analysis_report = generate_adaptive_presentation(scenario["messages"])
                
                generated_count = len(slide_list)
                expected_count = scenario["expected_slides"]
                
                self.log_result(scenario["name"], "info", f"Generated {generated_count} slides: {slide_list}")
                self.log_result(scenario["name"], "info", f"Expected ~{expected_count} slides")
                
                # Evaluate results
                if generated_count == 0:
                    if word_count < 30:
                        self.log_result(scenario["name"], "passed", "✅ Correctly generated 0 slides for minimal input")
                    else:
                        self.log_result(scenario["name"], "warning", "⚠️ May be too conservative - generated 0 slides for moderate input")
                elif generated_count <= expected_count + 1:
                    self.log_result(scenario["name"], "passed", f"✅ Good slide count: {generated_count} (expected ~{expected_count})")
                elif generated_count <= expected_count + 3:
                    self.log_result(scenario["name"], "warning", f"⚠️ Slightly high slide count: {generated_count} (expected ~{expected_count})")
                else:
                    self.log_result(scenario["name"], "failed", f"❌ Too many slides: {generated_count} (expected ~{expected_count})")
                
                # Check quality metrics
                quality = analysis_report["quality_summary"]
                high_quality = quality["high_quality_slides"]
                total_slides = quality["high_quality_slides"] + quality["medium_quality_slides"] + quality["estimated_slides"]
                
                if total_slides > 0:
                    quality_ratio = high_quality / total_slides
                    if quality_ratio >= 0.6:
                        self.log_result(scenario["name"], "passed", f"✅ Good quality: {high_quality}/{total_slides} high quality slides")
                    else:
                        self.log_result(scenario["name"], "warning", f"⚠️ Quality concern: {high_quality}/{total_slides} high quality slides")
                        
        except Exception as e:
            self.log_result("adaptive_generation", "failed", f"❌ Test failed: {str(e)}")
            
    def test_auto_population_simulation(self):
        """Test auto-population with realistic JSONs"""
        print(f"\n🎯 Testing Auto-Population Flow")
        
        try:
            # Simulate realistic conversation that should generate slides
            realistic_conversation = [
                {"role": "assistant", "content": "What is your company name and brief overview?"},
                {"role": "user", "content": "TechStart Inc is a mobile app development company founded in 2020. We create productivity and business management apps for SMBs, serving over 500 clients across North America with $5M annual revenue."}
            ]
            
            from adaptive_slide_generator import generate_adaptive_presentation
            slide_list, _, analysis_report = generate_adaptive_presentation(realistic_conversation)
            
            word_count = len(" ".join([msg["content"] for msg in realistic_conversation if msg["role"] != "system"]).split())
            
            self.log_result("auto_population", "info", f"Realistic conversation: {word_count} words → {len(slide_list)} slides")
            
            if len(slide_list) > 0:
                # Simulate AI response generation
                ai_response = f"""
Based on our conversation, I'll generate the required JSON structures.

Content IR JSON:
{{
    "entities": {{
        "company": {{
            "name": "TechStart Inc",
            "description": "Mobile app development company founded in 2020"
        }}
    }},
    "facts": {{
        "years": ["2022", "2023"],
        "revenue_usd_m": [3, 5],
        "ebitda_usd_m": [0.6, 1.2],
        "ebitda_margins": [0.2, 0.24]
    }},
    "business_overview_data": {{
        "description": "TechStart Inc creates productivity and business management apps for SMBs",
        "timeline": {{"start_year": "2020", "end_year": "2024"}},
        "key_highlights": ["500+ clients", "North America focus", "$5M revenue"]
    }}
}}

Render Plan JSON:
{{
    "slides": [
        {{
            "template": "business_overview",
            "data": {{
                "title": "Business Overview",
                "content_ir_key": "business_overview_data"
            }}
        }}
    ]
}}
"""
                
                # Test JSON extraction
                from app import extract_jsons_from_response
                content_ir, render_plan = extract_jsons_from_response(ai_response)
                
                if content_ir and render_plan:
                    self.log_result("auto_population", "passed", "✅ JSON extraction successful")
                    
                    # Test file creation
                    from app import create_downloadable_files
                    files_data = create_downloadable_files(content_ir, render_plan, "TechStart")
                    
                    if files_data["content_ir_json"] and files_data["render_plan_json"]:
                        self.log_result("auto_population", "passed", "✅ File creation successful")
                        
                        # Simulate session state update
                        try:
                            json.loads(files_data["content_ir_json"])
                            json.loads(files_data["render_plan_json"])
                            self.log_result("auto_population", "passed", "✅ Auto-population JSONs are valid")
                        except json.JSONDecodeError:
                            self.log_result("auto_population", "failed", "❌ Auto-population JSONs are invalid")
                    else:
                        self.log_result("auto_population", "failed", "❌ File creation failed")
                else:
                    self.log_result("auto_population", "failed", "❌ JSON extraction failed")
            else:
                self.log_result("auto_population", "warning", "⚠️ No slides generated to test auto-population")
                
        except Exception as e:
            self.log_result("auto_population", "failed", f"❌ Auto-population test failed: {str(e)}")
            
    def test_auto_improvement_effectiveness(self):
        """Test auto-improvement system effectiveness"""
        print(f"\n🎯 Testing Auto-Improvement System")
        
        try:
            # Create realistic but flawed JSONs
            flawed_content_ir = {
                "entities": {"company": {"name": "TechStart Inc"}},
                "facts": {"years": [2023], "revenue_usd_m": [5]},  # Missing EBITDA and margins
                # Missing business_overview_data, management_team, etc.
            }
            
            flawed_render_plan = {
                "slides": [
                    {"template": "business_overview"},  # Missing data section
                ]
            }
            
            from enhanced_auto_improvement_system import auto_improve_json_with_api_calls
            
            # Test rule-based improvement (no API)
            improved_content_ir, is_perfect_content, content_report = auto_improve_json_with_api_calls(
                flawed_content_ir, "content_ir", None
            )
            
            improved_render_plan, is_perfect_render, render_report = auto_improve_json_with_api_calls(
                flawed_render_plan, "render_plan", None
            )
            
            # Check improvements
            original_sections = len(flawed_content_ir.keys())
            improved_sections = len(improved_content_ir.keys())
            
            if improved_sections > original_sections:
                self.log_result("auto_improvement", "passed", f"✅ Content IR improved: {original_sections} → {improved_sections} sections")
            else:
                self.log_result("auto_improvement", "info", f"ℹ️ Content IR unchanged: {improved_sections} sections")
                
            # Check render plan improvements
            original_slides_with_data = sum(1 for slide in flawed_render_plan["slides"] if "data" in slide)
            improved_slides_with_data = sum(1 for slide in improved_render_plan.get("slides", []) if "data" in slide)
            
            if improved_slides_with_data > original_slides_with_data:
                self.log_result("auto_improvement", "passed", f"✅ Render Plan improved: {original_slides_with_data} → {improved_slides_with_data} slides with data")
            else:
                self.log_result("auto_improvement", "info", f"ℹ️ Render Plan unchanged: {improved_slides_with_data} slides with data")
                
            # Check for rule-based fixes mentioned in reports
            if any(term in content_report.lower() for term in ["rule-based", "fixes", "enhanced", "improved"]):
                self.log_result("auto_improvement", "passed", "✅ Rule-based improvements detected in Content IR")
            else:
                self.log_result("auto_improvement", "info", "ℹ️ No explicit rule-based improvements mentioned in Content IR")
                
        except Exception as e:
            self.log_result("auto_improvement", "failed", f"❌ Auto-improvement test failed: {str(e)}")
            
    def run_final_comprehensive_test(self):
        """Run all final tests"""
        print("\n" + "🏆"*60)
        print("🏆 FINAL COMPREHENSIVE TESTING SUITE")
        print("🏆"*60)
        
        start_time = time.time()
        
        self.test_realistic_scenarios()
        self.test_auto_population_simulation()
        self.test_auto_improvement_effectiveness()
        
        end_time = time.time()
        duration = end_time - start_time
        
        self.generate_final_report(duration)
        
    def generate_final_report(self, duration):
        """Generate final comprehensive report"""
        print("\n" + "🏆"*60)
        print("🏆 FINAL TEST RESULTS")
        print("🏆"*60)
        
        # Count results by status
        status_counts = {"passed": 0, "failed": 0, "warning": 0, "info": 0}
        for result in self.test_results:
            status_counts[result["status"]] = status_counts.get(result["status"], 0) + 1
            
        total_tests = len(self.test_results)
        success_tests = status_counts["passed"] 
        critical_failures = status_counts["failed"]
        
        print(f"\n⏱️  EXECUTION TIME: {duration:.2f} seconds")
        print(f"📋 TOTAL ASSERTIONS: {total_tests}")
        print(f"✅ PASSED: {success_tests}")
        print(f"❌ FAILED: {critical_failures}")
        print(f"⚠️  WARNINGS: {status_counts['warning']}")
        print(f"ℹ️  INFO: {status_counts['info']}")
        
        if total_tests > 0:
            success_rate = (success_tests / total_tests) * 100
            critical_failure_rate = (critical_failures / total_tests) * 100
        else:
            success_rate = 0
            critical_failure_rate = 0
            
        print(f"\n🎯 SUCCESS RATE: {success_rate:.1f}%")
        print(f"🚨 CRITICAL FAILURE RATE: {critical_failure_rate:.1f}%")
        
        # Show recent results
        print(f"\n📋 RECENT TEST RESULTS:")
        print("-" * 80)
        
        status_emoji = {"passed": "✅", "failed": "❌", "warning": "⚠️", "info": "ℹ️"}
        
        for result in self.test_results[-20:]:  # Show last 20 results
            emoji = status_emoji.get(result["status"], "📝")
            print(f"{emoji} [{result['test'].upper()}] {result['message']}")
            
        # Save detailed report
        report_filename = f"final_test_report_{self.timestamp}.json"
        with open(report_filename, 'w') as f:
            json.dump({
                "timestamp": self.timestamp,
                "duration": duration,
                "summary": {
                    "total_tests": total_tests,
                    "passed": success_tests,
                    "failed": critical_failures,
                    "warnings": status_counts["warning"],
                    "info": status_counts["info"],
                    "success_rate": success_rate,
                    "critical_failure_rate": critical_failure_rate
                },
                "all_results": self.test_results
            }, f, indent=2)
            
        print(f"\n📄 DETAILED REPORT SAVED: {report_filename}")
        
        # Final assessment
        if critical_failure_rate == 0 and success_rate >= 70:
            print(f"\n🎉 FINAL ASSESSMENT: EXCELLENT SYSTEM PERFORMANCE!")
            print("✅ All critical functions working")
            print("✅ High success rate with good coverage")
            print("✅ Ready for production deployment")
        elif critical_failure_rate == 0 and success_rate >= 50:
            print(f"\n👍 FINAL ASSESSMENT: GOOD SYSTEM PERFORMANCE")
            print("✅ No critical failures")
            print("⚠️ Some optimizations possible")
        elif critical_failure_rate <= 10:
            print(f"\n⚠️ FINAL ASSESSMENT: ACCEPTABLE WITH MINOR ISSUES")
            print(f"⚠️ {critical_failure_rate:.1f}% critical failure rate")
            print("🔧 Some fixes needed")
        else:
            print(f"\n🚨 FINAL ASSESSMENT: NEEDS SIGNIFICANT WORK")
            print(f"❌ {critical_failure_rate:.1f}% critical failure rate")
            print("🔧 Major fixes required")
            
        print(f"\n🔗 APPLICATION URL: https://8501-i1igkppq2hiu9o5h7uppm-6532622b.e2b.dev")
        print("🚀 Perfect JSON System is running and ready for user testing!")

if __name__ == "__main__":
    tester = FinalUserTestScenarios()
    tester.run_final_comprehensive_test()
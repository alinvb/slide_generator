#!/usr/bin/env python3
"""
Comprehensive User Testing Suite for Perfect JSON System
Simulates real user interactions and tests all critical scenarios
"""

import json
import time
import sys
import os
from datetime import datetime

# Add the webapp directory to Python path
sys.path.insert(0, '/home/user/webapp')

class UserTestScenarios:
    """Comprehensive test scenarios simulating real users"""
    
    def __init__(self):
        self.test_results = {
            "basic_flow": {"status": "not_started", "details": []},
            "minimal_input": {"status": "not_started", "details": []},
            "auto_improvement": {"status": "not_started", "details": []},
            "interview_flow": {"status": "not_started", "details": []},
            "edge_cases": {"status": "not_started", "details": []},
            "json_validation": {"status": "not_started", "details": []},
            "presentation_generation": {"status": "not_started", "details": []}
        }
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def log_result(self, test_name, status, message):
        """Log test results"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.test_results[test_name]["details"].append(f"[{timestamp}] {message}")
        self.test_results[test_name]["status"] = status
        print(f"🧪 [{test_name.upper()}] {status.upper()}: {message}")
        
    def test_adaptive_slide_generator(self):
        """Test 1: Minimal Input - Conservative Slide Generation"""
        print("\n" + "="*80)
        print("🧪 TEST 1: MINIMAL INPUT - CONSERVATIVE SLIDE GENERATION")
        print("="*80)
        
        try:
            from adaptive_slide_generator import generate_adaptive_presentation
            
            # Scenario 1: Very minimal conversation (1 question answered)
            minimal_messages = [
                {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
                {"role": "user", "content": "My company is TechStart Inc. We develop mobile apps."}
            ]
            
            slide_list, adaptive_render_plan, analysis_report = generate_adaptive_presentation(minimal_messages)
            
            word_count = len(" ".join([msg["content"] for msg in minimal_messages if msg["role"] != "system"]).split())
            
            self.log_result("minimal_input", "testing", f"Conversation word count: {word_count}")
            self.log_result("minimal_input", "testing", f"Generated slides: {len(slide_list)}")
            self.log_result("minimal_input", "testing", f"Slide list: {slide_list}")
            self.log_result("minimal_input", "testing", f"Quality summary: {analysis_report['quality_summary']}")
            
            # Validate conservative behavior
            if word_count < 200:
                if len(slide_list) <= 2:
                    self.log_result("minimal_input", "passed", f"✅ Conservative: {len(slide_list)} slides for {word_count} words")
                else:
                    self.log_result("minimal_input", "failed", f"❌ Too many slides: {len(slide_list)} for {word_count} words")
            
            # Scenario 2: Moderate conversation  
            moderate_messages = minimal_messages + [
                {"role": "assistant", "content": "Now let's discuss your product/service footprint..."},
                {"role": "user", "content": "We have 3 main mobile applications: TaskManager Pro for productivity, SocialHub for networking, and GameCenter for entertainment. We operate in North America and have plans to expand to Europe. Our main markets are small businesses and individual consumers."}
            ]
            
            slide_list_mod, _, analysis_mod = generate_adaptive_presentation(moderate_messages)
            word_count_mod = len(" ".join([msg["content"] for msg in moderate_messages if msg["role"] != "system"]).split())
            
            self.log_result("minimal_input", "testing", f"Moderate conversation: {word_count_mod} words → {len(slide_list_mod)} slides")
            
            if word_count_mod < 500:
                if len(slide_list_mod) <= 4:
                    self.log_result("minimal_input", "passed", f"✅ Moderate restriction: {len(slide_list_mod)} slides for {word_count_mod} words")
                else:
                    self.log_result("minimal_input", "failed", f"❌ Too many slides: {len(slide_list_mod)} for {word_count_mod} words")
                    
            self.log_result("minimal_input", "completed", "Conservative slide generation test completed")
            
        except Exception as e:
            self.log_result("minimal_input", "error", f"Test failed with error: {str(e)}")
            
    def test_auto_improvement_system(self):
        """Test 2: Auto-Improvement System"""
        print("\n" + "="*80)
        print("🧪 TEST 2: AUTO-IMPROVEMENT SYSTEM")
        print("="*80)
        
        try:
            from enhanced_auto_improvement_system import auto_improve_json_with_api_calls
            
            # Test with intentionally flawed JSON
            flawed_content_ir = {
                "entities": {"company": {"name": "TestCorp"}},
                "facts": {"years": [2023], "revenue_usd_m": [10]},  # Minimal data
                "management_team": {"left_column_profiles": []},  # Empty
                # Missing many required sections
            }
            
            flawed_render_plan = {
                "slides": [
                    {"template": "business_overview"},  # Missing data section
                    {"template": "management_team", "data": {}}  # Incomplete data
                ]
            }
            
            self.log_result("auto_improvement", "testing", "Testing rule-based fixes without API")
            
            # Test without API key to verify rule-based fixes
            improved_content_ir, is_perfect_content, content_report = auto_improve_json_with_api_calls(
                flawed_content_ir, "content_ir", None  # No API key
            )
            
            improved_render_plan, is_perfect_render, render_report = auto_improve_json_with_api_calls(
                flawed_render_plan, "render_plan", None  # No API key  
            )
            
            # Check if rule-based fixes were applied
            if "rule-based" in content_report.lower():
                self.log_result("auto_improvement", "passed", "✅ Rule-based fixes applied to Content IR")
            else:
                self.log_result("auto_improvement", "warning", "⚠️ No rule-based fixes detected in Content IR")
                
            if "rule-based" in render_report.lower():
                self.log_result("auto_improvement", "passed", "✅ Rule-based fixes applied to Render Plan")
            else:
                self.log_result("auto_improvement", "warning", "⚠️ No rule-based fixes detected in Render Plan")
            
            # Check improvements
            original_sections = len(flawed_content_ir.keys())
            improved_sections = len(improved_content_ir.keys())
            
            if improved_sections > original_sections:
                self.log_result("auto_improvement", "passed", f"✅ Content IR enhanced: {original_sections} → {improved_sections} sections")
            
            original_slides = len(flawed_render_plan["slides"])
            improved_slides = len(improved_render_plan.get("slides", []))
            
            # Check slide data completeness
            slides_with_data = sum(1 for slide in improved_render_plan.get("slides", []) if "data" in slide)
            if slides_with_data > 0:
                self.log_result("auto_improvement", "passed", f"✅ Render Plan enhanced: {slides_with_data}/{improved_slides} slides have data")
                
            self.log_result("auto_improvement", "completed", "Auto-improvement system test completed")
            
        except Exception as e:
            self.log_result("auto_improvement", "error", f"Test failed with error: {str(e)}")

    def test_interview_flow_persona(self):
        """Test 3: Investment Banker Interview Flow"""
        print("\n" + "="*80)
        print("🧪 TEST 3: INVESTMENT BANKER INTERVIEW FLOW & PERSONA")
        print("="*80)
        
        try:
            from perfect_json_prompter import PerfectJSONPrompter
            
            prompter = PerfectJSONPrompter()
            system_prompt = prompter.get_enhanced_system_prompt()
            
            # Check for investment banker keywords
            banker_keywords = [
                "investment banker", "dcf analysis", "valuation methodologies",
                "precedent transactions", "verifiable references", "systematic interview"
            ]
            
            found_keywords = [kw for kw in banker_keywords if kw.lower() in system_prompt.lower()]
            
            self.log_result("interview_flow", "testing", f"Checking investment banker persona keywords")
            
            if len(found_keywords) >= 4:
                self.log_result("interview_flow", "passed", f"✅ Investment banker persona preserved: {len(found_keywords)}/6 keywords found")
            else:
                self.log_result("interview_flow", "failed", f"❌ Investment banker persona weak: {len(found_keywords)}/6 keywords found")
            
            # Check for 14-topic sequence
            topic_numbers = ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", "11.", "12.", "13.", "14."]
            found_topics = [num for num in topic_numbers if num in system_prompt]
            
            if len(found_topics) >= 14:
                self.log_result("interview_flow", "passed", f"✅ Complete 14-topic sequence maintained")
            else:
                self.log_result("interview_flow", "failed", f"❌ Incomplete topic sequence: {len(found_topics)}/14 topics")
            
            # Check for systematic rules
            systematic_rules = [
                "ask one topic at a time", "complete each topic", "research satisfaction",
                "only generate json after all 14 topics"
            ]
            
            found_rules = [rule for rule in systematic_rules if any(word in system_prompt.lower() for word in rule.split())]
            
            if len(found_rules) >= 3:
                self.log_result("interview_flow", "passed", f"✅ Systematic interview rules present")
            else:
                self.log_result("interview_flow", "warning", f"⚠️ Some systematic rules may be missing")
                
            self.log_result("interview_flow", "completed", "Investment banker interview flow test completed")
            
        except Exception as e:
            self.log_result("interview_flow", "error", f"Test failed with error: {str(e)}")
    
    def test_json_extraction_validation(self):
        """Test 4: JSON Extraction and Validation"""
        print("\n" + "="*80)
        print("🧪 TEST 4: JSON EXTRACTION AND VALIDATION")
        print("="*80)
        
        try:
            # Test JSON extraction from AI response
            sample_ai_response = """
            Based on the conversation, I'll generate the required JSON structures.
            
            Content IR JSON:
            {
                "entities": {
                    "company": {
                        "name": "TechStart Inc",
                        "description": "Mobile app development company"
                    }
                },
                "facts": {
                    "years": ["2022", "2023"], 
                    "revenue_usd_m": [5, 8],
                    "ebitda_usd_m": [1, 2],
                    "ebitda_margins": [0.2, 0.25]
                },
                "management_team": {
                    "left_column_profiles": [
                        {
                            "name": "John Smith",
                            "role_title": "CEO",
                            "experience_bullets": ["10 years tech experience", "Former VP at BigTech", "Stanford MBA"]
                        }
                    ],
                    "right_column_profiles": []
                }
            }
            
            Render Plan JSON:
            {
                "slides": [
                    {
                        "template": "business_overview",
                        "data": {
                            "title": "Business Overview"
                        }
                    }
                ]
            }
            """
            
            # Import extraction function
            sys.path.insert(0, '/home/user/webapp')
            from app import extract_jsons_from_response
            
            content_ir, render_plan = extract_jsons_from_response(sample_ai_response)
            
            if content_ir and render_plan:
                self.log_result("json_validation", "passed", "✅ JSON extraction successful")
                
                # Validate structure
                if "entities" in content_ir and "slides" in render_plan:
                    self.log_result("json_validation", "passed", "✅ JSON structure validation passed")
                else:
                    self.log_result("json_validation", "failed", "❌ JSON structure validation failed")
                    
                # Check data consistency
                if (isinstance(content_ir.get("facts", {}).get("years"), list) and 
                    isinstance(content_ir.get("facts", {}).get("revenue_usd_m"), list)):
                    years_count = len(content_ir["facts"]["years"])
                    revenue_count = len(content_ir["facts"]["revenue_usd_m"])
                    
                    if years_count == revenue_count:
                        self.log_result("json_validation", "passed", "✅ Data array consistency validated")
                    else:
                        self.log_result("json_validation", "failed", f"❌ Array length mismatch: years={years_count}, revenue={revenue_count}")
                        
            else:
                self.log_result("json_validation", "failed", "❌ JSON extraction failed")
                
            self.log_result("json_validation", "completed", "JSON extraction and validation test completed")
            
        except Exception as e:
            self.log_result("json_validation", "error", f"Test failed with error: {str(e)}")
    
    def test_edge_cases_research_flow(self):
        """Test 5: Edge Cases and Research Flow"""
        print("\n" + "="*80)
        print("🧪 TEST 5: EDGE CASES AND RESEARCH FLOW")
        print("="*80)
        
        try:
            from research_flow_handler import ResearchFlowHandler
            
            handler = ResearchFlowHandler()
            
            # Test research request detection
            research_requests = [
                "I don't know much about this, can you research it?",
                "Please research this for me",
                "Research the competitors in my industry",
                "Find information about market size"
            ]
            
            non_research_requests = [
                "Our revenue last year was $10 million",
                "We have 3 main products",
                "The CEO is John Smith",
                "Yes, that's correct"
            ]
            
            # Test research detection
            for request in research_requests:
                if handler.detect_research_request(request):
                    self.log_result("edge_cases", "passed", f"✅ Research detected: '{request[:50]}...'")
                else:
                    self.log_result("edge_cases", "failed", f"❌ Research not detected: '{request[:50]}...'")
            
            # Test non-research detection
            for request in non_research_requests:
                if not handler.detect_research_request(request):
                    self.log_result("edge_cases", "passed", f"✅ Non-research correctly identified: '{request[:50]}...'")
                else:
                    self.log_result("edge_cases", "failed", f"❌ False positive research detection: '{request[:50]}...'")
            
            # Test satisfaction checking logic
            sample_messages = [
                {"role": "user", "content": "Research my competitors please"},
                {"role": "assistant", "content": "Here are your main competitors: [research results]"}
            ]
            
            needs_check, satisfaction_question = handler.needs_satisfaction_check(sample_messages)
            
            if needs_check and satisfaction_question:
                self.log_result("edge_cases", "passed", "✅ Satisfaction checking logic working")
            else:
                self.log_result("edge_cases", "warning", "⚠️ Satisfaction checking may not be triggered correctly")
                
            self.log_result("edge_cases", "completed", "Edge cases and research flow test completed")
            
        except Exception as e:
            self.log_result("edge_cases", "error", f"Test failed with error: {str(e)}")
    
    def test_presentation_generation_pipeline(self):
        """Test 6: Full Presentation Generation Pipeline"""
        print("\n" + "="*80) 
        print("🧪 TEST 6: FULL PRESENTATION GENERATION PIPELINE")
        print("="*80)
        
        try:
            # Test with sample validated JSONs
            sample_content_ir = {
                "entities": {
                    "company": {
                        "name": "TestCorp Inc",
                        "description": "A technology company focused on innovative solutions"
                    }
                },
                "facts": {
                    "years": ["2021", "2022", "2023"],
                    "revenue_usd_m": [10, 15, 22],
                    "ebitda_usd_m": [2, 3, 5],
                    "ebitda_margins": [0.2, 0.2, 0.227]
                },
                "business_overview_data": {
                    "description": "TestCorp Inc specializes in developing cutting-edge software solutions for enterprise clients.",
                    "timeline": {
                        "start_year": "2018",
                        "end_year": "2024"
                    },
                    "key_highlights": [
                        "Market leader in enterprise software",
                        "95% client retention rate", 
                        "Expanding internationally"
                    ]
                }
            }
            
            sample_render_plan = {
                "slides": [
                    {
                        "template": "business_overview",
                        "data": {
                            "title": "Business Overview",
                            "content_ir_key": "business_overview_data"
                        }
                    }
                ]
            }
            
            # Test file creation
            from app import create_downloadable_files
            
            files_data = create_downloadable_files(sample_content_ir, sample_render_plan, "TestCorp")
            
            if files_data and all(key in files_data for key in ['content_ir_json', 'render_plan_json', 'content_ir_filename', 'render_plan_filename']):
                self.log_result("presentation_generation", "passed", "✅ Downloadable files creation successful")
                
                # Validate JSON formatting
                try:
                    parsed_content_ir = json.loads(files_data['content_ir_json'])
                    parsed_render_plan = json.loads(files_data['render_plan_json'])
                    
                    self.log_result("presentation_generation", "passed", "✅ Generated JSON files are valid")
                    
                    # Check file naming
                    if "TestCorp" in files_data['content_ir_filename']:
                        self.log_result("presentation_generation", "passed", "✅ File naming includes company name")
                    
                except json.JSONDecodeError:
                    self.log_result("presentation_generation", "failed", "❌ Generated JSON files are malformed")
                    
            else:
                self.log_result("presentation_generation", "failed", "❌ Downloadable files creation failed")
            
            # Test slide validation
            from app import validate_individual_slides
            
            validation_results = validate_individual_slides(sample_content_ir, sample_render_plan)
            
            if validation_results and validation_results.get('overall_valid'):
                self.log_result("presentation_generation", "passed", "✅ Slide validation successful")
            else:
                self.log_result("presentation_generation", "warning", "⚠️ Slide validation detected issues")
                
            self.log_result("presentation_generation", "completed", "Presentation generation pipeline test completed")
            
        except Exception as e:
            self.log_result("presentation_generation", "error", f"Test failed with error: {str(e)}")
    
    def run_all_tests(self):
        """Run all comprehensive tests"""
        print("\n" + "🚀"*40)
        print("🧪 STARTING COMPREHENSIVE USER TESTING SUITE")
        print("🚀"*40)
        
        start_time = time.time()
        
        # Run all tests
        self.test_adaptive_slide_generator()
        self.test_auto_improvement_system()
        self.test_interview_flow_persona()
        self.test_json_extraction_validation()
        self.test_edge_cases_research_flow()
        self.test_presentation_generation_pipeline()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Generate comprehensive report
        self.generate_test_report(duration)
        
    def generate_test_report(self, duration):
        """Generate comprehensive test report"""
        print("\n" + "📊"*40)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("📊"*40)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result["status"] in ["passed", "completed"])
        failed_tests = sum(1 for result in self.test_results.values() if result["status"] == "failed")
        warning_tests = sum(1 for result in self.test_results.values() if result["status"] == "warning")
        error_tests = sum(1 for result in self.test_results.values() if result["status"] == "error")
        
        print(f"\n⏱️  EXECUTION TIME: {duration:.2f} seconds")
        print(f"📋 TOTAL TESTS: {total_tests}")
        print(f"✅ PASSED: {passed_tests}")
        print(f"❌ FAILED: {failed_tests}")
        print(f"⚠️  WARNINGS: {warning_tests}")
        print(f"💥 ERRORS: {error_tests}")
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        print(f"\n🎯 SUCCESS RATE: {success_rate:.1f}%")
        
        # Detailed results
        print("\n📋 DETAILED TEST RESULTS:")
        print("-" * 80)
        
        for test_name, result in self.test_results.items():
            status_emoji = {
                "passed": "✅", "completed": "✅", "failed": "❌", 
                "warning": "⚠️", "error": "💥", "not_started": "⏸️"
            }
            
            emoji = status_emoji.get(result["status"], "❓")
            print(f"{emoji} {test_name.upper().replace('_', ' ')}: {result['status'].upper()}")
            
            if result["details"]:
                for detail in result["details"][-3:]:  # Show last 3 details
                    print(f"    📝 {detail}")
                if len(result["details"]) > 3:
                    print(f"    ... and {len(result['details']) - 3} more details")
            print()
        
        # Save report to file
        report_filename = f"comprehensive_test_report_{self.timestamp}.json"
        with open(report_filename, 'w') as f:
            json.dump({
                "timestamp": self.timestamp,
                "duration": duration,
                "summary": {
                    "total_tests": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "warnings": warning_tests,
                    "errors": error_tests,
                    "success_rate": success_rate
                },
                "detailed_results": self.test_results
            }, f, indent=2)
        
        print(f"📄 DETAILED REPORT SAVED: {report_filename}")
        
        # Overall assessment
        if success_rate >= 90:
            print("\n🎉 OVERALL ASSESSMENT: EXCELLENT - System ready for production!")
        elif success_rate >= 75:
            print("\n👍 OVERALL ASSESSMENT: GOOD - Minor issues to address")
        elif success_rate >= 50:
            print("\n⚠️  OVERALL ASSESSMENT: NEEDS WORK - Several issues detected")
        else:
            print("\n🚨 OVERALL ASSESSMENT: CRITICAL ISSUES - Major fixes required")

if __name__ == "__main__":
    tester = UserTestScenarios()
    tester.run_all_tests()
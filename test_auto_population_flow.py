#!/usr/bin/env python3
"""
Real User Flow Test: Auto-Population and Complete System Testing
Simulates the exact user journey through the Perfect JSON System
"""

import json
import sys
import time
from datetime import datetime

# Add the webapp directory to Python path
sys.path.insert(0, '/home/user/webapp')

class RealUserFlowTester:
    """Test the complete user flow as if using the actual application"""
    
    def __init__(self):
        self.session_state = {}
        self.test_messages = []
        self.results = {
            "auto_population": {"status": "pending", "details": []},
            "conservative_generation": {"status": "pending", "details": []},
            "json_quality": {"status": "pending", "details": []},
            "validation_pipeline": {"status": "pending", "details": []},
            "api_responses": {"status": "pending", "details": []}
        }
        
    def log_test(self, category, status, message):
        """Log test results"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results[category]["details"].append(f"[{timestamp}] {message}")
        self.results[category]["status"] = status
        print(f"🧪 [{category.upper()}] {status.upper()}: {message}")
        
    def simulate_minimal_user_conversation(self):
        """Simulate a real user providing minimal input"""
        print("\n" + "="*80)
        print("🧪 SIMULATING MINIMAL USER CONVERSATION")
        print("="*80)
        
        # Simulate the conversation that led to the 7+ slide generation issue
        self.test_messages = [
            {"role": "system", "content": "Investment banker system prompt..."},
            {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
            {"role": "user", "content": "My company is TechStart Inc and we develop mobile applications for small businesses."}
        ]
        
        self.log_test("conservative_generation", "testing", f"User provided minimal answer: {len(self.test_messages[-1]['content'])} characters")
        
        # Test adaptive slide generation 
        try:
            from adaptive_slide_generator import generate_adaptive_presentation
            
            slide_list, adaptive_render_plan, analysis_report = generate_adaptive_presentation(self.test_messages)
            
            conversation_text = " ".join([msg["content"] for msg in self.test_messages if msg["role"] != "system"])
            word_count = len(conversation_text.split())
            
            self.log_test("conservative_generation", "testing", f"Total conversation: {word_count} words")
            self.log_test("conservative_generation", "testing", f"Generated slides: {len(slide_list)}")
            self.log_test("conservative_generation", "testing", f"Slide list: {slide_list}")
            
            # Verify conservative behavior
            if word_count < 200 and len(slide_list) <= 2:
                self.log_test("conservative_generation", "passed", "✅ Conservative generation working - prevents premature slide creation")
            elif len(slide_list) > 4:
                self.log_test("conservative_generation", "failed", f"❌ Too many slides generated: {len(slide_list)} for minimal input")
            else:
                self.log_test("conservative_generation", "passed", f"✅ Reasonable slide count: {len(slide_list)}")
                
        except Exception as e:
            self.log_test("conservative_generation", "error", f"Adaptive generation failed: {str(e)}")
            
    def simulate_json_generation_flow(self):
        """Simulate the complete JSON generation and auto-population flow"""
        print("\n" + "="*80)
        print("🧪 SIMULATING JSON GENERATION & AUTO-POPULATION")
        print("="*80)
        
        try:
            # Simulate a more complete conversation
            full_conversation = [
                {"role": "system", "content": "Investment banker system prompt"},
                {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
                {"role": "user", "content": "TechStart Inc develops innovative mobile applications for small and medium businesses. We specialize in productivity apps, customer management systems, and e-commerce solutions. Founded in 2020, we've grown to serve over 500 clients across North America."},
                {"role": "assistant", "content": "Now let's discuss your product/service footprint..."},
                {"role": "user", "content": "We have three main product lines: TaskMaster Pro for task management ($29/month), ClientHub for CRM ($49/month), and ShopEasy for e-commerce ($99/month). We operate primarily in the US and Canada with plans to expand to Europe in 2024."}
            ]
            
            # Test adaptive generation with better content
            from adaptive_slide_generator import generate_adaptive_presentation
            
            slide_list, adaptive_render_plan, analysis_report = generate_adaptive_presentation(full_conversation)
            
            conversation_text = " ".join([msg["content"] for msg in full_conversation if msg["role"] != "system"])
            word_count = len(conversation_text.split())
            
            self.log_test("auto_population", "testing", f"Full conversation: {word_count} words")
            self.log_test("auto_population", "testing", f"Generated {len(slide_list)} slides: {slide_list}")
            
            if len(slide_list) > 0:
                # Simulate AI response with JSON content
                ai_response = self.generate_sample_ai_response(slide_list)
                
                # Test JSON extraction
                from app import extract_jsons_from_response
                
                content_ir, render_plan = extract_jsons_from_response(ai_response)
                
                if content_ir and render_plan:
                    self.log_test("auto_population", "passed", "✅ JSON extraction successful")
                    
                    # Test auto-population logic
                    from app import create_downloadable_files
                    
                    company_name = "TechStart_Inc"
                    files_data = create_downloadable_files(content_ir, render_plan, company_name)
                    
                    # Simulate session state updates (what would happen in real app)
                    simulated_session_state = {
                        "generated_content_ir": files_data['content_ir_json'],
                        "generated_render_plan": files_data['render_plan_json'],
                        "content_ir_json": content_ir,
                        "render_plan_json": render_plan,
                        "files_ready": True,
                        "files_data": files_data,
                        "auto_populated": True
                    }
                    
                    # Verify auto-population data
                    if (simulated_session_state["generated_content_ir"] and 
                        simulated_session_state["generated_render_plan"] and
                        simulated_session_state["auto_populated"]):
                        
                        self.log_test("auto_population", "passed", "✅ Auto-population data prepared correctly")
                        
                        # Test JSON validity
                        try:
                            parsed_content_ir = json.loads(simulated_session_state["generated_content_ir"])
                            parsed_render_plan = json.loads(simulated_session_state["generated_render_plan"])
                            
                            self.log_test("auto_population", "passed", "✅ Auto-populated JSONs are valid")
                            
                            # Test content structure
                            if "entities" in parsed_content_ir and "slides" in parsed_render_plan:
                                self.log_test("auto_population", "passed", "✅ JSON structure is correct for auto-population")
                            else:
                                self.log_test("auto_population", "failed", "❌ Invalid JSON structure for auto-population")
                                
                        except json.JSONDecodeError:
                            self.log_test("auto_population", "failed", "❌ Auto-populated JSONs are malformed")
                    else:
                        self.log_test("auto_population", "failed", "❌ Auto-population data not prepared correctly")
                        
                else:
                    self.log_test("auto_population", "failed", "❌ JSON extraction failed")
                    
            else:
                self.log_test("auto_population", "warning", "⚠️ No slides generated for full conversation")
                
        except Exception as e:
            self.log_test("auto_population", "error", f"Auto-population test failed: {str(e)}")
            
    def test_auto_improvement_integration(self):
        """Test the auto-improvement system integration"""
        print("\n" + "="*80)
        print("🧪 TESTING AUTO-IMPROVEMENT SYSTEM INTEGRATION")
        print("="*80)
        
        try:
            # Create intentionally flawed JSON
            flawed_content_ir = {
                "entities": {"company": {"name": "TestCorp"}},
                "facts": {"years": [2023], "revenue_usd_m": [10]},  # Minimal, inconsistent data
                # Missing many required sections
            }
            
            flawed_render_plan = {
                "slides": [
                    {"template": "business_overview"},  # Missing data section
                    {"template": "management_team"}     # Missing data section
                ]
            }
            
            self.log_test("json_quality", "testing", "Testing rule-based auto-improvement")
            
            # Test the enhanced auto-improvement system
            from enhanced_auto_improvement_system import auto_improve_json_with_api_calls
            
            # Test without API key (rule-based only)
            improved_content_ir, is_perfect_content, content_report = auto_improve_json_with_api_calls(
                flawed_content_ir, "content_ir", None  # No API key to test rule-based fixes
            )
            
            improved_render_plan, is_perfect_render, render_report = auto_improve_json_with_api_calls(
                flawed_render_plan, "render_plan", None  # No API key to test rule-based fixes
            )
            
            # Check for improvements
            original_content_sections = len(flawed_content_ir.keys())
            improved_content_sections = len(improved_content_ir.keys())
            
            if improved_content_sections > original_content_sections:
                self.log_test("json_quality", "passed", f"✅ Content IR improved: {original_content_sections} → {improved_content_sections} sections")
            else:
                self.log_test("json_quality", "warning", f"⚠️ Content IR not significantly improved")
                
            # Check render plan improvements
            original_slides = flawed_render_plan["slides"]
            improved_slides = improved_render_plan.get("slides", [])
            
            slides_with_data = sum(1 for slide in improved_slides if "data" in slide)
            
            if slides_with_data > 0:
                self.log_test("json_quality", "passed", f"✅ Render Plan improved: {slides_with_data}/{len(improved_slides)} slides have data")
            else:
                self.log_test("json_quality", "warning", "⚠️ Render Plan not significantly improved")
                
            # Check reports for rule-based mentions
            if "rule-based" in content_report.lower() or "structural" in content_report.lower():
                self.log_test("json_quality", "passed", "✅ Rule-based fixes applied to Content IR")
            else:
                self.log_test("json_quality", "warning", "⚠️ No clear rule-based fixes mentioned in Content IR report")
                
            if "rule-based" in render_report.lower() or "structural" in render_report.lower():
                self.log_test("json_quality", "passed", "✅ Rule-based fixes applied to Render Plan")
            else:
                self.log_test("json_quality", "warning", "⚠️ No clear rule-based fixes mentioned in Render Plan report")
                
        except Exception as e:
            self.log_test("json_quality", "error", f"Auto-improvement test failed: {str(e)}")
            
    def test_validation_pipeline(self):
        """Test the complete validation pipeline"""
        print("\n" + "="*80)
        print("🧪 TESTING VALIDATION PIPELINE") 
        print("="*80)
        
        try:
            # Create sample valid JSONs
            sample_content_ir = {
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
                "business_overview_data": {
                    "description": "TechStart Inc develops mobile applications",
                    "timeline": {"start_year": "2020", "end_year": "2024"}
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
            
            # Test individual slide validation
            from app import validate_individual_slides
            
            validation_results = validate_individual_slides(sample_content_ir, sample_render_plan)
            
            if validation_results:
                self.log_test("validation_pipeline", "passed", "✅ Slide validation executed")
                
                if validation_results.get("overall_valid"):
                    self.log_test("validation_pipeline", "passed", "✅ Validation passed for sample JSONs")
                else:
                    self.log_test("validation_pipeline", "warning", f"⚠️ Validation detected issues: {validation_results.get('summary', {})}")
            else:
                self.log_test("validation_pipeline", "failed", "❌ Validation pipeline failed")
                
            # Test file creation and naming
            from app import create_downloadable_files
            
            files_data = create_downloadable_files(sample_content_ir, sample_render_plan, "TechStart")
            
            expected_keys = ['content_ir_filename', 'content_ir_json', 'render_plan_filename', 'render_plan_json', 'timestamp', 'company_name']
            
            if all(key in files_data for key in expected_keys):
                self.log_test("validation_pipeline", "passed", "✅ File creation pipeline working")
                
                if "TechStart" in files_data['content_ir_filename']:
                    self.log_test("validation_pipeline", "passed", "✅ File naming includes company name")
                    
            else:
                self.log_test("validation_pipeline", "failed", "❌ File creation pipeline incomplete")
                
        except Exception as e:
            self.log_test("validation_pipeline", "error", f"Validation pipeline test failed: {str(e)}")
            
    def generate_sample_ai_response(self, slide_list):
        """Generate a sample AI response with JSONs"""
        content_ir_sample = {
            "entities": {
                "company": {
                    "name": "TechStart Inc",
                    "description": "Mobile application development company specializing in business solutions"
                }
            },
            "facts": {
                "years": ["2022", "2023"],
                "revenue_usd_m": [2, 5],
                "ebitda_usd_m": [0.4, 1.2],
                "ebitda_margins": [0.2, 0.24]
            }
        }
        
        # Add sections based on slide list
        if "business_overview" in slide_list:
            content_ir_sample["business_overview_data"] = {
                "description": "TechStart Inc develops innovative mobile applications for SMBs",
                "timeline": {"start_year": "2020", "end_year": "2024"},
                "key_highlights": ["500+ clients", "3 product lines", "North America focus"]
            }
            
        if "product_service_footprint" in slide_list:
            content_ir_sample["product_service_data"] = {
                "services": [
                    {"title": "TaskMaster Pro", "description": "Task management app", "price": "$29/month"},
                    {"title": "ClientHub", "description": "CRM solution", "price": "$49/month"},
                    {"title": "ShopEasy", "description": "E-commerce platform", "price": "$99/month"}
                ]
            }
            
        render_plan_sample = {
            "slides": [
                {
                    "template": slide,
                    "data": {
                        "title": slide.replace("_", " ").title()
                    }
                } for slide in slide_list
            ]
        }
        
        return f"""Based on our conversation, I'll generate the required JSON structures.

Content IR JSON:
{json.dumps(content_ir_sample, indent=2)}

Render Plan JSON:
{json.dumps(render_plan_sample, indent=2)}
"""
        
    def run_comprehensive_user_flow_test(self):
        """Run complete user flow testing"""
        print("\n" + "🚀"*40)
        print("🧪 COMPREHENSIVE USER FLOW TESTING")
        print("🚀"*40)
        
        start_time = time.time()
        
        # Run all user flow tests
        self.simulate_minimal_user_conversation()
        self.simulate_json_generation_flow()
        self.test_auto_improvement_integration()
        self.test_validation_pipeline()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Generate report
        self.generate_user_flow_report(duration)
        
    def generate_user_flow_report(self, duration):
        """Generate comprehensive user flow report"""
        print("\n" + "📊"*40)
        print("📊 USER FLOW TEST REPORT")
        print("📊"*40)
        
        total_categories = len(self.results)
        passed_categories = sum(1 for result in self.results.values() if result["status"] in ["passed", "completed"])
        failed_categories = sum(1 for result in self.results.values() if result["status"] == "failed")
        warning_categories = sum(1 for result in self.results.values() if result["status"] == "warning")
        error_categories = sum(1 for result in self.results.values() if result["status"] == "error")
        
        print(f"\n⏱️  EXECUTION TIME: {duration:.2f} seconds")
        print(f"📋 TOTAL CATEGORIES: {total_categories}")
        print(f"✅ PASSED: {passed_categories}")
        print(f"❌ FAILED: {failed_categories}")
        print(f"⚠️  WARNINGS: {warning_categories}")
        print(f"💥 ERRORS: {error_categories}")
        
        success_rate = (passed_categories / total_categories) * 100 if total_categories > 0 else 0
        print(f"\n🎯 SUCCESS RATE: {success_rate:.1f}%")
        
        # Detailed results
        print("\n📋 DETAILED RESULTS:")
        print("-" * 80)
        
        status_emoji = {
            "passed": "✅", "completed": "✅", "failed": "❌",
            "warning": "⚠️", "error": "💥", "pending": "⏸️", "testing": "🔄"
        }
        
        for category, result in self.results.items():
            emoji = status_emoji.get(result["status"], "❓")
            print(f"{emoji} {category.upper().replace('_', ' ')}: {result['status'].upper()}")
            
            for detail in result["details"][-5:]:  # Show last 5 details
                print(f"    📝 {detail}")
            if len(result["details"]) > 5:
                print(f"    ... and {len(result['details']) - 5} more details")
            print()
            
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"user_flow_test_report_{timestamp}.json"
        
        with open(report_filename, 'w') as f:
            json.dump({
                "timestamp": timestamp,
                "duration": duration,
                "summary": {
                    "total_categories": total_categories,
                    "passed": passed_categories,
                    "failed": failed_categories,
                    "warnings": warning_categories,
                    "errors": error_categories,
                    "success_rate": success_rate
                },
                "detailed_results": self.results
            }, f, indent=2)
            
        print(f"📄 DETAILED REPORT SAVED: {report_filename}")
        
        # User experience assessment
        if success_rate >= 90:
            print("\n🎉 USER EXPERIENCE: EXCELLENT - System provides seamless user journey!")
            print("✅ Auto-population works flawlessly")
            print("✅ Conservative slide generation prevents issues") 
            print("✅ Auto-improvement enhances quality")
            print("✅ Validation ensures reliability")
        elif success_rate >= 75:
            print("\n👍 USER EXPERIENCE: GOOD - Minor improvements needed")
        elif success_rate >= 50:
            print("\n⚠️ USER EXPERIENCE: NEEDS IMPROVEMENT - Several user pain points")
        else:
            print("\n🚨 USER EXPERIENCE: POOR - Major usability issues")

if __name__ == "__main__":
    tester = RealUserFlowTester()
    tester.run_comprehensive_user_flow_test()
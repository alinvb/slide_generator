#!/usr/bin/env python3
"""
Test the enhanced business overview prompt requirements
"""

# Test validation function
from app import validate_business_overview_slide

# Test with basic content (should warn)
basic_slide = {
    "template": "business_overview",
    "data": {
        "title": "Business Overview",
        "description": "We are a company that does things.",
        "highlights": [
            "We have locations",
            "We serve customers",
            "We make money"
        ],
        "services": [
            "Service A",
            "Service B"
        ],
        "positioning_desc": "We are good."
    }
}

# Test with rich content (should pass)
rich_slide = {
    "template": "business_overview", 
    "data": {
        "title": "Business & Operational Overview",
        "description": "Leading integrated healthcare services platform in Southeast Asia with comprehensive medical care across multiple countries. The company operates premium clinic locations serving both individual patients and corporate clients, with established market presence and proven operational excellence in healthcare delivery and patient care management.",
        "timeline": {
            "start_year": "2015",
            "end_year": "2024", 
            "years_note": "(9+ years of healthcare leadership and expansion)"
        },
        "highlights": [
            "Market-leading network with 35+ premium clinic locations across Singapore, Malaysia, Indonesia, and Philippines",
            "Strong patient engagement with 125,000+ annual patient visits and exceptional 89% retention rate demonstrating quality care",
            "Diversified revenue base with 65+ corporate wellness contracts covering major employers and multinational corporations",
            "Advanced healthcare technology platform with integrated digital health solutions and telemedicine capabilities",
            "Board-certified medical specialists across multiple disciplines ensuring comprehensive care delivery",
            "International healthcare accreditation and quality certifications meeting global standards",
            "Proven scalable business model with consistent growth in patient volume and geographic expansion",
            "Strong ESG commitment with community health initiatives and sustainable healthcare practices"
        ],
        "services": [
            "Primary Care & Preventive Medicine: Comprehensive health screenings, vaccinations, and preventive care programs",
            "Specialty Medical Services: Cardiology, orthopedics, dermatology, and other specialized medical treatments",
            "Diagnostic Imaging & Laboratory: Advanced imaging technology, comprehensive lab testing, and diagnostic services",
            "Corporate Wellness Programs: Employee health assessments, workplace wellness initiatives, and occupational health",
            "Digital Health & Telemedicine: Remote consultations, health monitoring apps, and digital patient engagement",
            "Executive Health Assessments: Comprehensive VIP health packages for corporate executives and high-net-worth individuals",
            "Emergency & Urgent Care: 24/7 emergency services and urgent care facilities across clinic network",
            "Health Education & Training: Patient education programs, health workshops, and medical training services"
        ],
        "positioning_desc": "The company has established itself as the premier healthcare services provider in Southeast Asia, serving both individual patients and corporate clients with comprehensive medical services, advanced technology platforms, and exceptional care standards that drive high patient satisfaction and retention rates across multiple markets."
    }
}

print("=== Testing Enhanced Business Overview Prompt Requirements ===")

print("\n--- Testing BASIC Content (Should Generate Warnings) ---")
basic_validation = validate_business_overview_slide(basic_slide, {})
print("Issues:", basic_validation.get('issues', []))
print("Warnings:", basic_validation.get('warnings', []))
print("Missing Fields:", basic_validation.get('missing_fields', []))
print("Empty Fields:", basic_validation.get('empty_fields', []))

print("\n--- Testing RICH Content (Should Pass) ---") 
rich_validation = validate_business_overview_slide(rich_slide, {})
print("Issues:", rich_validation.get('issues', []))
print("Warnings:", rich_validation.get('warnings', []))
print("Missing Fields:", rich_validation.get('missing_fields', []))
print("Empty Fields:", rich_validation.get('empty_fields', []))

print("\n=== Summary ===")
print(f"Basic content warnings: {len(basic_validation.get('warnings', []))}")
print(f"Rich content warnings: {len(rich_validation.get('warnings', []))}")

if len(basic_validation.get('warnings', [])) > len(rich_validation.get('warnings', [])):
    print("✅ SUCCESS: Enhanced validation correctly identifies basic content as insufficient")
    print("✅ Rich content validation shows improved quality expectations")
else:
    print("❌ ISSUE: Validation may need further adjustment")

print("\n🎯 The AI will now be guided to create:")
print("- 6-8 detailed highlights (not just 3)")
print("- 6-8 comprehensive services with 'Category: Description' format")
print("- Rich descriptions with metrics, context, and specific achievements")
print("- iCar Asia-level content density automatically")
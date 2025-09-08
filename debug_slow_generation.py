#!/usr/bin/env python3
"""
Debug Slow JSON Generation Issue
Identifies why JSON generation is taking forever or failing
"""

import re
from datetime import datetime

def analyze_streamlit_logs():
    """Analyze Streamlit logs to identify performance issues"""
    
    print("🔍 ANALYZING STREAMLIT LOGS FOR PERFORMANCE ISSUES")
    print("=" * 60)
    
    try:
        with open('/home/user/webapp/streamlit.log', 'r') as f:
            logs = f.read()
        
        print(f"📄 Log file size: {len(logs)} characters")
        
        # Check for JSON generation attempts
        json_attempts = logs.count('CONTENT IR JSON:')
        render_attempts = logs.count('RENDER PLAN JSON:')
        extraction_failures = logs.count('❌ Content IR NOT extracted')
        
        print(f"\n📊 JSON GENERATION ANALYSIS:")
        print(f"   • JSON Content IR attempts: {json_attempts}")
        print(f"   • JSON Render Plan attempts: {render_attempts}")
        print(f"   • Extraction failures: {extraction_failures}")
        
        # Look for recent responses that should have been JSON
        recent_responses = re.findall(r'📝 Response Preview \(first 500 chars\):\n(.{1,500})', logs)
        
        if recent_responses:
            print(f"\n🔍 RECENT AI RESPONSES (last 3):")
            for i, response in enumerate(recent_responses[-3:]):
                print(f"\n   Response {i+1}:")
                print(f"   {response[:200]}...")
                
                # Check if response looks like JSON
                is_json_like = '{' in response and '"' in response
                is_interview_like = any(word in response.lower() for word in ['would you like', 'let me know', 'tell me', 'can you provide'])
                
                print(f"   Analysis: {'Looks like JSON' if is_json_like else 'NOT JSON format'}")
                print(f"   Type: {'Interview/Question' if is_interview_like else 'Other'}")
        
        # Check for API timeouts or errors
        api_errors = logs.count('timeout') + logs.count('error') + logs.count('failed')
        print(f"\n⚠️  API Issues: {api_errors} potential errors/timeouts detected")
        
        # Check for hanging processes
        force_populate_clicks = logs.count('Force Auto-Populate')
        manual_json_clicks = logs.count('Generate JSON Now')
        
        print(f"\n🎛️  USER INTERACTIONS:")
        print(f"   • Force Auto-Populate clicks: {force_populate_clicks}")
        print(f"   • Manual JSON generation clicks: {manual_json_clicks}")
        
        return {
            'json_attempts': json_attempts,
            'extraction_failures': extraction_failures,
            'recent_responses': recent_responses[-3:] if recent_responses else [],
            'api_errors': api_errors
        }
        
    except Exception as e:
        print(f"❌ Error reading logs: {str(e)}")
        return None

def identify_root_causes(analysis):
    """Identify the root causes of slow generation"""
    
    print(f"\n🎯 ROOT CAUSE ANALYSIS:")
    print("=" * 40)
    
    if not analysis:
        print("❌ Could not analyze logs")
        return
    
    # Check for common issues
    issues = []
    
    if analysis['extraction_failures'] > analysis['json_attempts']:
        issues.append("🚨 CRITICAL: AI not generating proper JSON format")
    
    if analysis['json_attempts'] == 0:
        issues.append("🚨 CRITICAL: No JSON generation attempts detected")
    
    if analysis['api_errors'] > 5:
        issues.append("⚠️  API performance issues detected")
    
    # Analyze recent responses
    for i, response in enumerate(analysis['recent_responses']):
        if 'would you like' in response.lower() or 'let me know' in response.lower():
            issues.append(f"🔍 Response {i+1}: AI still in interview/research mode")
        elif '{' not in response:
            issues.append(f"🔍 Response {i+1}: No JSON structure in response")
    
    if issues:
        print("❌ IDENTIFIED ISSUES:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("✅ No obvious issues detected in logs")
    
    print(f"\n💡 RECOMMENDATIONS:")
    if analysis['extraction_failures'] > 0:
        print("   1. Check if AI is receiving proper JSON generation instructions")
        print("   2. Verify system prompts are enforcing JSON output format")
        print("   3. Consider using stronger completion triggers")
    
    if analysis['api_errors'] > 0:
        print("   4. Check API key validity and rate limits")
        print("   5. Consider adding timeout and retry logic")

def suggest_fixes():
    """Suggest immediate fixes for the slow generation issue"""
    
    print(f"\n🔧 IMMEDIATE FIX SUGGESTIONS:")
    print("=" * 40)
    
    print("1. 🚀 **Force Proper JSON Generation**:")
    print("   - Update system prompt to be more explicit about JSON requirement")
    print("   - Add stronger completion signals")
    print("   - Use template-based JSON generation")
    
    print("\n2. ⚡ **Performance Optimization**:")
    print("   - Add timeout controls for API calls")
    print("   - Implement request caching")
    print("   - Use streaming responses where possible")
    
    print("\n3. 🎛️ **User Experience**:")
    print("   - Show progress indicators during generation")
    print("   - Add cancel/retry buttons")
    print("   - Provide estimated completion times")
    
    print("\n4. 🧪 **Testing Recommendations**:")
    print("   - Test with minimal conversation (3 questions)")
    print("   - Use adaptive slide generation to reduce scope")
    print("   - Verify JSON markers are present in responses")

def main():
    """Main debugging function"""
    
    print("🐛 DEBUG: Slow JSON Generation Issue")
    print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Analyze logs
    analysis = analyze_streamlit_logs()
    
    # Identify root causes
    identify_root_causes(analysis)
    
    # Suggest fixes
    suggest_fixes()
    
    print(f"\n🌐 STREAMLIT URL: https://8502-i4lx93n6x87cg5p48o0ic-6532622b.e2b.dev")
    print("\n✅ Debug analysis complete!")

if __name__ == "__main__":
    main()
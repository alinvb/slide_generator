#!/usr/bin/env python3
"""
Monitor JSON generation progress in real-time
"""
import time
import subprocess
import re

def monitor_generation():
    """Monitor the JSON generation progress"""
    print("📊 Monitoring JSON Generation Progress...")
    print("=" * 60)
    
    last_line_count = 0
    
    while True:
        try:
            # Get recent log lines
            result = subprocess.run(['tail', '-50', '/home/user/webapp/streamlit.log'], 
                                  capture_output=True, text=True)
            
            lines = result.stdout.strip().split('\n')
            current_line_count = len(lines)
            
            # Look for progress indicators
            chunk_patterns = [
                r'🔍 \[CHUNK-(\d+)\] Calling API',
                r'✅ \[CHUNKED\] Chunk (\d+) success',
                r'🔍 \[CHUNKED\] Generating (\w+)',
                r'✅ \[CLEAN-REWRITE\] Step (\d+) Complete',
                r'📋 \[CLEAN\] Building render plan',
                r'✅ \[CLEAN\] Render plan built'
            ]
            
            # Find latest progress
            latest_progress = []
            for line in lines[-10:]:  # Last 10 lines
                for pattern in chunk_patterns:
                    match = re.search(pattern, line)
                    if match:
                        latest_progress.append(line.strip())
            
            # Check for completion or errors
            completion_indicators = [
                '✅ [CLEAN-REWRITE] JSON generation complete',
                '✅ [CLEAN] Render plan built',
                '❌',
                'ERROR',
                'FAILED'
            ]
            
            status = "🔄 In Progress"
            for line in lines[-5:]:
                for indicator in completion_indicators:
                    if indicator in line:
                        if '✅' in indicator:
                            status = "✅ Completed"
                        elif '❌' in indicator or 'ERROR' in indicator:
                            status = "❌ Error Detected"
            
            # Display current status
            print(f"\r{status} | Lines: {current_line_count} | Latest: ", end="")
            if latest_progress:
                print(latest_progress[-1][-80:])  # Show last 80 chars of latest progress
            else:
                print("Monitoring...")
            
            # Check for specific issues
            recent_lines = '\n'.join(lines[-20:])
            
            # Look for timeout issues
            if 'timeout' in recent_lines.lower():
                print("\n⚠️  Timeout detected in logs")
            
            # Look for JSON parsing issues  
            if 'JSON parsing failed' in recent_lines:
                print("\n⚠️  JSON parsing issue detected")
            
            # Look for API issues
            if 'API call failed' in recent_lines or 'status: 4' in recent_lines:
                print("\n⚠️  API call issue detected")
            
            # Break if completed or error
            if status in ["✅ Completed", "❌ Error Detected"]:
                break
                
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped by user")
            break
        except Exception as e:
            print(f"\n❌ Monitoring error: {e}")
            break
    
    print(f"\n📊 Final Status: {status}")

def check_recent_generation_results():
    """Check the most recent generation results"""
    print("\n📋 Recent Generation Summary:")
    print("=" * 60)
    
    try:
        # Get last 100 lines to analyze
        result = subprocess.run(['tail', '-100', '/home/user/webapp/streamlit.log'], 
                              capture_output=True, text=True)
        
        lines = result.stdout.strip().split('\n')
        
        # Extract key information
        company_name = None
        chunks_completed = []
        errors = []
        
        for line in lines:
            # Company name
            if 'Company:' in line and company_name is None:
                match = re.search(r'Company: (\w+)', line)
                if match:
                    company_name = match.group(1)
            
            # Chunk completion
            if 'Chunk' in line and 'success' in line:
                match = re.search(r'Chunk (\d+) success: (\d+) fields', line)
                if match:
                    chunks_completed.append(f"Chunk {match.group(1)}: {match.group(2)} fields")
            
            # Errors
            if '❌' in line or 'ERROR' in line or 'FAILED' in line:
                errors.append(line.strip())
        
        print(f"🏢 Company: {company_name or 'Unknown'}")
        print(f"📊 Chunks Completed: {len(chunks_completed)}")
        for chunk in chunks_completed:
            print(f"   ✅ {chunk}")
        
        if errors:
            print(f"⚠️  Errors Found: {len(errors)}")
            for error in errors[-3:]:  # Show last 3 errors
                print(f"   ❌ {error}")
        else:
            print("✅ No errors detected")
            
    except Exception as e:
        print(f"❌ Error analyzing logs: {e}")

if __name__ == "__main__":
    print("🔍 JSON Generation Monitor\n")
    
    # Check current status
    check_recent_generation_results()
    
    # Ask if user wants to monitor
    print(f"\nOptions:")
    print(f"1. Monitor generation progress (real-time)")
    print(f"2. Check current status only")
    
    try:
        choice = input("\nEnter choice (1 or 2): ").strip()
        if choice == "1":
            monitor_generation()
        else:
            print("📊 Status check complete")
    except:
        print("📊 Status check complete")
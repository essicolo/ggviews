#!/usr/bin/env python3
"""
Test all example files to ensure they run without errors
"""

import subprocess
import os
import sys
from pathlib import Path

def test_example_file(filename):
    """Test a single example file"""
    print(f"\n{'='*60}")
    print(f"Testing: {filename}")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, filename],
            cwd='/app/examples',
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ {filename} - SUCCESS")
            # Print last few lines of output
            lines = result.stdout.strip().split('\n')
            if len(lines) > 3:
                print("   Last output:")
                for line in lines[-3:]:
                    print(f"   {line}")
            return True
        else:
            print(f"❌ {filename} - FAILED")
            print("   Error output:")
            error_lines = result.stderr.strip().split('\n')
            for line in error_lines[-5:]:  # Last 5 error lines
                print(f"   {line}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️ {filename} - TIMEOUT (>30s)")
        return False
    except Exception as e:
        print(f"❌ {filename} - EXCEPTION: {e}")
        return False

def main():
    """Test all example files"""
    print("🚀 Testing All ggviews Example Files")
    print("="*60)
    
    # List of example files to test
    example_files = [
        'basic_usage.py',
        'test_notebook_compatibility.py', 
        'american_names_recreation.py',
        'updated_ggplot2_comparison.py',
        'advanced_examples.py',
        'faceting_comprehensive_test.py',
        'ggplot2_comparison.py',
        'simple_comparison.py',
        'test_advanced_features.py',
        'test_coordinates.py',
        'comprehensive_features_demo.py'
    ]
    
    # Check which files exist
    examples_dir = Path('/app/examples')
    existing_files = []
    missing_files = []
    
    for filename in example_files:
        filepath = examples_dir / filename
        if filepath.exists():
            existing_files.append(filename)
        else:
            missing_files.append(filename)
    
    if missing_files:
        print(f"\n⚠️ Missing files: {missing_files}")
    
    print(f"\n📋 Found {len(existing_files)} example files to test")
    
    # Test each file
    results = {}
    for filename in existing_files:
        results[filename] = test_example_file(filename)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"Total files tested: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success rate: {passed/total*100:.1f}%")
    
    print("\nDetailed Results:")
    for filename, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {filename}")
    
    if passed == total:
        print(f"\n🎉 ALL EXAMPLES WORKING PERFECTLY!")
        print(f"📊 ggviews library is fully functional!")
    else:
        failed_files = [f for f, success in results.items() if not success]
        print(f"\n⚠️ Files needing attention: {failed_files}")

if __name__ == "__main__":
    main()
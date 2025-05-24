#!/usr/bin/env python3
"""
Simple setup validation script for Strands Documentation Assistant.
Run this to verify your installation is working correctly.
"""

import os
import sys
import subprocess
import tempfile
import shutil

def test_python_version():
    """Test if Python version is compatible."""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not supported. Please use Python 3.9+")
        return False

def test_dependencies():
    """Test if required dependencies are installed."""
    print("\n🔍 Checking dependencies...")
    required_packages = ['boto3', 'requests']
    
    try:
        # Try importing strands - this might fail if not installed
        import strands
        print("✅ strands-agent is available")
    except ImportError:
        print("⚠️  strands-agent not found - this is expected if testing locally")
        print("   Install with: pip install strands-agent")
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is not installed")
            return False
    
    return True

def test_cli_parsing():
    """Test command line argument parsing."""
    print("\n🔍 Testing CLI argument parsing...")
    try:
        result = subprocess.run([
            sys.executable, 'main.py', '--help'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and '--docs-path' in result.stdout:
            print("✅ CLI argument parsing works")
            return True
        else:
            print("❌ CLI argument parsing failed")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def test_dry_run():
    """Test dry-run functionality with a temporary docs directory."""
    print("\n🔍 Testing dry-run mode...")
    
    # Create temporary directory with test docs
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "test.md")
        with open(test_file, 'w') as f:
            f.write("# Test Documentation\n\nThis is a test file for validation.")
        
        try:
            result = subprocess.run([
                sys.executable, 'main.py', 
                '--docs-path', temp_dir,
                '--dry-run'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and 'DRY RUN MODE' in result.stdout:
                print("✅ Dry-run mode works")
                print(f"   Found test documentation in: {temp_dir}")
                return True
            else:
                print("❌ Dry-run mode failed")
                print(f"   stdout: {result.stdout}")
                print(f"   stderr: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Dry-run test failed: {e}")
            return False

def test_aws_config():
    """Test if AWS configuration is available (optional)."""
    print("\n🔍 Checking AWS configuration (optional)...")
    
    # Check for AWS credentials
    has_credentials = (
        os.environ.get('AWS_ACCESS_KEY_ID') or 
        os.path.exists(os.path.expanduser('~/.aws/credentials'))
    )
    
    if has_credentials:
        print("✅ AWS credentials found")
        return True
    else:
        print("⚠️  AWS credentials not found")
        print("   This is okay for testing with --dry-run mode")
        print("   For full functionality, run: aws configure")
        return True  # Not a failure

def main():
    """Run all validation tests."""
    print("=" * 60)
    print("🧪 Strands Documentation Assistant - Setup Validation")
    print("=" * 60)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("CLI Parsing", test_cli_parsing),
        ("Dry Run Mode", test_dry_run),
        ("AWS Configuration", test_aws_config),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("  1. Add documentation files to ./docs/ directory")
        print("  2. Run: python main.py --dry-run")
        print("  3. Configure AWS: aws configure")
        print("  4. Run: python main.py")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 
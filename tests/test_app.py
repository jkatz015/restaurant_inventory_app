#!/usr/bin/env python3
"""
Simple test file to verify the Restaurant Kitchen Inventory app structure
"""

import sys
import os
import importlib

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import streamlit
        import pandas
        import PIL
        import plotly
        print("✅ All required packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_page_modules():
    """Test that all page modules can be imported"""
    pages = [
        "1_ProductDatabase",
        "2_RecipeBuilder", 
        "3_VarianceCalculator",
        "4_SheetToShelfInventory"
    ]
    
    # Add pages directory to path
    sys.path.append('pages')
    
    for page in pages:
        try:
            module = importlib.import_module(page)
            if hasattr(module, 'main'):
                print(f"✅ {page}.py imported successfully with main() function")
            else:
                print(f"⚠️ {page}.py imported but missing main() function")
        except Exception as e:
            print(f"❌ Error importing {page}.py: {e}")
            return False
    
    return True

def test_data_directory():
    """Test that data directory exists"""
    if os.path.exists("data"):
        print("✅ Data directory exists")
        return True
    else:
        print("❌ Data directory missing")
        return False

def test_logo_file():
    """Test that logo file exists"""
    logo_path = "data/Curated Restaurant Consulting Logo for Business Card.png"
    if os.path.exists(logo_path):
        print("✅ Logo file exists")
        return True
    else:
        print("⚠️ Logo file not found (this is optional)")
        return True

def main():
    """Run all tests"""
    print("🧪 Testing Restaurant Kitchen Inventory App...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_page_modules,
        test_data_directory,
        test_logo_file
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! App is ready to run.")
        print("\nTo run the app:")
        print("py -m streamlit run app.py")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main() 
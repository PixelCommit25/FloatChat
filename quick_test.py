#!/usr/bin/env python3
"""
Quick FloatChat System Verification
Fast check to see if the system is working
"""

def quick_check():
    """Quick system verification"""
    print("🌊 FloatChat Quick System Check")
    print("=" * 40)
    
    # Test 1: Basic imports
    print("1. Testing basic imports...")
    try:
        import pandas as pd
        import numpy as np
        import streamlit as st
        print("   ✅ Core modules OK")
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("   Fix: pip install -r requirements.txt")
        return False
    
    # Test 2: Data processor
    print("2. Testing data processor...")
    try:
        from data_processor import ArgoDataPipeline
        pipeline = ArgoDataPipeline()
        print("   ✅ Data processor OK")
    except Exception as e:
        print(f"   ❌ Data processor error: {e}")
        return False
    
    # Test 3: FloatChat system
    print("3. Testing FloatChat system...")
    try:
        from floatchat_system import FloatChatQueryProcessor
        processor = FloatChatQueryProcessor()
        print("   ✅ FloatChat system OK")
    except Exception as e:
        print(f"   ❌ FloatChat system error: {e}")
        return False
    
    # Test 4: Streamlit app
    print("4. Testing Streamlit app...")
    try:
        import floatchat_app
        print("   ✅ Streamlit app OK")
    except Exception as e:
        print(f"   ❌ Streamlit app error: {e}")
        return False
    
    print("\n🎉 Quick check PASSED!")
    print("\n🚀 Ready to run:")
    print("   streamlit run floatchat_app.py")
    return True

if __name__ == "__main__":
    quick_check()
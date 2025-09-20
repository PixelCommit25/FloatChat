#!/usr/bin/env python3
"""
Test script to verify query processing works
"""

def test_query_processing():
    """Test the query processing functionality"""
    print("🧪 Testing Query Processing Fix")
    print("=" * 40)
    
    try:
        from floatchat_system import FloatChatQueryProcessor
        
        # Initialize processor
        processor = FloatChatQueryProcessor()
        print("✅ Query processor initialized")
        
        # Test queries
        test_queries = [
            "Show me temperature profiles near the equator",
            "Find salinity data in the Arabian Sea",
            "Display oxygen levels in the Indian Ocean",
            "Show me all data from the last 6 months"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Test {i}: {query}")
            
            try:
                result = processor.process_natural_language_query(query)
                
                if result['success']:
                    df = result['results']
                    print(f"   ✅ Success: {len(df)} profiles found")
                    print(f"   📊 Columns: {list(df.columns)}")
                    print(f"   🔍 SQL: {result['sql_query'][:100]}...")
                else:
                    print(f"   ❌ Failed: {result['message']}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        print("\n🎉 Query processing test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_query_processing()

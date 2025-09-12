import json
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def test_precedent_transactions_data():
    """Test the precedent transactions data extraction and rendering flow"""
    
    # Create sample content_ir with precedent transactions data
    sample_content_ir = {
        "precedent_transactions": [
            {
                "target": "Netflix Competitor A",
                "acquirer": "Media Giant Corp",
                "date": "2023",
                "country": "USA",
                "enterprise_value": "$15.2B",
                "revenue": "$3.4B", 
                "ev_revenue_multiple": "4.5x"
            },
            {
                "target": "Streaming Service B", 
                "acquirer": "Tech Company",
                "date": "2022",
                "country": "UK",
                "enterprise_value": "$8.1B",
                "revenue": "$1.8B",
                "ev_revenue_multiple": "4.5x"
            },
            {
                "target": "Content Platform C",
                "acquirer": "Entertainment Corp",
                "date": "2023", 
                "country": "Canada",
                "enterprise_value": "$5.3B",
                "revenue": "$1.2B",
                "ev_revenue_multiple": "4.4x"
            }
        ]
    }
    
    generator = CleanBulletproofJSONGenerator()
    
    # Test the extract_slide_data function for precedent_transactions
    def extract_slide_data(slide_type: str, content_ir: dict) -> dict:
        """Copy of the exact extraction logic from the main file"""
        if slide_type == "precedent_transactions":
            transactions = content_ir.get('precedent_transactions', [])
            
            processed_transactions = []
            
            for txn in transactions:
                if isinstance(txn, dict):
                    processed_txn = {
                        "target": txn.get('target', 'Target Company'),
                        "acquirer": txn.get('acquirer', 'Acquirer'),
                        "date": txn.get('date', 'N/A'),
                        "country": txn.get('country', 'N/A'),
                        "enterprise_value": txn.get('enterprise_value', 'Data Issue'),
                        "revenue": txn.get('revenue', 'Data Issue'),
                        "ev_revenue_multiple": txn.get('ev_revenue_multiple', 'N/A')
                    }
                    processed_transactions.append(processed_txn)
                elif isinstance(txn, str):
                    processed_transactions.append({
                        "target": "Transaction Data",
                        "acquirer": "Acquirer",
                        "date": "N/A",
                        "country": "N/A", 
                        "enterprise_value": "Data Format Issue",
                        "revenue": "Data Format Issue",
                        "ev_revenue_multiple": "N/A"
                    })
            
            return {
                "title": "Precedent Transactions",
                "transactions": processed_transactions
            }
    
    # Extract slide data
    slide_data = extract_slide_data("precedent_transactions", sample_content_ir)
    
    print("=== PRECEDENT TRANSACTIONS DEBUG ===")
    print(f"Original transactions count: {len(sample_content_ir['precedent_transactions'])}")
    print(f"Processed transactions count: {len(slide_data['transactions'])}")
    
    print("\n=== ORIGINAL DATA ===")
    for i, txn in enumerate(sample_content_ir['precedent_transactions']):
        print(f"Transaction {i+1}: {json.dumps(txn, indent=2)}")
    
    print("\n=== PROCESSED SLIDE DATA ===")
    for i, txn in enumerate(slide_data['transactions']):
        print(f"Transaction {i+1}: {json.dumps(txn, indent=2)}")
    
    print("\n=== DATA VALIDATION ===")
    for i, txn in enumerate(slide_data['transactions']):
        print(f"Transaction {i+1}: {isinstance(txn, dict)} - Fields: {list(txn.keys()) if isinstance(txn, dict) else 'Not dict'}")
    
    return slide_data

if __name__ == "__main__":
    test_precedent_transactions_data()

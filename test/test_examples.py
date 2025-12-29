"""
Visual examples of FIFO matching with detailed output
Shows input and output for each test case

Usage:
    python test/test_examples.py
    
    Or from project root:
    python -m test.test_examples
"""

import sys
import os
import pandas as pd

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fifo_matching import perform_fifo_matching_logic


def print_dataframe(df, title):
    """Print dataframe with title"""
    print(f"\n{title}")
    print("-" * 80)
    if len(df) == 0:
        print("(empty)")
    else:
        print(df.to_string(index=False))
    print()


def example_1_simple_matching():
    """Example 1: Simple one-to-one matching"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Simple One-to-One Matching")
    print("="*80)
    print("Scenario: Customer earns $100, then spends $100")
    
    earned = pd.DataFrame({
        'transaction_id': ['E001'],
        'customer_id': ['C001'],
        'amount': [100.0],
        'timestamp': pd.to_datetime(['2024-01-01']),
        'transaction_type': ['earned']
    })
    
    spent = pd.DataFrame({
        'transaction_id': ['S001'],
        'customer_id': ['C001'],
        'amount': [-100.0],
        'timestamp': pd.to_datetime(['2024-01-05']),
        'transaction_type': ['spent']
    })
    
    expired = pd.DataFrame(columns=['transaction_id', 'customer_id', 'amount', 'timestamp', 'transaction_type'])
    
    print_dataframe(earned, "INPUT - Earned Transactions:")
    print_dataframe(spent, "INPUT - Spent Transactions:")
    
    result = perform_fifo_matching_logic(earned, spent, expired)
    print_dataframe(result, "OUTPUT - Matched Transactions with REDEEMID:")
    
    print("Explanation:")
    print("- Spent S001 points to earned E001 (REDEEMID = E001)")
    print("- Earned E001 points to spent S001 (REDEEMID = S001)")
    print("- Both transactions are fully matched")


def example_2_one_to_one_matching():
    """Example 2: 1:1 matching (no partial redemption)"""
    print("\n" + "="*80)
    print("EXAMPLE 2: 1:1 Matching (No Partial Redemption)")
    print("="*80)
    print("Scenario: Customer earns $100, spends $60 - no splitting")
    
    earned = pd.DataFrame({
        'transaction_id': ['E001'],
        'customer_id': ['C001'],
        'amount': [100.0],
        'timestamp': pd.to_datetime(['2024-01-01']),
        'transaction_type': ['earned']
    })
    
    spent = pd.DataFrame({
        'transaction_id': ['S001'],
        'customer_id': ['C001'],
        'amount': [-60.0],
        'timestamp': pd.to_datetime(['2024-01-05']),
        'transaction_type': ['spent']
    })
    
    expired = pd.DataFrame(columns=['transaction_id', 'customer_id', 'amount', 'timestamp', 'transaction_type'])
    
    print_dataframe(earned, "INPUT - Earned Transactions:")
    print_dataframe(spent, "INPUT - Spent Transactions:")
    
    result = perform_fifo_matching_logic(earned, spent, expired)
    print_dataframe(result, "OUTPUT - Matched Transactions with REDEEMID:")
    
    print("Explanation:")
    print("- 1:1 matching: Each TRANS_ID used only once")
    print("- Spent S001 points to earned E001 (REDEEMID = E001)")
    print("- Earned E001 points to spent S001 (REDEEMID = S001)")
    print("- E001 amount remains $100 (no splitting)")
    print("- Note: This is 1:1 matching, not partial redemption")


def example_3_fifo_order():
    """Example 3: FIFO order with multiple earned (1:1 matching)"""
    print("\n" + "="*80)
    print("EXAMPLE 3: FIFO Order - Oldest Earned First (1:1 Matching)")
    print("="*80)
    print("Scenario: Customer earns $50, $30, $20, then spends $70")
    
    earned = pd.DataFrame({
        'transaction_id': ['E001', 'E002', 'E003'],
        'customer_id': ['C001', 'C001', 'C001'],
        'amount': [50.0, 30.0, 20.0],
        'timestamp': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
        'transaction_type': ['earned', 'earned', 'earned']
    })
    
    spent = pd.DataFrame({
        'transaction_id': ['S001'],
        'customer_id': ['C001'],
        'amount': [-70.0],
        'timestamp': pd.to_datetime(['2024-01-10']),
        'transaction_type': ['spent']
    })
    
    expired = pd.DataFrame(columns=['transaction_id', 'customer_id', 'amount', 'timestamp', 'transaction_type'])
    
    print_dataframe(earned, "INPUT - Earned Transactions:")
    print_dataframe(spent, "INPUT - Spent Transactions:")
    
    result = perform_fifo_matching_logic(earned, spent, expired)
    print_dataframe(result, "OUTPUT - Matched Transactions with REDEEMID:")
    
    print("Explanation:")
    print("- 1:1 matching: S001 matches only E001 (oldest earned)")
    print("- E001 ($50) matched to S001")
    print("- E002 ($30) and E003 ($20) remain unmatched")
    print("- No splitting - each TRANS_ID used only once")


def example_4_multiple_spent():
    """Example 4: One earned, multiple spent (1:1 matching)"""
    print("\n" + "="*80)
    print("EXAMPLE 4: One Earned, Multiple Spent (1:1 Matching)")
    print("="*80)
    print("Scenario: Customer earns $100, then spends $30, $40, $20")
    
    earned = pd.DataFrame({
        'transaction_id': ['E001'],
        'customer_id': ['C001'],
        'amount': [100.0],
        'timestamp': pd.to_datetime(['2024-01-01']),
        'transaction_type': ['earned']
    })
    
    spent = pd.DataFrame({
        'transaction_id': ['S001', 'S002', 'S003'],
        'customer_id': ['C001', 'C001', 'C001'],
        'amount': [-30.0, -40.0, -20.0],
        'timestamp': pd.to_datetime(['2024-01-05', '2024-01-06', '2024-01-07']),
        'transaction_type': ['spent', 'spent', 'spent']
    })
    
    expired = pd.DataFrame(columns=['transaction_id', 'customer_id', 'amount', 'timestamp', 'transaction_type'])
    
    print_dataframe(earned, "INPUT - Earned Transactions:")
    print_dataframe(spent, "INPUT - Spent Transactions:")
    
    result = perform_fifo_matching_logic(earned, spent, expired)
    print_dataframe(result, "OUTPUT - Matched Transactions with REDEEMID:")
    
    print("Explanation:")
    print("- 1:1 matching: Only first spent matches earned")
    print("- S001 ($30) matches E001 (REDEEMID = E001)")
    print("- S002 and S003 have NULL REDEEMID (no more earned available)")
    print("- E001 amount remains $100 (no splitting)")
    print("- Each TRANS_ID used only once")


def example_5_multiple_customers():
    """Example 5: Multiple customers"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Multiple Customers (Independent Matching)")
    print("="*80)
    print("Scenario: Two customers with separate transactions")
    
    earned = pd.DataFrame({
        'transaction_id': ['E001', 'E002'],
        'customer_id': ['C001', 'C002'],
        'amount': [100.0, 50.0],
        'timestamp': pd.to_datetime(['2024-01-01', '2024-01-01']),
        'transaction_type': ['earned', 'earned']
    })
    
    spent = pd.DataFrame({
        'transaction_id': ['S001', 'S002'],
        'customer_id': ['C001', 'C002'],
        'amount': [-50.0, -30.0],
        'timestamp': pd.to_datetime(['2024-01-05', '2024-01-05']),
        'transaction_type': ['spent', 'spent']
    })
    
    expired = pd.DataFrame(columns=['transaction_id', 'customer_id', 'amount', 'timestamp', 'transaction_type'])
    
    print_dataframe(earned, "INPUT - Earned Transactions:")
    print_dataframe(spent, "INPUT - Spent Transactions:")
    
    result = perform_fifo_matching_logic(earned, spent, expired)
    print_dataframe(result, "OUTPUT - Matched Transactions with REDEEMID:")
    
    print("Explanation:")
    print("- C001: S001 matches E001 (no cross-customer matching)")
    print("- C002: S002 matches E002 (no cross-customer matching)")
    print("- Each customer's transactions are matched independently")


def example_6_expired():
    """Example 6: Expired transactions (1:1 matching)"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Expired Transactions (1:1 Matching)")
    print("="*80)
    print("Scenario: Customer earns $100, $50 expires")
    
    earned = pd.DataFrame({
        'transaction_id': ['E001'],
        'customer_id': ['C001'],
        'amount': [100.0],
        'timestamp': pd.to_datetime(['2024-01-01']),
        'transaction_type': ['earned']
    })
    
    spent = pd.DataFrame(columns=['transaction_id', 'customer_id', 'amount', 'timestamp', 'transaction_type'])
    
    expired = pd.DataFrame({
        'transaction_id': ['X001'],
        'customer_id': ['C001'],
        'amount': [-50.0],
        'timestamp': pd.to_datetime(['2024-06-01']),
        'transaction_type': ['expired']
    })
    
    print_dataframe(earned, "INPUT - Earned Transactions:")
    print_dataframe(expired, "INPUT - Expired Transactions:")
    
    result = perform_fifo_matching_logic(earned, spent, expired)
    print_dataframe(result, "OUTPUT - Matched Transactions with REDEEMID:")
    
    print("Explanation:")
    print("- 1:1 matching: Expired X001 matches E001")
    print("- X001 points to E001 (REDEEMID = E001)")
    print("- E001 points to X001 (REDEEMID = X001)")
    print("- E001 amount remains $100 (no splitting)")
    print("- Expired transactions work same as spent (1:1 matching)")


def run_all_examples():
    """Run all visual examples"""
    print("\n" + "="*80)
    print("THRIVE CASH FIFO MATCHING - VISUAL EXAMPLES")
    print("="*80)
    
    examples = [
        example_1_simple_matching,
        example_2_one_to_one_matching,
        example_3_fifo_order,
        example_4_multiple_spent,
        example_5_multiple_customers,
        example_6_expired
    ]
    
    for example in examples:
        example()
    
    print("\n" + "="*80)
    print("All examples completed!")
    print("="*80 + "\n")


if __name__ == "__main__":
    run_all_examples()

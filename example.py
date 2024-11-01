import requests
import json

def get_transaction_history(address, limit=10):
    url = "https://api.mainnet-beta.solana.com"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",  # Updated method name
        "params": [
            address,
            {
                "limit": limit  # Adjust the limit for more transactions
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Example usage
address = "#replace with your address"
try:
    transaction_history = get_transaction_history(address)

    # Print the transaction history
    if 'result' in transaction_history:
        if transaction_history['result']:
            for txn in transaction_history['result']:
                print(f"Signature: {txn['signature']}, Slot: {txn['slot']}, Err: {txn['err']}")
        else:
            print("No transaction history found for this address.")
    else:
        print("Error in the response:", transaction_history.get('error', 'Unknown error'))
except Exception as e:
    print(str(e))

import aiohttp
import asyncio
import json

async def fetch_transaction_history(session, address, limit=10):
    url = "https://api.mainnet-beta.solana.com"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [address, {"limit": limit}]
    }
    headers = {"Content-Type": "application/json"}
    
    async with session.post(url, headers=headers, json=payload) as response:
        if response.status == 200:
            return await response.json()
        else:
            raise Exception(f"Error: {response.status}, {await response.text()}")

async def get_transaction_histories(addresses, limit=10):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for address in addresses:
            tasks.append(fetch_transaction_history(session, address, limit))
        return await asyncio.gather(*tasks)

def read_addresses(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]  # Filter out empty lines
    except FileNotFoundError:
        print("Error: address.txt file not found.")
        return []
    except Exception as e:
        print(f"Error reading the address file: {e}")
        return []

async def main():
    addresses = read_addresses('address.txt')
    results = await get_transaction_histories(addresses)

    # Write results to result.txt
    with open('result.txt', 'w', encoding='utf-8') as f:
        for address, transaction_history in zip(addresses, results):
            if transaction_history and 'result' in transaction_history:
                transaction_count = len(transaction_history['result']) if transaction_history['result'] else 0
                f.write(f"{address}: {transaction_count} транзакций\n")
            else:
                f.write(f"{address}: Ошибка в ответе или превышен лимит.\n")

    print("Results written to result.txt")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())

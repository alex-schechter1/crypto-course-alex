import os
import pandas as pd
from web3 import Web3
import matplotlib.pyplot as plt
import seaborn as sns
from web3.types import LogReceipt, TxData
from dotenv import load_dotenv

load_dotenv()
BADGER_TOKEN_ADDRESS = '0x4b92d19c11435614cd49af1b589001b7c08cd4d5'

def get_approvals(w3: Web3) -> list[LogReceipt]:
    transfer_event_hash = Web3.keccak(text='Approval(address,address,uint256)')

    return w3.eth.get_logs({'address': Web3.to_checksum_address(BADGER_TOKEN_ADDRESS), 'topics':[transfer_event_hash], 'fromBlock': 13133845, 'toBlock': 13916631})

infura_url = os.getenv("INFURA_URL")
infura_api_key = os.getenv("INFURA_API_KEY")
w3 = Web3(Web3.HTTPProvider(f'{infura_url}/{infura_api_key}'))

# Call get_approvals function with provided address
approval_list = get_approvals(w3)
approval: LogReceipt
df = pd.DataFrame(map(lambda approval: {
    'token_contract_address': approval.address,
    'transaction_hash': approval.transactionHash.hex(),
    'amount_of_tokens': int.from_bytes(approval.data, byteorder="big"),
    'from_user': '0x' + approval.topics[1].hex()[-40:],
    'spender': '0x' + approval.topics[2].hex()[-40:],
    'block_number': approval.blockNumber
}, approval_list))

print(len(approval_list))
df.head()

spender_counts = df['spender'].value_counts().reset_index()
spender_counts.columns = ['spender', 'count']
spender_counts['is_contract'] = spender_counts.apply(lambda row: w3.eth.get_code(w3.to_checksum_address(row.spender)).hex() > hex(0), axis=1)
print(spender_counts.head(10))

import matplotlib.pyplot as plt
import seaborn as sns

colors = ['green' if is_contract else 'red' for is_contract in spender_counts['is_contract']]
plt.figure(figsize=(12, 8))
sns.barplot(x='spender', y='count', data=spender_counts.head(100), palette=colors)
plt.title('Number of Approvals for Each Spender')
plt.xlabel('Spender')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
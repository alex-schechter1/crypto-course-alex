import os
import argparse
from web3 import Web3
from web3.types import LogReceipt
from dotenv import load_dotenv

load_dotenv()

def get_approvals(w3: Web3, address: str, ) -> list[LogReceipt]:
    transfer_event_hash = Web3.keccak(text='Approval(address,address,uint256)')
    checksum_address = Web3.to_checksum_address(address)
    padded_address = '0x' + address[2:].zfill(64).lower()
    return w3.eth.get_logs({'topics':[transfer_event_hash, padded_address], 'fromBlock': 0, 'toBlock': 4581766})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve ERC20 token approvals for a given address.')
    parser.add_argument('--address', type=str, help='Ethereum address to check approvals for', required=True)
    args = parser.parse_args()

    infura_url = os.getenv("INFURA_URL")
    infura_api_key = os.getenv("INFURA_API_KEY")
    w3 = Web3(Web3.HTTPProvider(f'{infura_url}/{infura_api_key}'))

    # Call get_approvals function with provided address
    approval: LogReceipt
    for approval in get_approvals(w3, args.address):
        abi = [{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]
        contract = w3.eth.contract(approval.address, abi = abi)
        token_symbol = contract.functions.symbol().call()
        printed_token = token_symbol if token_symbol else approval.address
        print(f'approval on {printed_token} on amount of {int.from_bytes(approval.topics[2], byteorder="big")}')
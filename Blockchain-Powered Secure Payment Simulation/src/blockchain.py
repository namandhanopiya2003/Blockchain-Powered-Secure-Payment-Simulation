from web3 import Web3
import json
import os

class BlockchainManager:
    def __init__(self):
        # Connects to local blockchain running on this address
        self.w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

        # If connection fails, it shows error message
        if not self.w3.is_connected():
            raise Exception("<!> Could not connect to Ganache. Please start Ganache.")

        # Loads the compiled contract from the build folder
        build_path = os.path.join(os.path.dirname(__file__), "../build/contracts/Payroll.json")
        with open(build_path, "r") as f:
            build = json.load(f)

        # Gets the contract's deployed address from the JSON file
        try:
            network_id = list(build["networks"].keys())[0]
            self.contract_address = build["networks"][network_id]["address"]
        except (IndexError, KeyError):
            raise Exception("<!> Payroll contract not deployed. Run `truffle migrate --reset` first.")

        self.contract_abi = build["abi"]
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.contract_abi)

        # Gets list of available accounts
        self.accounts = self.w3.eth.accounts
        if not self.accounts:
            raise Exception("<!> No accounts found in Ganache.")

        # Prints connection info
        print(f"==> Connected to Ganache")
        print(f"==> Using contract address: {self.contract_address}")
        print(f"==> Accounts available: {self.accounts[:3]} ...")

    def pay_salary(self, emp_id, amount_wei):
        try:
            # Uses the first account to send the transaction
            from_account = self.accounts[0]
            # Preparse the transaction to call 'paySalary' on the smart contract
            tx = self.contract.functions.paySalary(emp_id, amount_wei).build_transaction({
                "from": from_account,
                "nonce": self.w3.eth.get_transaction_count(from_account),
                "gas": 3000000
            })

            # Sends the transaction to the blockchain
            tx_hash = self.w3.eth.send_transaction(tx)
            # Waits for the transaction to finish and get the receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return receipt

        # If something goes wrong, it prints the error
        except Exception as e:
            print(f"<!> Error during salary payment: {e}")
            return None

if __name__ == "__main__":
    bc = BlockchainManager()
    receipt = bc.pay_salary(emp_id=1, amount_wei=10**18)
    print("Payment receipt:", receipt)


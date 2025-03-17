# 🔐 Bitcoin Transaction Signer

This project demonstrates how to **sign a Bitcoin transaction offline** using the `bitcoin` Python library. The script allows you to generate a transaction hex using a WIF (Wallet Import Format) private key, receiver's legacy wallet address, and UTXOs (Unspent Transaction Outputs) data.

---

## 📌 Features
- Generate raw Bitcoin transaction hexes offline.
- Support for **WIF private keys**.
- Transaction output can be broadcasted online using services like Slipstream Mara.
- It is perfect if you find any of the private key of the BTC Puzzle challenge.

---

## 📂 Requirements
- Python 3.x
- `bitcoin` library 
- `base58` library 
- `ecdsa` library 

---

## ⚙️ Installation
1. Clone the repository:
```bash
git clone https://github.com/jalfr3d/btc-transaction-signer.git
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

---

## 📌 Usage
1. Edit main.py with your private key, receiver's address, and UTXO data.
2. Run the script.
3. The script will output the transaction hex.

---

## 💡 Example Usage
```bash
private_key_wif = "<your_wif_private_key>"
to_address = "1YourLegacyAddressHere"
utxos = [
    {"txid": "d14fa6c0c8e88bc74e420b8f678a3143f396a648315c911970971ef57ef59e3c", "vout": 0, "value": 612000},
    {"txid": "b9a2588b6bb080c7788dbcebb44d3eb84fd7c27a8a1e376a2d4cdef3f21b8be3", "vout": 1, "value": 61200}
]
amount = 6.8
fee_rate = 20

transaction_hex = create_raw_transaction(private_key_wif, to_address, utxos, amount, fee_rate)
print("Raw Transaction Hex:", transaction_hex)
```
* The UTXOS data load in the main.py are from the Puzzle 68.
---

## 📝 Important Notes
- Ensure your private key is stored securely and never exposed online.
- The generated transaction hex must be broadcasted online manually.
- This script currently supports legacy addresses (starting with '1').

---

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## ❤️ Donation
bc1q9zntcdsum9mneum23uvwv8z34mzyj5j2r0m2ty

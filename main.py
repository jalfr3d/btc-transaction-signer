from bitcoin import *
import ecdsa
import requests


def create_raw_transaction(private_key_wif, to_address, amount, fee):
    # Convert WIF private key to hexadecimal format
    private_key_hex = decode_privkey(private_key_wif, 'wif')

    # Get public key
    signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    public_key = '04' + verifying_key.to_string().hex()

    # Get the Bitcoin address from the public key
    from_address = pubkey_to_address(public_key)

    # Fetch unspent transactions (UTXOs)
    response = requests.get(f"https://blockchain.info/unspent?active={from_address}")
    utxos = response.json()['unspent_outputs']

    # Choose the first UTXO (You may want to select more for larger amounts)
    utxo = utxos[0]
    txid = utxo['tx_hash_big_endian']
    vout = utxo['tx_output_n']
    value = utxo['value']

    # Calculate the change
    satoshi_amount = int(amount * 1e8)
    satoshi_fee = int(fee * 1e8)
    change = value - satoshi_amount - satoshi_fee

    # Build the transaction
    tx = mktx([{
        'output': f'{txid}:{vout}',
        'value': value
    }], [
        {'address': to_address, 'value': satoshi_amount},
        {'address': from_address, 'value': change}
    ])

    # Sign the transaction
    signed_tx = sign(tx, 0, private_key_wif)
    return signed_tx


# Example usage:
private_key_wif = "<Your WIF Private Key>"
to_address = "<Your New Receiving Address>"
amount = 0.001  # Amount of BTC to send
fee = 0.0001  # Fee in BTC

transaction_hex = create_raw_transaction(private_key_wif, to_address, amount, fee)
print("Raw Transaction Hex:", transaction_hex)

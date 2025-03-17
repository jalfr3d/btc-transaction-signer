from bitcoin import *
import ecdsa
import base58


def decode_privkey(wif_privkey):
    """Decodes a WIF private key, handling compression."""
    decoded = base58.b58decode(wif_privkey)
    if len(decoded) == 38 and decoded[-5] == 0x01:  # Compressed key
        return decoded[1:-5], True
    elif len(decoded) == 37:  # Uncompressed key
        return decoded[1:-1], False
    else:
        raise ValueError("Invalid WIF private key")


def encode_privkey(privkey_bytes, encoding='hex'):
    """Encodes a private key to hex or bytes."""
    if encoding == 'hex':
        return privkey_bytes.hex()
    elif encoding == 'bytes':
        return privkey_bytes
    else:
        raise ValueError("Invalid encoding specified")


def get_public_key(private_key_wif):
    """Generates a public key from a WIF private key."""
    private_key_bytes, compressed = decode_privkey(private_key_wif)
    signing_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()

    if compressed:
        public_key = verifying_key.to_string("compressed").hex()
    else:
        public_key = '04' + verifying_key.to_string().hex()  # Uncompressed format

    return public_key, compressed


def estimate_transaction_size(num_inputs, num_outputs, compressed=True):
    """Estimate transaction size in bytes."""
    base_size = 10  # Basic transaction structure
    input_size = 148 if not compressed else 108  # Input size depends on key type
    output_size = 34  # Standard output size
    return base_size + (num_inputs * input_size) + (num_outputs * output_size)


def create_raw_transaction(private_key_wif, to_address, utxos, amount, fee_rate):
    # Get the private key bytes and compression status
    private_key_bytes, compressed = decode_privkey(private_key_wif)

    # Generate signing key and public key
    signing_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()

    if compressed:
        public_key = verifying_key.to_string("compressed").hex()
    else:
        public_key = '04' + verifying_key.to_string().hex()  # Uncompressed format

    # Generate the sending address
    from_address = pubkey_to_address(public_key)

    # Prepare inputs
    total_input_value = 0
    inputs = []
    for utxo in utxos:
        inputs.append({
            'output': f"{utxo['txid']}:{utxo['vout']}",
            'value': utxo['value']
        })
        total_input_value += utxo['value']

    # Check if the total inputs cover the amount
    satoshi_amount = int(amount * 1e8)
    estimated_size = estimate_transaction_size(len(utxos), 2, compressed)  # 2 outputs (recipient + change)
    satoshi_fee = estimated_size * fee_rate  # Calculate fee in satoshis

    if total_input_value < (satoshi_amount + satoshi_fee):
        raise ValueError("Insufficient funds for transaction.")

    # Calculate the change
    change = total_input_value - satoshi_amount - satoshi_fee

    # Prepare outputs
    outputs = [{'address': to_address, 'value': satoshi_amount}]
    if change > 0:
        outputs.append({'address': from_address, 'value': change})

    # Create the raw transaction
    tx = mktx(inputs, outputs)

    # Sign each input
    for i, _ in enumerate(inputs):
        tx = sign(tx, i, private_key_wif)

    return tx


# Example usage:
private_key_wif = "KxH7JiGfvbPnqzr5iHekXaEvaLRTNrtSGPZaDpCPVtHcLjuE4XL9"
to_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"


# Manually add UTXOs (replace with your real UTXO data)
utxos = [
    {
        'txid': '12f34b58b04dfb0233ce889f674781c0e0c7ba95482cca469125af41a78d13b3',  # Example: 'b3f5b6...7c8'
        'vout': 3,  # check the explorer
        'value': int(6.12 * 1e8)  # Amount in satoshis (0.001 BTC = 100000 satoshis)
    },
    {
        'txid': '5d45587cfd1d5b0fb826805541da7d94c61fe432259e68ee26f4a04544384164',
        'vout': 16,
        'value': int(0.612 * 1e8)
    },
    {
        'txid': '08389f34c98c606322740c0be6a7125d9860bb8d5cb182c02f98461e5fa6cd15',
        'vout': 67,
        'value': int(0.068 * 1e8)
    }
]

amount = 6.7999  # Amount of BTC to send (in BTC)
fee_rate = 20  # Fee rate in sats/vByte (Mara requirement)

try:
    transaction_hex = create_raw_transaction(private_key_wif, to_address, utxos, amount, fee_rate)
    print("Raw Transaction Hex:", transaction_hex)
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    import traceback
    print("An unexpected error occurred:")
    print(str(e))
    traceback.print_exc()
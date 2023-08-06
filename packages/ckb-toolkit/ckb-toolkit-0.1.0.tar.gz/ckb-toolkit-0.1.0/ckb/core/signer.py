from .types import Transaction, HexBytes
from .transaction import transaction_hash, extend_serialized_raw_transaction
from .hash import ckb_hasher
from .hex_coder import hex_to_bytes, hex_from_bytes
from .molecule import extend_uint64
from coincurve import PrivateKey
from .witness_args import new_witness_args, extend_serialized_witness_args

def sign_tx(tx: Transaction, private_key: HexBytes) -> Transaction:
    tx_hash = transaction_hash(tx)
    hasher = ckb_hasher()
    hasher.update(hex_to_bytes(tx_hash))

    witness_args = new_witness_args()
    witness_buffer = bytearray()
    extend_serialized_witness_args(witness_buffer, witness_args)
    len_buffer = bytearray()
    extend_uint64(len_buffer, str(len(witness_buffer)))
    hasher.update(len_buffer)
    hasher.update(witness_buffer)

    witnesses = tx['witnesses'][1:]
    for witness in witnesses:
        len_buffer = bytearray()
        extend_uint64(len_buffer, len(witness))
        hasher.update(len_buffer)
        hasher.update(hex_to_bytes(witnesses))

    message = '0x' + hasher.hexdigest()

    _private_key = PrivateKey.from_hex(private_key)
    signature = _private_key.sign_recoverable(hex_to_bytes(message), None)

    witness_args = new_witness_args(lock=hex_from_bytes(signature))
    witness_buffer = bytearray()
    serialized_witness_args = extend_serialized_witness_args(
        witness_buffer, witness_args)

    tx['witnesses'][0] = hex_from_bytes(witness_buffer)

    return tx

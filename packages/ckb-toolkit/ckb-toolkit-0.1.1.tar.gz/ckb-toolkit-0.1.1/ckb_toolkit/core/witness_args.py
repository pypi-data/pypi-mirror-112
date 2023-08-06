from .types import HexBytes, WitnessArgs
from .molecule import HeaderBuilder, extend_uint32, extend_uint64, extend_bytes_array, extend_bytes_fixvec
from .hex_coder import hex_from_bytes, hex_to_bytes

SIGNATURE_PLACEHOLDER = "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"


def new_witness_args(lock=SIGNATURE_PLACEHOLDER):
    return {'lock': lock, 'input_type': '', 'output_type': ''}


def extend_serialized_witness_args(buffer: bytearray, witness_args: WitnessArgs) -> bytearray:
    # table WitnessArgs
    # {
    #     lock: BytesVec,
    #     input_type: BytesVec,
    #     output_type: BytesVec,
    # }

    witness_args_header = HeaderBuilder(buffer, 3)

    extend_bytes_fixvec(buffer, witness_args['lock'])
    witness_args_header.finish_item()

    if witness_args['input_type'] != '' and witness_args['input_type'] != '0x':
        extend_bytes_fixvec(buffer, witness_args['input_type'])
    witness_args_header.finish_item()

    if witness_args['input_type'] != '' and witness_args['output_type'] != '0x':
        extend_bytes_fixvec(buffer, witness_args['output_type'])
    witness_args_header.finish_item()

    return buffer

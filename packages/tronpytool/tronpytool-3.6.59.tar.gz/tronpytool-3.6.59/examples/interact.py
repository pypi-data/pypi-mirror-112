#!/usr/bin/env python
# coding: utf-8

from attrdict import AttrDict
from tronpytool.common import abi

from common.abi import method_result_handler
from tronpytool import Tron

tron = Tron().setNetwork('nile')
private_key = '444e82ce44f09f701e0b09f5773a0cc6823bf100b4e83552ba804388ab12db9d'
wallet_address = 'TR3TEXGWZvY5DZryrQx6bkmCK6whBr7SE4'
# contract = 'TRXut9s5NKLtXYw8Fj7ze4jUuHyLuHkYxw'
contract = 'TAgtKZmFtS8Mv94VVBKVFs72jjsCSJmXEi'
tron.private_key = private_key
tron.default_address = wallet_address
debug_health_contract = False
"""
data = {'contract_address': 'TRXut9s5NKLtXYw8Fj7ze4jUuHyLuHkYxw', 'function_selector': 'name()',
        'issuer_address': AttrDict({'hex': '41A5576E55542477CE999F2D3A8C242697B0FCF416',
                                    'base58': 'TR3TEXGWZvY5DZryrQx6bkmCK6whBr7SE4'}), 'fee_limit': 30000,
        'call_value': 0,
        'token_value': 0, 'token_id': 0, 'parameters': []}
"""

data = {'contract_address': 'TAgtKZmFtS8Mv94VVBKVFs72jjsCSJmXEi', 'function_selector': 'whatTime()',
        'issuer_address': AttrDict(
            {'hex': '41A5576E55542477CE999F2D3A8C242697B0FCF416', 'base58': 'TR3TEXGWZvY5DZryrQx6bkmCK6whBr7SE4'}),
        'fee_limit': 30000, 'call_value': 0, 'token_value': 0, 'token_id': 0, 'parameters': []}

if debug_health_contract:
    collection = tron.Chain.get_contract(contract)
    print('Transaction: ')
    print(collection)
    print('-----------')

get_name_tx = tron.transaction_builder.trigger_smart_contract(data)

ok, constant_result, transaction_detail = method_result_handler(get_name_tx)

"""
def parse_output(self, raw: any) -> any:
    if type(raw) is bytes:

        parsed_result = abi.decode_single(self.output_type, bytes.fromhex(raw))
        if len(self.outputs) == 1:
            return parsed_result[0]
        if len(self.outputs) == 0:
            return None
        return parsed_result
    else:
        return raw"""

if ok:
    print("=======debug request result {}".format(constant_result[0]))
    res = constant_result[0]
    decodedbytes = bytes.fromhex(res)
    parse_res = abi.decode_single("", decodedbytes)
    print(parse_res)
    #   print(transaction_detail)
    print("=======end event report ========")
else:
    raise KeyError('Request returns Error - {} msg:{} txt:{}'.format(constant_result, transaction_detail, ""))

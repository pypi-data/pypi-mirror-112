# CKB Python Toolkit

> The library works only with Python 3.

## Installation

```
pip install ckb-toolkit
```

## Quick Start

Install in a virtualenv

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Example

```
from ckb.rpc import rpc
rpc.get_tip_block_number()
```

The [example.py](https://github.com/duanyytop/ckb-python-toolkit/blob/master/example.py) shows how to generate the CKB address and sign the transaction, and then send the transaction to the CKB node.

```
python3 example.py
```

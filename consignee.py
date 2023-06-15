import os
from flask import request, render_template, session, redirect
from typing import List, Tuple
import traceback

from werkzeug.utils import secure_filename

from __init__ import app
from client.signer_impl import Signer_Impl
from eth_utils.address import to_checksum_address
from models import Contracts, Consignee, IPFSObject, db, count_numbers
from blockchain import signin_account, create_account, deploy_contract, call_contract
from crypto import gen_rsakey, shamir_encode, aes_encode
from ipfs import ipfs_client


def load():
    pass


def login(username, password) -> Tuple[Consignee, Signer_Impl]:
    if username == "":
        return None, None  # input error
    consignee = Consignee.query.filter(Consignee.username == username).first()
    if consignee is None:
        # no such user
        return signup(username, password)

    if consignee.password != password:
        return None, None  # password error
    signer = signin_account(username, password)
    if signer is None:
        return None, None  # password error
    return consignee, signer


def signup(username, password) -> Tuple[Consignee, Signer_Impl]:
    try:
        signer = create_account(username, password)

        consignee = Consignee(username=username, password=password)

        contract_addr = deploy_contract("Enterprise", signer=signer)      #合约要改
        consignee.contract_addr = contract_addr
        consignee.account_addr = str(signer.keypair.address)
        consignee.account_pub = str(signer.keypair.public_key)
        consignee.account_priv = str(signer.keypair.private_key)

        privkey, pubkey = gen_rsakey()
        consignee.envelope_pub = pubkey
        consignee.envelope_priv = privkey

        managementAddr = db.session.query(Contracts).filter(Contracts.name == "Management").first().addr

        call_contract(managementAddr, "Management", "addEnterprise",                   #合约要改，addContainer
                      args=[
                          username,
                          to_checksum_address(consignee.account_addr),
                          to_checksum_address(consignee.contract_addr),
                          consignee.envelope_pub, ""])

        db.session.add(consignee)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        return None, None
    return consignee, signer
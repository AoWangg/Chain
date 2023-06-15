import sys
import os
import json
from typing import List, Union
import traceback
import re

# Python SDK path
sys.path.append("/home/aowang/anchan/python-sdk")

from client.bcosclient import BcosClient
from client.bcoserror import BcosError, BcosException
from client.datatype_parser import DatatypeParser
from client.common.compiler import Compiler
from eth_utils import to_checksum_address
from client.signer_impl import Signer_ECDSA, Signer_Impl
from eth_account.account import Account

from client_config import client_config
from models import Contracts, Engineer, db
from config import debug
from __init__ import app

ContractsList = ["Agency", "Arbitrate", "Credit","EngineerList", "Enterprise", "License", "Management","ReportEvaluation", "Accusation","Im_goods", "state","goods", "carrier"]

UniqueContractsList = ["Accusation", "Credit", "EngineerList", "Management","Im_goods", "state","goods", "carrier"]

def create_account(name, password = ""):
    ac = Account.create(password)
    kf = Account.encrypt(ac.privateKey, password)
    keyfile = "{}/{}.keystore".format(client_config.account_keyfile_path, name)

    # if os.access(keyfile, os.F_OK):
    #     common.backup_file(keyfile)

    with open(keyfile, "w") as dump_f:
        json.dump(kf, dump_f)
        dump_f.close()

    return signin_account(name, password)

def signin_account(username, password) -> Union[Signer_Impl, None]:
    try:
        signer = Signer_ECDSA.from_key_file(f"{client_config.account_keyfile_path}/{username}.keystore", password)
    except Exception:
        return None
    return signer

def compile_and_abis(is_compile: bool = True):
    """
    Compiles all contracts and generates abi and bin files 
    """
    for c in ContractsList:
        if is_compile:
            Compiler.compile_file(f"Contracts/{c}.sol", output_path="Contracts")

def deploy_contract(contract, is_compile: bool = False, signer: Signer_Impl = None, fn_args = None):
    """
    Args:
        contract: the contract's name, e.g.: "EngineerList"
        is_compile (bool): compile or not
    Returns:
        the contract address
    """
    if is_compile and (os.path.isfile(client_config.solc_path) or os.path.isfile(client_config.solcjs_path)):
        Compiler.compile_file(f"Contracts/{contract}.sol", output_path="Contracts")

    data_parser = DatatypeParser()
    data_parser.load_abi_file(f"Contracts/{contract}.abi")

    client = BcosClient()
    try:
        with open(f"Contracts/{contract}.bin", 'r') as load_f:
            contract_bin = load_f.read()
            load_f.close()
        result = client.deploy(contract_bin, contract_abi = data_parser.contract_abi, fn_args= fn_args ,from_account_signer=signer)
        addr = result["contractAddress"]
    except BcosError:
        traceback.print_exc()
        return None
    except BcosException:
        traceback.print_exc()
        return None
    except Exception:
        traceback.print_exc()
        return None
    finally:
        client.finish()
    app.logger.info(f"deploy contract {contract} at {addr}")
    return addr

def call_contract(contract_addr: str, contract_name: str, fn_name: str, args: List = None, signer: Signer_Impl = None, gasPrice = 30000000):
    client = BcosClient()

    data_parser: DatatypeParser = DatatypeParser()
    data_parser.load_abi_file(f"Contracts/{contract_name}.abi")
    contract_abi = data_parser.contract_abi

    receipt = client.sendRawTransactionGetReceipt(to_address = contract_addr, contract_abi= contract_abi, fn_name = fn_name, args = args,from_account_signer= signer, gasPrice= gasPrice)

    if receipt["status"] != "0x0":
        msg = receipt.get("statusMsg", "")
        app.logger.warn(f"call contract {contract_name} at {contract_addr}. {fn_name} ({args}) error:{msg}")
        app.logger.warn(f"receipt: {receipt}")
        print(msg)
        raise Exception(f"contract error: {msg}")
    txhash = receipt['transactionHash']
    txresponse = client.getTransactionByHash(txhash)
    inputresult = data_parser.parse_transaction_input(txresponse['input'])
    outputresult = data_parser.parse_receipt_output(inputresult['name'], receipt['output'])
    client.finish()
    app.logger.info(f"call contract {contract_name} at {contract_addr}. {fn_name} ({args}) -> {outputresult}")
    return outputresult

def call_contract2(contract_addr: str, contract_name: str, fn_name: str, args: List = None, signer: Signer_Impl = None):
    client = BcosClient()
    if signer is not None:
        client.default_from_account_signer = signer

    data_parser: DatatypeParser = DatatypeParser()
    data_parser.load_abi_file(f"Contracts/{contract_name}.abi")
    contract_abi = data_parser.contract_abi

    ret = client.call(contract_addr, contract_abi, fn_name, args)
    app.logger.info(f"call contract {contract_name} at {contract_addr}. {fn_name} ({args}) -> {ret}")
    client.finish()
    return ret

def init_accounts():
    password = ""
    container_name = "货物进口商A1"
    consignee_name = "委托人A1"
    carrier_name = "运输机构A1"
    maritime_name = '海事部门A1'

    import container
    import consignee
    import carrier
    import maritime
    cont_1, signer_1 = container.signup(container_name, password)
    app.logger.info(f"创建账户:{cont_1}")
    cons_1, signer_2 = consignee.signup(consignee_name, password)
    app.logger.info(f"创建账户:{cons_1}")
    car_1, signer_3 = carrier.signup(carrier_name, password)
    app.logger.info(f"创建账户:{car_1}")
    marit_1, signer_4 = maritime.signup(maritime_name, password)
    app.logger.info(f"创建账户:{marit_1}")

def ini_all_acounts():
    password = ""
    enterprise_list = [("运输公司A1", "王A", "某某省某某市", "有限责任公司", "危险货物运输")]
    for elem in enterprise_list:
        name = elem[0]
        import enterprise
        ent, signer = enterprise.signup(name, password)
        call_contract(ent.contract_addr, "Enterprise", "setInformation", args = [name, elem[1], elem[2], elem[3], elem[4]], signer = signer)
        app.logger.info(f"创建账户:{ent}")



def init():
    """
    compile all contracts and deploy common contracts
    """

    with app.app_context():
        app.logger.warning("clean databases")
        db.drop_all()
        db.create_all()

        app.logger.warning("compile all contracts")
        compile_and_abis(is_compile=True)

        for c_name in UniqueContractsList:
            addr = deploy_contract(c_name)
            c = Contracts(name=c_name, addr=addr)
            db.session.add(c)
            db.session.commit()

        EngineerListAddr = Contracts.query.filter(Contracts.name == "EngineerList").first().addr
        CreditAddr = Contracts.query.filter(Contracts.name == "Credit").first().addr

        call_contract(EngineerListAddr, "EngineerList", "setCreditContractAddr", args=[to_checksum_address(CreditAddr)])

        if debug:
            init_accounts()

if __name__ == "__main__":
    init()

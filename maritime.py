import os
from flask import request, render_template, session, redirect
from typing import List, Tuple
import traceback

from werkzeug.utils import secure_filename

from __init__ import app
from client.signer_impl import Signer_Impl
from eth_utils.address import to_checksum_address
from models import Contracts, Maritime, Container, IPFSObject, db, count_numbers
from blockchain import signin_account, create_account, deploy_contract, call_contract
from crypto import gen_rsakey, shamir_encode, aes_encode
from ipfs import ipfs_client


def load():
    pass


def login(username, password) -> Tuple[Maritime, Signer_Impl]:
    if username == "":
        return None, None  # input error
    maritime = Maritime.query.filter(Maritime.username == username).first()
    if maritime is None:
        # no such user
        return signup(username, password)

    if maritime.password != password:
        return None, None  # password error
    signer = signin_account(username, password)
    if signer is None:
        return None, None  # password error
    return maritime, signer


def signup(username, password) -> Tuple[Maritime, Signer_Impl]:
    try:
        signer = create_account(username, password)

        maritime = Maritime(username=username, password=password)

        contract_addr = deploy_contract("Enterprise", signer=signer)      #合约要改
        maritime.contract_addr = contract_addr
        maritime.account_addr = str(signer.keypair.address)
        maritime.account_pub = str(signer.keypair.public_key)
        maritime.account_priv = str(signer.keypair.private_key)

        privkey, pubkey = gen_rsakey()
        maritime.envelope_pub = pubkey
        maritime.envelope_priv = privkey

        managementAddr = db.session.query(Contracts).filter(Contracts.name == "Management").first().addr

        call_contract(managementAddr, "Management", "addEnterprise",                   #合约要改，addContainer
                      args=[
                          username,
                          to_checksum_address(maritime.account_addr),
                          to_checksum_address(maritime.contract_addr),
                          maritime.envelope_pub, ""])

        db.session.add(maritime)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        return None, None
    return maritime, signer


@app.route("/maritime", methods=["GET", "POST"])
def maritime():
    if request.method == "GET":
        username = session.get("username", "")
        password = session.get("password", "")
        maritime, signer = login(username, password)

        if maritime is None or signer is None:
            return render_template("maritime2.html", is_login=False)            #页面需修改
        return render_template("maritime2.html", is_login=True, maritime=maritime, username=username)


    username = request.form.get("name", "")
    password = request.form.get("password", "")
    maritime, signer = login(username, password)

    if maritime is None or signer is None:
        return render_template("maritime2.html", is_login=False, fail_msg="登录失败")

    session["username"] = username
    session["password"] = password


    return render_template("maritime2.html", is_login=True, succ_msg="登录成功", maritime=maritime, username=username)




@app.route("/maritime/get_goods_info",methods=["GET", "POST"])

def maritime_get_goods_info():

    username = session.get("username", "")
    password = session.get("password", "")
    maritime, signer = login(username, password)


    if maritime is None:
        return redirect("/maritime")

    if request.method == "GET":
        return render_template("maritime2-1.html", is_login = True, maritime = maritime, username = username)

    container_name = request.form.get("container-name")
    goods_Addr = db.session.query(Contracts).filter(Contracts.name == "Im_goods").first().addr
    # ma_Addr = db.session.query(Contracts).filter(Contracts.name == "Management").first().addr
    # container_addr = call_contract(ma_Addr, "Management", "getEnterpriseAccountAddr", args=['huowu'],
    #                         signer=signer)


    try:
        container_ = Container.query.filter(Container.username == 'huowu').first()
        container_addr = container_.account_addr
        # container_addr = Container.query.filter(Container.username == container_name).first().account_addr
        Goodsdata = call_contract(goods_Addr, "Im_goods", "getGoodsReports", args=[str(container_addr)],
                            signer=signer)
        goodsdata = list(zip(*Goodsdata))
        state_Addr = db.session.query(Contracts).filter(Contracts.name == "state").first().addr
        # call_contract(state_Addr, "TraceableSmartContract", "start",
        #               args=[goods_id, state_Addr, container.account_addr, haishi_addr], signer=signer)

    except Exception:
        return render_template("maritime2-2.html", is_login = True, fail_msg = "查找信息失败", maritime=maritime, username = username)

    return render_template("maritime2-2.html", is_login=True, succ_msg = "查找信息成功", maritime=maritime,  username=username, goodsdata=goodsdata)


import os
from flask import request, render_template, session, redirect
from typing import List, Tuple
import traceback

from werkzeug.utils import secure_filename

from __init__ import app
from client.signer_impl import Signer_Impl
from eth_utils.address import to_checksum_address
from models import Contracts, Carrier, IPFSObject, db, count_numbers, Transport
from blockchain import signin_account, create_account, deploy_contract, call_contract
from crypto import gen_rsakey, shamir_encode, aes_encode
from ipfs import ipfs_client


def load():
    pass


def login(username, password) -> Tuple[Carrier, Signer_Impl]:
    if username == "":
        return None, None  # input error
    carrier = Carrier.query.filter(Carrier.username == username).first()
    if carrier is None:
        # no such user
        return signup(username, password)

    if carrier.password != password:
        return None, None  # password error
    signer = signin_account(username, password)
    if signer is None:
        return None, None  # password error
    return carrier, signer


def signup(username, password) -> Tuple[Carrier, Signer_Impl]:
    try:
        signer = create_account(username, password)

        carrier = Carrier(username=username, password=password)

        contract_addr = deploy_contract("Enterprise", signer=signer)      #合约要改
        carrier.contract_addr = contract_addr
        carrier.account_addr = str(signer.keypair.address)
        carrier.account_pub = str(signer.keypair.public_key)
        carrier.account_priv = str(signer.keypair.private_key)

        privkey, pubkey = gen_rsakey()
        carrier.envelope_pub = pubkey
        carrier.envelope_priv = privkey

        managementAddr = db.session.query(Contracts).filter(Contracts.name == "Management").first().addr

        call_contract(managementAddr, "Management", "addEnterprise",                   #合约要改，addContainer
                      args=[
                          username,
                          to_checksum_address(carrier.account_addr),
                          to_checksum_address(carrier.contract_addr),
                          carrier.envelope_pub, ""])

        db.session.add(carrier)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        return None, None
    return carrier, signer

@app.route("/carrier", methods=["GET", "POST"])
def carrier():
    if request.method == "GET":
        username = session.get("username", "")
        password = session.get("password", "")
        carrier, signer = login(username, password)
        if carrier is None or signer is None:
            return render_template("carrier2.html", is_login=False)            #页面需修改


        return render_template("carrier2.html", is_login=True, carrier=carrier,
            username=username)



    username = request.form.get("name", "")
    password = request.form.get("password", "")
    carrier, signer = login(username, password)

    if carrier is None or signer is None:
        return render_template("carrier2.html", is_login=False, fail_msg="登录失败")

    session["username"] = username
    session["password"] = password

    Addr = db.session.query(Contracts).filter(Contracts.name == "carrier").first().addr

    try:
        fileData = call_contract(Addr, "carrier", "getAllData", signer=signer)

        filedata = list(zip(*fileData))

    except Exception:
        return render_template("carrier2.html", is_login=True, succ_msg="登录成功", carrier=carrier,
                               username=username)

    return render_template("carrier2.html", is_login=True, succ_msg="登录成功", carrier=carrier, username=username, filedata=filedata)


@app.route("/carrier/upload", methods=["GET", "POST"])
def carrier_upload():
    username = session.get("username", "")
    password = session.get("password", "")
    carrier, signer = login(username, password)

    if carrier is None:
        return redirect("/carrier")

    if request.method == "GET":
        return render_template("carrier2-1.html", is_login=True, carrier=carrier, username=username)

    data_hash = request.form.get("data-hash")
    data_file = request.files.get("data-file")

    if data_file is None:
        return render_template("carrier2-1.html", is_login=True, carrier=carrier, username=username,
                               fail_msg="缺少上传文件")
    if data_file.filename == "":
        return render_template("carrier2-1.html", is_login=True, carrier=carrier, username=username,
                               fail_msg="缺少上传文件")

    data_file_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(data_file.filename))
    data_file.save(data_file_path)

    try:
        _, _, _, _, _, _,n, _ = count_numbers()
        t = 3
        key, shares = shamir_encode(t, n)

        enc_data_path = os.path.join(app.config["UPLOAD_FOLDER"], "enc-" + secure_filename(data_file.filename))
        aes_encode(key, data_file_path, enc_data_path)

        data_file_addr = ipfs_client.add(enc_data_path)

        for i, transport in enumerate(Transport.query.all()):
            obj_data = IPFSObject(hash=data_file_addr["Hash"], name=secure_filename(data_file.filename),
                                  secret=shares[i][1].hex(), idx=shares[i][0])
            transport.files.append(obj_data)
            db.session.add(obj_data)
            db.session.commit()
    except Exception as e:
        traceback(e)
        return render_template("carrier2-1.html", is_login=True, carrier=carrier, username=username,
                               succ_msg="IPFS上传失败")

    try:
        Addr = db.session.query(Contracts).filter(Contracts.name == "carrier").first().addr
        call_contract(Addr, "carrier", "addData", args=[data_hash, data_file_addr["Hash"]],
                      signer=signer)
    except Exception as e:
        traceback(e)
        return render_template("carrier2-1.html", is_login=True, carrier=carrier, username=username,
                               succ_msg="智能合约调用失败")
    return render_template("carrier2-1.html", is_login=True, carrier=carrier, username=username,
                           succ_msg="添加成功")
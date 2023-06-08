**仅学习使用**

本文档提供了安产链项目的部署和运行指引。我们主要使用了 FISCO BCOS 区块链及其 Python SDK 、 IPFS 星际文件系统、 WeBase 区块链开发平台、 Truora 预言机以及 Hyperledger Caliper 压力测试平台。

## 一、基本运行环境

安产链项目在 Ubuntu 20.04 操作系统上编译部署成功，系统运行于本地 8C8G 虚拟机上。本项目使用的基本框架及其版本是：

|  依赖   | 版本  |
|  ----  | ----  |
| Python  | 3.8 |
| pip    | 21.3.1 |
| Java  | openjdk-11 |
| Node.js  | 8.17.0 |
| npm    | 6.13.4 |
| docker | 20.10.7|
| docker-compose | 1.25.0 |

环境准备
```sh
sudo apt install -y openssl curl
# 安装默认Java版本(Java 8或以上)
sudo apt install -y default-jdk
# 查询Java版本
java -version

#环境变量设置
gedit /etc/profile

JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
JRE_HOME=$JAVA_HOME/jre
CLASS_PATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
export JAVA_HOME JRE_HOME CLASS_PATH PATH

source /etc/profile

// 添加仓库，回车继续
sudo add-apt-repository ppa:deadsnakes/ppa
// 安装python 3.8
sudo apt-get install -y python3.8
sudo apt-get install -y python3-pip
```


## 二、Fisco BCOS 区块链

可以使用 FISCO BCOS v2.8.0 项目及其文档推荐的 `build_chain.sh` 脚本快速搭建和部署区块链平台，具体使用的命令是

```sh
cd ~ 
mkdir anchan & cd anchan
curl -LO https://github.com/FISCO-BCOS/FISCO-BCOS/releases/download/v2.8.0/build_chain.sh && chmod u+x build_chain.sh #下载脚本
curl -#LO https://osp-1257653870.cos.ap-guangzhou.myqcloud.com/FISCO-BCOS/FISCO-BCOS/releases/v2.9.1/build_chain.sh && chmod u+x build_chain.sh  #网络差
bash build_chain.sh -l 127.0.0.1:8 -p 30300,20200,8545 #部署4个节点
./nodes/127.0.0.1/start_all.sh #启动所有节点
```

## 三、 Python SDK

我们的项目是基于 Python 语言开发的，因此需要使用 FISCO BCOS 平台提供的 Python SDK 和区块链节点进行交互。

### 3.1 拉取 Python SDK 源代码

```sh
git clone https://github.com/FISCO-BCOS/python-sdk #克隆仓库
cd python-sdk
pip install -r requirements.txt 
bash init_env.sh -i
npm install solc@v0.4.25
cp ~/anchan/nodes/127.0.0.1/sdk/* ./bin #复制证书
```

### 3.2 测试 Python SDK 和节点的连通性

我们使用如下命令和 FISCO BCOS 区块链中的节点进行交互。

```sh
chmod 755 ./console2.py
sudo ln -s /usr/bin/python3 /usr/bin/python
./console2.py getNodeVersion #检查SDK能否连接节点。

#输出如下即可：
INFO >> BcosClient:  channel 127.0.0.1:20200,groupid :1,crypto type:ECDSA,ssl type:ECDSA
INFO : getNodeVersion
     : {
    "Build Time": "20210830 12:52:15",
    "Build Type": "Linux/clang/Release",
    "Chain Id": "1",
    "FISCO-BCOS Version": "2.8.0",
    "Git Branch": "HEAD",
    "Git Commit Hash": "30fb38ac5692468058abf6aa12869d2ae776c275",
    "Supported Version": "2.8.0"
}

```
## 四、 IPFS 集群

我们部署了 IPFS 节点用于分布式文件存储。我们使用了 IPFS 文档推荐的 docker-compose 方法如下部署了四个节点的私有 IPFS 集群。使用者可以根据实际情况修改节点数量。具体的部署命令是：

``` bash
wget https://dist.ipfs.io/ipfs-cluster-ctl/v0.14.0/ipfs-cluster-ctl_v0.14.0_linux-amd64.tar.gz
tar xvzf ipfs-cluster-ctl_v0.14.0_linux-amd64.tar.gz
wget https://raw.githubusercontent.com/ipfs/ipfs-cluster/master/docker-compose.yml

#要修改docker-compose.yml

```
安产链项目使用名为 ipfshttpclient 的 Python 库实现 IPFS 文件系统的调用。但是，由于 ipfshttpclient 的版本限制，需要修改源码如下：
（在执行完Chain项目的requirement.txt后再修改）
``` sh
cd $HOME/.local/lib/python3.8/site-packages/ipfshttpclient/client
# 将__init__.py中的VERSION_MAXIMUM改为：
VERSION_MAXIMUM   = "0.19.3"
```

之后，回到ipfs-cluster-clt文件夹，利用docker-compose启动容器。

```
sudo snap install docker
sudo apt  install docker-compose
sudo docker-compose up -d
#或者
sudo docker-compose up 
```

***值得注意的是，我们修改了 docker-compose.yml 文件，使得其 node1 的相关端口被转发出来，以实现远程接入，要按照需求进行修改***

```
version: '3.4'

# This is an example docker-compose file to quickly test an IPFS Cluster
# with multiple peers on a contained environment.

# It runs 3 cluster peers (cluster0, cluster1...) attached to kubo daemons
# (ipfs0, ipfs1...) using the CRDT consensus component. Cluster peers
# autodiscover themselves using mDNS on the docker internal network.
#
# To interact with the cluster use "ipfs-cluster-ctl" (the cluster0 API port is
# exposed to the locahost. You can also "docker exec -ti cluster0 sh" and run
# it from the container. "ipfs-cluster-ctl peers ls" should show all 3 peers a few
# seconds after start.
#
# For persistence, a "compose" folder is created and used to store configurations
# and states. This can be used to edit configurations in subsequent runs. It looks
# as follows:
#
# compose/
# |-- cluster0
# |-- cluster1
# |-- ...
# |-- ipfs0
# |-- ipfs1
# |-- ...
#
# During the first start, default configurations are created for all peers.

services:

##################################################################################
## Cluster PEER 0 ################################################################
##################################################################################

  ipfs0:
    container_name: ipfs0
    image: ipfs/kubo:release
    ports:
      - "4001:4001" # ipfs swarm - expose if needed/wanted
      - "5001:5001" # ipfs api - expose if needed/wanted
      - "8080:8080" # ipfs gateway - expose if needed/wanted
    volumes:
      - ./compose/ipfs0:/data/ipfs

  cluster0:
    container_name: cluster0
    image: ipfs/ipfs-cluster:latest
    depends_on:
      - ipfs0
    environment:
      CLUSTER_PEERNAME: cluster0
      CLUSTER_SECRET: ${CLUSTER_SECRET} # From shell variable if set
      CLUSTER_IPFSHTTP_NODEMULTIADDRESS: /dns4/ipfs0/tcp/5001
      CLUSTER_CRDT_TRUSTEDPEERS: '*' # Trust all peers in Cluster
      CLUSTER_RESTAPI_HTTPLISTENMULTIADDRESS: /ip4/0.0.0.0/tcp/9094 # Expose API
      CLUSTER_MONITORPINGINTERVAL: 2s # Speed up peer discovery
    ports:
          # Open API port (allows ipfs-cluster-ctl usage on host)
          - "127.0.0.1:9094:9094"
          # The cluster swarm port would need  to be exposed if this container
          # was to connect to cluster peers on other hosts.
          # But this is just a testing cluster.
          # - "9095:9095" # Cluster IPFS Proxy endpoint
          # - "9096:9096" # Cluster swarm endpoint
    volumes:
      - ./compose/cluster0:/data/ipfs-cluster

##################################################################################
## Cluster PEER 1 ################################################################
##################################################################################

# See Cluster PEER 0 for comments (all removed here and below)
  ipfs1:
    container_name: ipfs1
    image: ipfs/kubo:release
    volumes:
      - ./compose/ipfs1:/data/ipfs

  cluster1:
    container_name: cluster1
    image: ipfs/ipfs-cluster:latest
    depends_on:
      - ipfs1
    environment:
      CLUSTER_PEERNAME: cluster1
      CLUSTER_SECRET: ${CLUSTER_SECRET}
      CLUSTER_IPFSHTTP_NODEMULTIADDRESS: /dns4/ipfs1/tcp/5001
      CLUSTER_CRDT_TRUSTEDPEERS: '*'
      CLUSTER_MONITORPINGINTERVAL: 2s # Speed up peer discovery
    volumes:
      - ./compose/cluster1:/data/ipfs-cluster

##################################################################################
## Cluster PEER 2 ################################################################
##################################################################################

# See Cluster PEER 0 for comments (all removed here and below)
  ipfs2:
    container_name: ipfs2
    image: ipfs/kubo:release
    volumes:
      - ./compose/ipfs2:/data/ipfs

  cluster2:
    container_name: cluster2
    image: ipfs/ipfs-cluster:latest
    depends_on:
      - ipfs2
    environment:
      CLUSTER_PEERNAME: cluster2
      CLUSTER_SECRET: ${CLUSTER_SECRET}
      CLUSTER_IPFSHTTP_NODEMULTIADDRESS: /dns4/ipfs2/tcp/5001
      CLUSTER_CRDT_TRUSTEDPEERS: '*'
      CLUSTER_MONITORPINGINTERVAL: 2s # Speed up peer discovery
    volumes:
      - ./compose/cluster2:/data/ipfs-cluster

# For adding more peers, copy PEER 1 and rename things to ipfs2, cluster2.
# Keep bootstrapping to cluster0.
```




## 五、安产链项目

安产链项目的源代码部署在github网站上。使用如下命令运行安产链项目：

```sh
git clone https://github.com/AAooWW/Chain.git #拉取源代码

cd Chain
pip install -r requirements.txt
mkdir -p ./bin/logs
cp -r ${PATH_TO_PYTHON_SDK}/bin/* ./bin #将python-sdk的bin文件夹内容复制bin中
```

我们需要修改 `client_config.py` 文件夹如下：将 `${PATH_TO_PYTHON_SDK}`设置为Python SDK路径，将`${PATH_TO_ANCAHNCHAIN_PROJECT}` 设置为安产链项目代码路径。

```py 
    channel_ca = "${PATH_TO_PYTHON_SDK}/bin/ca.crt"  # 采用channel协议时，需要设置链证书,如采用rpc协议通信，这里可以留空
    channel_node_cert = "${PATH_TO_PYTHON_SDK}/bin/sdk.crt"  # 采用channel协议时，需要设置sdk证书,如采用rpc协议通信，这里可以留空
    channel_node_key = "${PATH_TO_PYTHON_SDK}/bin/sdk.key"   # 采用channel协议时，需要设置sdk私钥,如采用rpc协议通信，这里可以留空

    # ---------account &keyfile config--------------
    contract_info_file = "${PATH_TO_ANCHANCHAIN_PROJECT}/bin/contract.ini"  # 保存已部署合约信息的文件
    account_keyfile_path = "${PATH_TO_ANCHANCHAIN_PROJECT}/bin/accounts"  # 保存keystore文件的路径，在此路径下,keystore文件以 [name].keystore命名
    account_keyfile = "pyaccount.keystore"
    account_password = "123456"  # 实际使用时建议改为复杂密码
    gm_account_keyfile = "gm_account.json"  # 国密账号的存储文件，可以加密存储,如果留空则不加载
    gm_account_password = "123456"  # 如果不设密码，置为None或""则不加密
    
    # ---------console mode, support user input--------------
    background = True

    # ---------runtime related--------------
    # path of solc compiler
    solc_path = "${PATH_TO_PYTHON_SDK}/bin/solc/v0.4.25/solc"
    gm_solc_path = "${PATH_TO_PYTHON_SDK}/bin/solc/v0.4.25/solc-gm"
    solcjs_path = "${PATH_TO_PYTHON_SDK}/solcjs"

    logdir = "${PATH_TO_ANCHANCHAIN_PROJECT}/bin/logs"  # 默认日志输出目录，该目录必须先建立
```

之后，我们可以尝试启动安产链项目：

```sh
python blockchain.py #启动SDK，编译、部署并初始化所有智能合约，
python app.py #启动flask服务
```

至此，我们已经可以运行安产链的绝大部分功能了。但是为了开发和使用，我们还可以部署如下一些 FISCO BCOS 中间件。
## 六、 WeBASE 智能合约开发和中控屏

WeBASE 提供了方便的智能合约开发和调试平台，本节内容介绍 WeBASE 的部署方案。

### 6.1 Mysql 数据库部署
使用如下命令部署 Mysql 数据库：

```sh
docker pull mysql:5.6
sudo apt install mariadb-client-core-10.3 
pip3 install PyMySQL
```

### 6.2 WeBASE 部署

使用如下命令即可获取 WeBase 代码并配置相关文件：

```sh
wget https://osp-1257653870.cos.ap-guangzhou.myqcloud.com/WeBASE/releases/download/v1.5.3/webase-deploy.zip
unzip webase-deploy.zip && cd webase-deploy
mkdir sqlConf sqlData sqlLogs
docker run -p 3306:3306 --name mysql56 -v $PWD/sqlConf:/etc/mysql/conf.d -v $PWD/sqlLogs:/logs -v $PWD/sqlData:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.6

```

我们注意到，需要修改 `webase-deploy/comm/check.py`, 将 47 行 `checkExitedChainInfo()` 注释掉。否则 WeBASE 无法运行。

### 6.3 修改commom-properties 配置文件
我们需要进一步配置 WeBASE的相关信息，用于数据库接入等。

``` sh
[common]

# Webase Subsystem Version (v1.1.0 or above)
webase.web.version=v1.5.3
webase.mgr.version=v1.5.3
webase.sign.version=v1.5.3
webase.front.version=v1.5.3

#####################################################################
# if use [installDockerAll] to install WeBASE by docker
# if use [installAll] or [installWeBASE], ignore configuration here

# 1: enable mysql in docker
# 0: mysql run in host, required fill in the configuration of webase-node-mgr and webase-sign
docker.mysql=1

# if [docker.mysql=1], mysql run in host (only works in [installDockerAll])
# run mysql 5.6 by docker
docker.mysql.port=23306
# default user [root]
docker.mysql.password=123456
#####################################################################

# Mysql database configuration of WeBASE-Node-Manager
mysql.ip=127.0.0.1
mysql.port=3306
mysql.user=root
mysql.password=123456
mysql.database=webasenodemanager

# Mysql database configuration of WeBASE-Sign
sign.mysql.ip=127.0.0.1
sign.mysql.port=3306
sign.mysql.user=root
sign.mysql.password=123456
sign.mysql.database=webasesign
# if docker mysql disabled[docker.mysql=0] above

# H2 database name of WeBASE-Front (docker mode ignore this)
front.h2.name=webasefront
front.org=fisco

# WeBASE-Web service port 
web.port=5100
# enable WeBASE-Web overview pages for mobile phone(docker mode not support h5 yet)
# (0: disable, 1: enable)
web.h5.enable=1

# WeBASE-Node-Manager service port
mgr.port=5101

# WeBASE-Front service port
front.port=5102

# WeBASE-Sign service port
sign.port=5104

# Node listening IP
node.listenIp=127.0.0.1
# Node p2p service port
node.p2pPort=30300
# Node channel service port
node.channelPort=20200
# Node rpc service port
node.rpcPort=8545

# Encrypt type (0: standard, 1: guomi)
encrypt.type=0
# ssl encrypt type (0: standard ssl, 1: guomi ssl)
# only guomi type support guomi ssl
encrypt.sslType=0

# Use existing chain or not (yes/no)
if.exist.fisco=yes

### if build new chain, [if.exist.fisco=no]
# Configuration required when building a new chain 
# Fisco-bcos version
fisco.version=2.8.0
# Number of building nodes (default value: 2)
node.counts=nodeCounts

### if using exited chain, [if.exist.fisco=yes]
# The path of the existing chain, the path of the start_all.sh script
# Under the path, there should be a 'sdk' directory where the SDK certificates (ca.crt, sdk.crt, node.key and gm directory(gm ssl)) are stored
fisco.dir=/home/aowang/anchan/nodes/127.0.0.1
# Node directory in [fisco.dir] for WeBASE-Front to connect 
# example: 'node.dir=node0' would auto change to '/data/app/nodes/127.0.0.1/node0'
# Under the path, there is a conf directory where node certificates (ca.crt, node.crt and node.key) are stored
node.dir=node0

```
### 6.4 启动 WeBASE 组件

使用如下命令启动 WeBASE 组件。

```sh
python deploy.py installAll # 启动WeBASE服务
```

## 七、 Truora 可信预言机

我们的项目使用了 FISCO BCOS 的可信预言机组件实现审查实体和仲裁实体的随机选取。因此，需要不熟 Truora 可信预言机组件。

### 7.1 拉取源码

使用如下命令拉取 Truora 项目源码：

```sh
wget "https://github.com/WeBankBlockchain/Truora-Service/releases/download/v1.1.0/docker-deploy.zip"
unzip docker-deploy.zip -d docker-deploy # 必须加-d 参数，否则会将所有内容解压到当前文件夹
```

### 7.2 创建数据库
使用如下 mysql 语句创建 Truora 所需的数据库：

``` sh 
mysql -h 127.0.0.1 -P 3306 -u root -p
> CREATE DATABASE `truora`;
```

### 7.3 进一步修改配置文件

由于 docker 已经启动了。但是，我们发现当使用普通用户的权限时，运行 `deploy_single.sh` 脚本是无法使用的。因此，我们使用命令 `systemctl start docker` 启动docker。 之后，将 `docker-deploy/util/utils.sh` 的 135 行的内容 `systemctl start docker` 注释掉，以跳过启动 truora-web 和 truora-service 容器启动后检查端口部分。还需要将 `docker-deploy/start.sh` 的 59-67 行代码注释。

> 注：节点sdk文件夹中没有 `node.key` 和 `node.crt` 文件，必须要将某个区块链节点的 `conf` 文件夹中的 `node.key` 和 `node.crt` 复制到 sdk 文件夹中。

### 7.4 启动docker-deploy 

我们使用如下命令启动 Truora：

```sh
bash deploy_single.sh -d
```

## 八、压力测试工具 Hyperledger Caliper 
最后，我们使用 Caliper 工具实现了自动化的区块链智能合约压力测试和性能评估。

### 8.1 获取 Caliper 代码

使用如下命令获取 Caliper 的基本代码
```sh
mkdir benchmarks && cd benchmarks
nvm use 8
nvm init
npm install --only=prod @hyperledger/caliper-cli@0.2.0
npx caliper bind --caliper-bind-sut fisco-bcos --caliper-bind-sdk latest
git clone https://github.com/vita-dounai/caliper-benchmarks.git
```

### 8.2 修改 Caliper 源码
我们发现， Caliper 项目无法正常启动。通过阅读[issue1248](https://github.com/FISCO-BCOS/FISCO-BCOS/issues/1248)相关描述和 [pull request 647](https://github.com/hyperledger/caliper/pull/647/files)，我们修改了一下文件： `benchmarks/node_modules/@hyperledger/caliper-fisco-bcos/lib/channelPromise.js` 、 `benchmarks/node_modules/@hyperledger/caliper-fisco-bcos/lib/fiscoBcos.js` 、 `benchmarks/node_modules/@hyperledger/caliper-fisco-bcos/lib/web3lib/web3sync.js`。

根据 [issue1721](https://github.com/FISCO-BCOS/FISCO-BCOS/issues/1721#event-3661578575)， 我们修改了 `benchmarks/node_modules/@hyperledger/caliper-fisco-bcos/package.json` 中的 `dependencies` 并添加一项 `"secp256k1": "^3.8.0"` 并执行 `npm -i `。

### 8.3 创建账户
使用如下命令创建账户：
```
cd ${PATH_TO_PYTHON_SDK}
./console.py newaccount ${newAccount} ${accountPrivkey}
```
### 8.4 修改fisco-bcos.json 配置文件

由于我们使用本地方式构建了 FISCO 区块链系统，因此需要创建新账户并修改 `benchmarks/caliper-benchmarks/networks/fisco-bcos/4nodes1group/fisco-bcos.json` 配置文件。

> 注1：填写私钥 ·${accountPrivkey}· 时要删掉 `0x` 前缀
> 注2：节点 sdk 文件夹中没有 `node.key` 和 `node.crt` 文件，必须要将任意区块链节点的 conf 文件夹中的  `node.key` 和 `node.crt` 复制到 sdk 文件夹中。最后，我们的 json 配置文件是：

```json
{
    "caliper": {
        "blockchain": "fisco-bcos"
    },
    "fisco-bcos": {
        "config": {
            "privateKey": "${accountPrivkey}", 
            "account": "${newAccount}"
        },
        "network": {
            "nodes": [
                {
                    "ip": "127.0.0.1",
                    "rpcPort": "8545",
                    "channelPort": "20200"
                },
                {
                    "ip": "127.0.0.1",
                    "rpcPort": "8546",
                    "channelPort": "20201"
                },
                {
                    "ip": "127.0.0.1",
                    "rpcPort": "8547",
                    "channelPort": "20202"
                },
                {
                    "ip": "127.0.0.1",
                    "rpcPort": "8548",
                    "channelPort": "20203"
                }
            ],
            "authentication": {
                "key": "/home/ubuntu/anchan/nodes/127.0.0.1/sdk/node.key",
                "cert": "/home/ubuntu/anchan/nodes/127.0.0.1/sdk/node.crt",
                "ca": "/home/ubuntu/anchan/nodes/127.0.0.1/sdk/ca.crt"
            },
            "groupID": 1,
            "timeout": 100000
        }
    }{以下省略}
}

```

### 8.5 执行 HelloWorld 合约测试
我们使用了如下命令对 HelloWorld 智能合约进行性能测试。

```
npx caliper benchmark run --caliper-workspace caliper-benchmarks --caliper-benchconfig benchmarks/samples/fisco-bcos/helloworld/config.yaml  --caliper-networkconfig networks/fisco-bcos/4nodes1group/fisco-bcos.json
```

之后，就可以对安产链相关的智能合约进行性能和压力测试。

pragma solidity 0.4.25;
pragma experimental ABIEncoderV2;



contract carrier {
    mapping(uint => string) private encryptedDataIpfsList; // 储存所有encryptedDataIpfs
    mapping(uint => string) private encryptedDataHashList; // 储存所有encryptedDataHash
    uint private dataCount = 0; // 储存数据个数

    function addData(string _dataHash, string _dataIpfs) public {
        encryptedDataIpfsList[dataCount] = _dataIpfs;
        encryptedDataHashList[dataCount] = _dataHash;
        dataCount += 1;
    }

    function getAllData() public view returns (string[], string[]) {
        string[] memory dataIpfsList = new string[](dataCount);
        string[] memory dataHashList = new string[](dataCount);

        for (uint i = 0; i < dataCount; i++) {
            dataIpfsList[i] = encryptedDataIpfsList[i];
            dataHashList[i] = encryptedDataHashList[i];
        }

        return (dataIpfsList, dataHashList);
    }
}


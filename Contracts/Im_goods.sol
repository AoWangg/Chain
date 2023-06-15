pragma solidity 0.4.25;

pragma experimental ABIEncoderV2;

contract Im_goods {

    struct GoodsInfo {
        uint256 goodsId;
        string goodsType;
        string goodsName;
        uint256 goodsHe;
        string submitter;
    }

    mapping (uint256 => GoodsInfo) private goodsInfoMap;
    uint256[] private goodsIds;

    event LogGoodsInfo(uint256 goodsId, string goodsType, string goodsName, uint256 goodsHe, string submitter);

    function reportGoodsInfo(uint256 goodsId, string goodsType, string goodsName, uint256 goodsHe, string submitter) public {
        require(goodsInfoMap[goodsId].goodsHe == 0, "Goods with this id already exists");

        GoodsInfo memory newGoodsInfo = GoodsInfo(goodsId, goodsType, goodsName, goodsHe, submitter);
        goodsInfoMap[goodsId] = newGoodsInfo;
        goodsIds.push(goodsId);

        emit LogGoodsInfo(goodsId, goodsType, goodsName, goodsHe, submitter);
    }

    function getGoodsById(uint256 goodsId) public view returns (string, string, uint256, string) {
        GoodsInfo storage goodsInfo = goodsInfoMap[goodsId];
        require(goodsInfo.goodsHe > 0, "Goods with this id does not exist");

        return (goodsInfo.goodsType, goodsInfo.goodsName, goodsInfo.goodsHe, goodsInfo.submitter);
    }

    function getGoodsIds() public view returns (uint256[]) {
        return goodsIds;
    }

    function getGoodsReports(string memory submitter) public view returns (uint[], string[], string[], uint[]) {
        uint256 count = 0;
        for (uint256 i = 0; i < goodsIds.length; i++) {
            if (keccak256(abi.encodePacked(goodsInfoMap[goodsIds[i]].submitter)) == keccak256(abi.encodePacked(submitter))) {
                count++;
            }
        }

        uint[] memory ids = new uint[](count);
        string[] memory goodsTypes = new string[](count);
        string[] memory goodsNames = new string[](count);
        uint[] memory goodsHes = new uint[](count);

        count = 0;
        for (uint256 j = 0; j < goodsIds.length; j++) {
            if (keccak256(abi.encodePacked(goodsInfoMap[goodsIds[j]].submitter)) == keccak256(abi.encodePacked(submitter))) {
                ids[count] = goodsInfoMap[goodsIds[j]].goodsId;
                goodsTypes[count] = goodsInfoMap[goodsIds[j]].goodsType;
                goodsNames[count] = goodsInfoMap[goodsIds[j]].goodsName;
                goodsHes[count] = goodsInfoMap[goodsIds[j]].goodsHe;
                count++;
            }
        }

        return (ids, goodsTypes, goodsNames, goodsHes);
    }
}
pragma solidity 0.4.25;
pragma experimental ABIEncoderV2;

contract goods {

    struct GoodsInfo {
        uint256 goodsId;
        string goodsType;
        string goodsName;
        uint256 goodsHe;
        string submitter;
        string bumen;
    }

    mapping(uint256 => GoodsInfo[]) goodsInfoMap;
    uint256[] goodsIds;

    function addGoodsInfo(uint256 goodsId, string memory goodsType, string memory goodsName, uint256 goodsHe, string memory submitter, string memory bumen) public {
        GoodsInfo memory newGoodsInfo = GoodsInfo({
            goodsId:goodsId,
            goodsType:goodsType,
            goodsName:goodsName,
            goodsHe:goodsHe,
            submitter:submitter,
            bumen:bumen
        });
        goodsInfoMap[goodsId].push(newGoodsInfo);
        goodsIds.push(goodsId);
    }

    function filterGoodsInfo(uint256 goodsId) public view returns (string[] memory goodsTypes, string[] memory goodsNames, uint256[] memory goodsHes, string[] memory submitters, string[] memory bumens) {
        GoodsInfo[] storage goodsInfos = goodsInfoMap[goodsId];
        goodsTypes = new string[](goodsInfos.length);
        goodsNames = new string[](goodsInfos.length);
        goodsHes = new uint256[](goodsInfos.length);
        submitters = new string[](goodsInfos.length);
        bumens = new string[](goodsInfos.length);
        for (uint256 i = 0; i < goodsInfos.length; i++) {
            goodsTypes[i] = goodsInfos[i].goodsType;
            goodsNames[i] = goodsInfos[i].goodsName;
            goodsHes[i] = goodsInfos[i].goodsHe;
            submitters[i] = goodsInfos[i].submitter;
            bumens[i] = goodsInfos[i].bumen;
        }
        return (goodsTypes, goodsNames, goodsHes, submitters, bumens);
    }
}
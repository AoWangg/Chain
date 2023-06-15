pragma solidity 0.4.25;
pragma experimental ABIEncoderV2;

contract state {

  // 定义有限状态机状态转换结构体
  struct Transition {
    string fromState;
    string toState;
    uint timestamp;
    uint goodsId;
    string smartContractAddress;
    string initiator;
    string receiver;
  }

  Transition[] public transitions;
  
  function start(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "start",
        toState: "Reported",
        timestamp: block.timestamp,   // 获取当前块的时间戳
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}

function report(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "Start",
        toState: "Reported",
        timestamp: block.timestamp,
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}


function approve(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "Reported",
        toState: "Approved",
        timestamp: block.timestamp,
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}

function requestDeparture(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "Approved",
        toState: "RequestedDeparture",
        timestamp: block.timestamp,
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}

function approveRequest(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "RequestedDeparture",
        toState: "DepartureApproved",
        timestamp: block.timestamp,
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}

function depart(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "DepartureApproved",
        toState: "Departed",
        timestamp: block.timestamp,
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}

function reportToWarehouse(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "Departed",
        toState: "ReportedToWarehouse",
        timestamp: block.timestamp,
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}

function approveWarehouse(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "ReportedToWarehouse",
        toState: "WarehouseApproved",
        timestamp: block.timestamp,
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}

function requestTransportation(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "WarehouseApproved",
        toState: "RequestedTransportation",
        timestamp: block.timestamp,
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}

function reportOutbound(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "RequestedTransportation",
        toState: "ReportedOutbound",
        timestamp: block.timestamp,
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}

function approveOutbound(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "ReportedOutbound",
        toState: "OutboundApproved",
        timestamp: block.timestamp,
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}

function submitQualifications(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "OutboundApproved",
        toState: "SubmittedQualifications",
        timestamp: block.timestamp,
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}

function approveQualifications(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "SubmittedQualifications",
        toState: "ApprovedQualifications",
        timestamp: block.timestamp,
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}

function deliver(uint _goodsId, string memory _smartContractAddress, string memory _initiator, string memory _receiver) public {
    transitions.push(Transition({
        fromState: "ApprovedQualifications",
        toState: "Delivered",
        timestamp: block.timestamp,
        goodsId: _goodsId,
        smartContractAddress: _smartContractAddress,
        initiator: _initiator,
        receiver: _receiver
    }));
}

function getTransitionsNoGoodsId1(uint _goodsId) public view returns (string[] memory, string[] memory, uint[] memory) {
    string[] memory fromStates = new string[](transitions.length);
    string[] memory toStates = new string[](transitions.length);
    uint[] memory timestamps = new uint[](transitions.length);
    uint count = 0;
    for (uint i=0; i<transitions.length; i++) {
        if (transitions[i].goodsId == _goodsId) {
            fromStates[count] = transitions[i].fromState;
            toStates[count] = transitions[i].toState;
            timestamps[count] = transitions[i].timestamp;
            count++;
        }
    }

    string[] memory trimmedFromStates = new string[](count);
    string[] memory trimmedToStates = new string[](count);
    uint[] memory trimmedTimestamps = new uint[](count);
    for (uint j=0; j<count; j++) {
        trimmedFromStates[j] = fromStates[j];
        trimmedToStates[j] = toStates[j];
        trimmedTimestamps[j] = timestamps[j];
    }

    return (trimmedFromStates, trimmedToStates, trimmedTimestamps);
}

function getTransitionsNoGoodsId2(uint _goodsId) public view returns (string[] memory, string[] memory, string[] memory) {
    string[] memory smartContractAddresses = new string[](transitions.length);
    string[] memory initiators = new string[](transitions.length);
    string[] memory receivers = new string[](transitions.length);
    uint count = 0;
    for (uint i=0; i<transitions.length; i++) {
        if (transitions[i].goodsId == _goodsId) {
            smartContractAddresses[count] = transitions[i].smartContractAddress;
            initiators[count] = transitions[i].initiator;
            receivers[count] = transitions[i].receiver;
            count++;
        }
    }

    string[] memory trimmedSmartContractAddresses = new string[](count);
    string[] memory trimmedInitiators = new string[](count);
    string[] memory trimmedReceivers = new string[](count);
    for (uint j=0; j<count; j++) {
        trimmedSmartContractAddresses[j] = smartContractAddresses[j];
        trimmedInitiators[j] = initiators[j];
        trimmedReceivers[j] = receivers[j];
    }

    return (trimmedSmartContractAddresses, trimmedInitiators, trimmedReceivers);
}

    
}
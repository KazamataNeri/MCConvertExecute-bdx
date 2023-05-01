from io import BytesIO
from BDXConverter.GeneralClass import GeneralClass
from BDXConverter.StructOfChest import ChestData
from Utils.getByte import getByte
from struct import pack, unpack


class PlaceBlockWithChestData(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'PlaceBlockWithChestData'
        self.operationNumber: int = 40
        self.blockConstantStringID: int = 0
        self.blockData: int = 0
        self.slotCount: int = 0
        self.data: ChestData = ChestData()

    def Marshal(self, writer: BytesIO) -> None:
        self.data.slotCount = self.slotCount
        writer.write(pack('>H', self.blockConstantStringID) + pack('>H', self.blockData) +
                     self.slotCount.to_bytes(length=1, byteorder='big', signed=False) + self.data.Marshal())

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.blockConstantStringID = unpack('>H', getByte(buffer, 2))[0]
        self.blockData = unpack('>H', getByte(buffer, 2))[0]
        self.slotCount = getByte(buffer, 1)[0]
        self.data.slotCount = self.slotCount
        self.data.UnMarshal(buffer)

    def Loads(self, jsonDict: dict) -> None:
        self.blockConstantStringID = jsonDict['blockConstantStringID'] if 'blockConstantStringID' in jsonDict else 0
        self.blockData = jsonDict['blockData'] if 'blockData' in jsonDict else 0
        self.slotCount = jsonDict['slotCount'] if 'slotCount' in jsonDict else 0
        newChestData = ChestData()
        if 'data' in jsonDict:
            newChestData.Loads(jsonDict['data'])
        self.data = newChestData
        self.data.slotCount = self.slotCount

    def Dumps(self) -> dict:
        result: dict = {
            'operationName': self.operationName,
            'operationNumber': self.operationNumber,
            'blockConstantStringID': self.blockConstantStringID,
            'blockData': self.blockData,
            'slotCount': self.slotCount,
            'data': self.data.Dumps()
        }
        return result

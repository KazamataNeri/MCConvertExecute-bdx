from io import BytesIO
from BDXConverter.GeneralClass import GeneralClass
from Utils.getString import getByte, getString
from struct import pack, unpack


class ChestSlot(GeneralClass):
    """
    Note: `ChestSlot` is not a operation
    """

    def __init__(self) -> None:
        self.itemName: str = ''
        self.count: int = 0
        self.data: int = 0
        self.slotID: int = 0

    def Marshal(self) -> bytes:
        return self.itemName.encode(encoding='utf-8') + b'\x00' + self.count.to_bytes(length=1, byteorder='big', signed=False) + pack('>H', self.data) + self.slotID.to_bytes(length=1, byteorder='big', signed=False)

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.itemName = getString(buffer)
        self.count = getByte(buffer, 1)[0]
        self.data = unpack('>H', getByte(buffer, 2))[0]
        self.slotID = getByte(buffer, 1)[0]

    def Loads(self, jsonDict: dict) -> None:
        self.itemName = jsonDict['itemName'] if 'itemName' in jsonDict else ''
        self.count = jsonDict['count'] if 'count' in jsonDict else 0
        self.data = jsonDict['data'] if 'data' in jsonDict else 0
        self.slotID = jsonDict['slotID'] if 'slotID' in jsonDict else 0


class ChestData(GeneralClass):
    """
    Note: `ChestData` is not a operation
    """

    def __init__(self) -> None:
        self.slotCount: int = 0
        self.chestData: list[ChestSlot] = []

    def Marshal(self) -> bytes:
        return b''.join([self.chestData[i].Marshal() for i in range(self.slotCount)])

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.chestData = []
        for _ in range(self.slotCount):
            newSlot = ChestSlot()
            newSlot.UnMarshal(buffer)
            self.chestData.append(newSlot)

    def Dumps(self) -> list[dict]:
        result: list[dict] = []
        for i in self.chestData:
            result.append(i.Dumps())
        return result

    def Loads(self, jsonList: list[dict]) -> None:
        self.slotCount = len(jsonList)
        self.chestData = []
        for i in jsonList:
            newSlot = ChestSlot()
            newSlot.Loads(i)
            self.chestData.append(newSlot)
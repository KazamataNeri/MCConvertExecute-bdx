from io import BytesIO
from BDXConverter.GeneralClass import GeneralClass
from Utils.getByte import getByte
from struct import pack, unpack


class PlaceRuntimeBlock(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'PlaceRuntimeBlock'
        self.operationNumber: int = 32
        self.runtimeId: int = 0

    def Marshal(self, writer: BytesIO) -> None:
        writer.write(pack('>H', self.runtimeId))

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.runtimeId = unpack('>H', getByte(buffer, 2))[0]

    def Loads(self, jsonDict: dict) -> None:
        self.runtimeId = jsonDict['runtimeId'] if 'runtimeId' in jsonDict else 0
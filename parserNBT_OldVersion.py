import nbtlib
import io
import struct

endian:str = '<'

class getValueError(Exception):
    def __init__(self,errorOccurredPosition:int):
        Exception.__init__(self, f'failed to parse value, and the error occurred at position {errorOccurredPosition}')

class unexpectedError(Exception):
    def __init__(self, value:int):
        Exception.__init__(self, f'unexpected number {value}')

def getName(buffer:io.BytesIO) -> str:
    keyLength = struct.unpack(f'{endian}h',buffer.read(2))[0]
    return str(buffer.read(keyLength))[2:-1]    

def getValue(buffer:io.BytesIO,valueType:int) -> nbtlib.tag.Byte|nbtlib.tag.Short|nbtlib.tag.Int|nbtlib.tag.Long|nbtlib.tag.Float|nbtlib.tag.Double|nbtlib.tag.ByteArray|nbtlib.tag.String|nbtlib.tag.List[any]|nbtlib.tag.Compound|nbtlib.tag.IntArray|nbtlib.tag.LongArray:
    if valueType == 1:
        return nbtlib.tag.Byte(buffer.read(1)[0])
    elif valueType == 2:
        return nbtlib.tag.Short(struct.unpack(f'{endian}h',buffer.read(2))[0])
    elif valueType == 3:
        return nbtlib.tag.Int(struct.unpack(f'{endian}i',buffer.read(4))[0])
    elif valueType == 4:
        return nbtlib.tag.Long(struct.unpack(f'{endian}q',buffer.read(8))[0])
    elif valueType == 5:
        return nbtlib.tag.Float(struct.unpack(f'{endian}f',buffer.read(4))[0])
    elif valueType == 6:
        return nbtlib.tag.Double(struct.unpack(f'{endian}d',buffer.read(8))[0])
    elif valueType == 7:
        return getArray(buffer,7)
    elif valueType == 8:
        return nbtlib.tag.String(getName(buffer))
    elif valueType == 9:
        return getList(buffer)
    elif valueType == 10:
        return getCompound(buffer)
    elif valueType == 11:
        return getArray(buffer,11)
    elif valueType == 12:
        return getArray(buffer,12)
    else:
        raise getValueError(buffer.seek(0,1))

def getArray(buffer:io.BytesIO,valueType:int) -> nbtlib.tag.ByteArray|nbtlib.tag.IntArray|nbtlib.tag.LongArray:
    arrayLength = struct.unpack(f'{endian}i',buffer.read(4))[0]
    if valueType == 7:
        return nbtlib.tag.ByteArray([buffer.read(1)[0] for _ in range(arrayLength)])
    elif valueType == 11:
        return nbtlib.tag.IntArray([struct.unpack(f'{endian}i',buffer.read(4))[0] for _ in range(arrayLength)])
    elif valueType == 12:
        return nbtlib.tag.LongArray([struct.unpack(f'{endian}q',buffer.read(8))[0] for _ in range(arrayLength)])
    else:
        raise unexpectedError(valueType)

def getList(buffer:io.BytesIO) -> nbtlib.tag.List[any]:
    valueType = buffer.read(1)[0]
    listLength = struct.unpack(f'{endian}i',buffer.read(4))[0]
    return nbtlib.tag.List([getValue(buffer,valueType) for _ in range(listLength)])

def getCompound(buffer:io.BytesIO) -> nbtlib.tag.Compound:
    result:dict = {}
    while True:
        nextBuffer = buffer.read(1)
        if len(nextBuffer) <= 0:
            raise EOFError
        if nextBuffer == b'\x00':
            return nbtlib.tag.Compound(result)
        # if meet EOF or TAG_End
        buffer.seek(-1,1)
        # correct the pointer
        valueType = buffer.read(1)[0]
        name = getName(buffer)
        result[name] = getValue(buffer,valueType)
        # set values

def parse(buffer:io.BytesIO) -> tuple[nbtlib.tag.Byte|nbtlib.tag.Short|nbtlib.tag.Int|nbtlib.tag.Long|nbtlib.tag.Float|nbtlib.tag.Double|nbtlib.tag.ByteArray|nbtlib.tag.String|nbtlib.tag.List[any]|nbtlib.tag.Compound|nbtlib.tag.IntArray|nbtlib.tag.LongArray,str]:
    valueType = buffer.read(1)[0]
    name = getName(buffer)
    return getValue(buffer,valueType), name
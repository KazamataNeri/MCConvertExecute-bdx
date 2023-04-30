from BDXConverter.GeneralClass import GeneralClass
from BDXConverter.Pool import GetBDXCommandPool
from BDXConverter.ConvertErrorDefine import notAcorrectBDXFileError
from BDXConverter.ConvertErrorDefine import readError, unknownOperationError
from Utils.getString import getByte, getString
from brotli import compress, decompress
from io import BytesIO
from json import dumps
from copy import deepcopy


def ReadBDXFile(path: str) -> tuple[list[GeneralClass], str]:
    """
    Convert BDX file into list[GeneralClass] and return the author's name
    """
    with open(path, "r+b") as file:
        fileContext: bytes = file.read()
    file.close()
    # get the context of this bdx file
    if fileContext[0:3] != b'BD@':
        raise notAcorrectBDXFileError(path)
    buffer = BytesIO(decompress(fileContext[3:]))
    if getByte(buffer, 3) != b'BDX':
        raise notAcorrectBDXFileError(path)
    # check header and create new buffer
    result: list[GeneralClass] = []
    bdxCommandPool = GetBDXCommandPool()
    # prepare
    getByte(buffer, 1)
    authorName = getString(buffer)
    # get author's information
    while True:
        commandId = getByte(buffer, 1)
        if commandId[0] in bdxCommandPool:
            struct: GeneralClass = deepcopy(bdxCommandPool[commandId[0]])
            # get struct(operation) from the pool
            try:
                struct.UnMarshal(buffer)
            except EOFError:
                raise EOFError
            except:
                raise readError(buffer.seek(0, 1))
            # unmarshal bytes into python object(GeneralClass)
            result.append(struct)
            # submit single datas
            if struct.operationNumber == 88:
                break
            # if meet operation Terminate(88)
        else:
            raise unknownOperationError(commandId[0], buffer.seek(0, 1))
            # if we can not find the operation from the command pool
    # read bdx file
    return result, authorName
    # return


def ConvertListIntoBDXFile(
        structs: list[GeneralClass],
        outputPath: str,
        authorName: str = 'KazamataNeri/MCConvertExecute-bdx'
) -> None:
    """
    Convert list[GeneralClass] into bytes and write it into a bdx file(outputPath:str).

    Note:
        - Author's name is no need to write,
        because this field has been officially deprecated.
        But we still put the names into this place as symbolically
    """
    writer: BytesIO = BytesIO(b'')
    # request a new writer
    writer.write(b'BDX\x00'+authorName.encode(encoding='utf-8')+b'\x00')
    # write inside header(BDX) and author's name
    for i in structs:
        writer.write(i.operationNumber.to_bytes(
            length=1, byteorder='big', signed=False))
        i.Marshal(writer)
    # marshal python object into the writer
    result = b'BD@' + compress(writer.getvalue())
    # compress writer into bytes and set outside header which named "BD@"
    with open(outputPath, 'w+b') as file:
        file.write(result)
    file.close()
    # write bytes into a bdx file


def ConvertListIntoJSONFile(structs: list[GeneralClass], outputPath: str) -> None:
    """
    Convert list[GeneralClass] into json data and write it into outputPath:str
    """
    new: list = []
    for i in structs:
        new.append(i.Dumps())
    # convert bdx file in to basic datas
    result: str = dumps(
        new,
        sort_keys=True,
        indent=4,
        separators=(', ', ': '),
        ensure_ascii=False
    )
    # get string
    with open(outputPath, 'w+', encoding='utf-8') as file:
        file.write(result)
    file.close()
    # write json datas

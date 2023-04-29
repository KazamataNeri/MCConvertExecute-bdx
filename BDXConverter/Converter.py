from BDXConverter.GeneralClass import GeneralClass
from BDXConverter.Pool import GetBDXCommandPool
from utils.getString import getByte, getString
from brotli import decompress
from io import BytesIO
from json import dumps
from copy import deepcopy


class notAcorrectBDXFileError(Exception):
    """
    Not a correct BDX file error
    """

    def __init__(self, path: str):
        Exception.__init__(self, f'"{path}" is not a correct BDX file')


class readError(Exception):
    """
    BDX file read error
    """

    def __init__(self, errorOccurredPosition: int):
        Exception.__init__(
            self, f'failed to convert this BDX file, and the error occurred at position {errorOccurredPosition}')


class unknownOperationError(Exception):
    """
    Find unknown operation error
    """

    def __init__(self, operationId: int, errorOccurredPosition: int):
        Exception.__init__(
            self, f'an unknown operation {operationId} was found, and the error occurred at position {errorOccurredPosition}')


def ReadBDXFile(path: str) -> list[GeneralClass]:
    """
    Convert BDX file into list[GeneralClass]
    """
    with open(path, "r+b") as file:
        fileContext: bytes = b''.join(file.readlines())
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
    getString(buffer)
    # jump author's information
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
    return result
    # return


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
    # write json datas

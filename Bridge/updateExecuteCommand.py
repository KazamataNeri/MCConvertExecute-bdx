import nbtlib
from BDXConverter.Converter.FileOperation import ReadBDXFile, DumpStructs
from CommandUpdater.updater import ExecuteCommandUpdater

from BDXConverter.Operation.SetCommandBlockData import SetCommandBlockData
from BDXConverter.Operation.PlaceBlockWithCommandBlockData import PlaceBlockWithCommandBlockData
from BDXConverter.Operation.PlaceRuntimeBlockWithCommandBlockData import PlaceRuntimeBlockWithCommandBlockData
from BDXConverter.Operation.PlaceRuntimeBlockWithCommandBlockDataAndUint32RuntimeID import PlaceRuntimeBlockWithCommandBlockDataAndUint32RuntimeID
from BDXConverter.Operation.PlaceCommandBlockWithCommandBlockData import PlaceCommandBlockWithCommandBlockData
from BDXConverter.Operation.PlaceBlockWithNBTData import PlaceBlockWithNBTData


def upgradeExecuteCommand(inputPath: str, outputPath: str) -> None:
    """
    Upgrade the execute command in the file of the
    inputPath:str and output it in the outPath:str
    """
    readResult = ReadBDXFile(inputPath)
    # read bdx file
    for i in readResult.BDXContents:
        match i.operationNumber:
            case 26 | 27 | 34 | 35 | 36:
                i1: SetCommandBlockData | PlaceBlockWithCommandBlockData | PlaceRuntimeBlockWithCommandBlockData | PlaceRuntimeBlockWithCommandBlockDataAndUint32RuntimeID | PlaceCommandBlockWithCommandBlockData = i  # type: ignore
                # explicit data type
                commandString: str = str(i1.command)
                convertResult = ExecuteCommandUpdater(commandString)
                if convertResult[1] == True:
                    i1.command = nbtlib.tag.String(
                        convertResult[0])
                # convert
            case 41:
                i2: PlaceBlockWithNBTData = i  # type: ignore
                # explicit data type

                def subFunc():
                    if not 'id' in i2.blockNBT:
                        return
                    if i2.blockNBT['id'] != nbtlib.tag.String('CommandBlock'):
                        return
                    if not 'Command' in i2.blockNBT:
                        return
                    # check the block
                    commandString: str = str(i2.blockNBT['Command'])
                    convertResult = ExecuteCommandUpdater(commandString)
                    if convertResult[1] == True:
                        i2.blockNBT['Command'] = nbtlib.tag.String(
                            convertResult[0])
                    # convert
                # define a subfunc to execute codes
                subFunc()
                # execute the subFunc
    # upgrade execute command
    readResult.AuthorName = 'KazamataNeri/MCConvertExecute-bdx'
    readResult.Signature.signedOrNeedToSign = False
    DumpStructs(readResult, outputPath)
    # write result

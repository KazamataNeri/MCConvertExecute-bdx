import nbtlib
from BDXConverter.Converter import ReadBDXFile, DumpStructs
from CommandUpdater.updater import ExecuteCommandUpdater

from BDXConverter.SetCommandBlockData import SetCommandBlockData
from BDXConverter.PlaceBlockWithCommandBlockData import PlaceBlockWithCommandBlockData
from BDXConverter.PlaceRuntimeBlockWithCommandBlockData import PlaceRuntimeBlockWithCommandBlockData
from BDXConverter.PlaceRuntimeBlockWithCommandBlockDataAndUint32RuntimeID import PlaceRuntimeBlockWithCommandBlockDataAndUint32RuntimeID
from BDXConverter.PlaceCommandBlockWithCommandBlockData import PlaceCommandBlockWithCommandBlockData
from BDXConverter.PlaceBlockWithNBTData import PlaceBlockWithNBTData


def upgradeExecuteCommand(inputPath: str, outputPath: str) -> None:
    """
    Upgrade the execute command in the file of the
    inputPath:str and output it in the outPath:str
    """
    readResult, _ = ReadBDXFile(inputPath)
    # read bdx file
    for i in readResult:
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
    DumpStructs(readResult, outputPath)
    # write result

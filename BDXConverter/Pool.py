from BDXConverter.GeneralClass import GeneralClass

from BDXConverter.CreateConstantString import CreateConstantString
from BDXConverter.PlaceBlockWithBlockStates import PlaceBlockWithBlockStates
from BDXConverter.AddInt16ZValue0 import AddInt16ZValue0
from BDXConverter.PlaceBlock import PlaceBlock
from BDXConverter.AddZValue0 import AddZValue0
from BDXConverter.NOP import NOP
from BDXConverter.AddInt32ZValue0 import AddInt32ZValue0
from BDXConverter.PlaceBlockWithBlockStatesDeprecated import PlaceBlockWithBlockStatesDeprecated
from BDXConverter.AddXValue import AddXValue
from BDXConverter.SubtractXValue import SubtractXValue
from BDXConverter.AddYValue import AddYValue
from BDXConverter.SubtractYValue import SubtractYValue
from BDXConverter.AddZValue import AddZValue
from BDXConverter.SubtractZValue import SubtractZValue
from BDXConverter.AddInt16XValue import AddInt16XValue
from BDXConverter.AddInt32XValue import AddInt32XValue
from BDXConverter.AddInt16YValue import AddInt16YValue
from BDXConverter.AddInt32YValue import AddInt32YValue
from BDXConverter.AddInt16XValue import AddInt16XValue
from BDXConverter.AddInt32XValue import AddInt32XValue
from BDXConverter.AddInt16YValue import AddInt16YValue
from BDXConverter.AddInt32YValue import AddInt32YValue
from BDXConverter.AddInt16ZValue import AddInt16ZValue
from BDXConverter.AddInt32ZValue import AddInt32ZValue
from BDXConverter.SetCommandBlockData import SetCommandBlockData
from BDXConverter.PlaceBlockWithCommandBlockData import PlaceBlockWithCommandBlockData
from BDXConverter.AddInt8XValue import AddInt8XValue
from BDXConverter.AddInt8YValue import AddInt8YValue
from BDXConverter.AddInt8ZValue import AddInt8ZValue
from BDXConverter.UseRuntimeIDPool import UseRuntimeIDPool
from BDXConverter.PlaceRuntimeBlock import PlaceRuntimeBlock
from BDXConverter.PlaceBlockWithRuntimeId import PlaceBlockWithRuntimeId
from BDXConverter.PlaceRuntimeBlockWithCommandBlockData import PlaceRuntimeBlockWithCommandBlockData
from BDXConverter.PlaceRuntimeBlockWithCommandBlockDataAndUint32RuntimeID import PlaceRuntimeBlockWithCommandBlockDataAndUint32RuntimeID
from BDXConverter.PlaceCommandBlockWithCommandBlockData import PlaceCommandBlockWithCommandBlockData
from BDXConverter.PlaceRuntimeBlockWithChestData import PlaceRuntimeBlockWithChestData
from BDXConverter.PlaceRuntimeBlockWithChestDataAndUint32RuntimeID import PlaceRuntimeBlockWithChestDataAndUint32RuntimeID
from BDXConverter.AssignDebugData import AssignDebugData
from BDXConverter.PlaceBlockWithChestData import PlaceBlockWithChestData
from BDXConverter.PlaceBlockWithNBTData import PlaceBlockWithNBTData
from BDXConverter.Terminate import Terminate


def GetBDXCommandPool() -> dict[int, GeneralClass]:
    """
    Return dict[commandId:int, PythonObject:GeneralClass]
    """
    return {
        1: CreateConstantString(),
        5: PlaceBlockWithBlockStates(),
        6: AddInt16ZValue0(),
        7: PlaceBlock(),
        8: AddZValue0(),
        9: NOP(),
        12: AddInt32ZValue0(),
        13: PlaceBlockWithBlockStatesDeprecated(),
        14: AddXValue(),
        15: SubtractXValue(),
        16: AddYValue(),
        17: SubtractYValue(),
        18: AddZValue(),
        19: SubtractZValue(),
        20: AddInt16XValue(),
        21: AddInt32XValue(),
        22: AddInt16YValue(),
        23: AddInt32YValue(),
        24: AddInt16ZValue(),
        25: AddInt32ZValue(),
        26: SetCommandBlockData(),
        27: PlaceBlockWithCommandBlockData(),
        28: AddInt8XValue(),
        29: AddInt8YValue(),
        30: AddInt8ZValue(),
        31: UseRuntimeIDPool(),
        32: PlaceRuntimeBlock(),
        33: PlaceBlockWithRuntimeId(),
        34: PlaceRuntimeBlockWithCommandBlockData(),
        35: PlaceRuntimeBlockWithCommandBlockDataAndUint32RuntimeID(),
        36: PlaceCommandBlockWithCommandBlockData(),
        37: PlaceRuntimeBlockWithChestData(),
        38: PlaceRuntimeBlockWithChestDataAndUint32RuntimeID(),
        39: AssignDebugData(),
        40: PlaceBlockWithChestData(),
        41: PlaceBlockWithNBTData(),
        88: Terminate()
    }

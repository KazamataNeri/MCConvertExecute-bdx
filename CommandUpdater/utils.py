from CommandUpdater.CommandReader import CommandReader
from CommandUpdater.Position import SinglePos, Pos


def searchForHeader(c: CommandReader, header: str, jumpSlash: bool) -> bool:
    """
    概述 & 返回值
        从 c.context 的 c.pointer 处寻找命令前缀 header 。
        当找到时，返回真并且修改阅读进度，否则返回假。
    参数
        c:CommandReader | 指代一个命令阅读器，用于从中阅读 Execute 命令
        header:str | 指代要查找的命令前缀
        jumpSlash:bool | 是否要跳过斜杠 "/" ，为真时代表需要跳过，否则反正
    """
    c.jumpSpace(jumpSlash)
    tmp = c.pointer
    headerGet = c.read(len(header)).lower()
    # jump space and read command header
    if headerGet == header:
        return True
    else:
        c.pointer = tmp
        return False
    # return


def getSelector(c: CommandReader) -> list:
    """
    概述
        从 c.context 的 c.pointer 处寻找选择器，
        并在找到时更新阅读器的阅读进度
    参数
        c:CommandReader | 指代一个命令阅读器，用于从中阅读 Execute 命令
    返回值
        返回一个列表且只有两个元素。
        其第一项代表找到的选择器，是一个字符串，
        其第二项代表查找结果，且只有为真时代表找到，否则反之
    """
    tmp = c.pointer

    def failedFunc():
        c.pointer = tmp
        return [-1, False]
    # init values
    c.jumpSpace(False)
    # jump space
    selectorStartLocation = c.pointer
    readAns = c.read(1)
    # read header
    if readAns == '@':
        findAns = c.highSearching(
            [
                "s", "a", "p", "e", "r", "initiator", "c", "v"
            ]
        )
        if findAns[2] == False:
            return failedFunc()
        if findAns[0] != selectorStartLocation+1:
            return failedFunc()
        selectorEndLocation = c.pointer
        # try to find @...
        c.jumpSpace(False)
        # jump space
        string = c.read(1)
        # read ... in @...
        if string == '[':
            parameterStartLocation = c.pointer - 1
            parameterEndLocation = c.getRightBarrier(0)
            if parameterEndLocation[1] == False:
                return failedFunc()
            return [
                f'{c.context[selectorStartLocation:selectorEndLocation]}{c.context[parameterStartLocation: parameterEndLocation[0]]}',
                True
            ]
            # @...[...]
        else:
            c.pointer = findAns[1]
            return [
                c.context[selectorStartLocation: findAns[1]],
                True
            ]
            # @...
        # @...[...] or @...
    elif readAns == '"':
        findAns = c.getRightBarrier(1)
        if findAns[1] == False:
            return failedFunc()
        return [
            c.context[selectorStartLocation: findAns[0]],
            True
        ]
        # "..."
    else:
        if tmp == selectorStartLocation:
            return failedFunc()
        findAns = c.highSearching([" ", "~", "^", "+"])
        if findAns[2] == False:
            return failedFunc()
        c.pointer = c.pointer-1
        return [
            c.context[selectorStartLocation: c.pointer],
            True
        ]
        # ...


def getPos(c: CommandReader) -> Pos:
    """
    概述
        从 c.context 的 c.pointer 处寻找一组三维坐标，
        并在每解析一个坐标时更新阅读器的阅读进度。
        特别地，在最终检验语法时发现了语法错误，
        则阅读器的阅读进度会回溯到调用此函数前的状态
    参数
        c:CommandReader | 指代一个命令阅读器，用于从中阅读 Execute 命令
    返回值
        返回一个完整的坐标 Pos
    """
    ans = Pos(
        SinglePos(),
        SinglePos(),
        SinglePos()
    )
    tmp = c.pointer
    # init values
    for i in range(0, 3):
        newPos = SinglePos()
        successStates = newPos.parse(c)
        if successStates == False:
            return ans
        match i:
            case 0:
                ans.posx = newPos
            case 1:
                ans.posy = newPos
            case 2:
                ans.posz = newPos
    # get posx, posy, posz
    ans.Checker()
    if ans.verified == False:
        c.pointer = tmp
    return ans
    # return


def detectBlock(c: CommandReader) -> list:
    """
    概述
        从 c.context 的 c.pointer 处解析一组 detect block 信息，
        并在成功解析时更新阅读器的阅读进度
    参数
        c:CommandReader | 指代一个命令阅读器，用于从中阅读 Execute 命令
    返回值
        返回一个列表且只有三个元素。
        其第一项代表是否找到了 detect block 信息，为真时代表找到，否则没有找到；
        其第二项是一个字符串，包含了 detect block 信息在新语法下的表示；
        其第三项表示 detect block 信息的解析结果，为真时代表解析成功，否则反之
    """
    if searchForHeader(c, 'detect', False) == True:
        tmp = c.pointer

        def failedFunc():
            c.pointer = tmp
            return [True, "", False]
        # init values
        position = getPos(c)
        if position.verified == False:
            return failedFunc()
        posString = position.format()
        # pos
        save = c.pointer
        c.jumpSpace(False)
        if c.pointer == save and position.posz.isNotNumber == False:
            return failedFunc()
        # for example, "~~ +5air 0" is wrong
        blockNameAndblockData = []
        for _ in range(0, 2):
            c.jumpSpace(False)
            startLocation = c.pointer
            findAns = c.index(' ')
            if findAns[1] == False:
                return failedFunc()
            blockNameAndblockData.append(c.context[startLocation:findAns[0]])
            c.pointer = findAns[0]
        # block name and block data
        c.jumpSpace(True)
        # jump space and slash
        return [
            True,
            f' if block {posString} {blockNameAndblockData[0]}',
            True
        ]
        # TODO - Convert block data to the block states
        return [
            True,
            f' if block {posString} {blockNameAndblockData[0]} {blockNameAndblockData[1]}',
            True
        ]
        # return
    else:
        return [False, "", False]
        # return

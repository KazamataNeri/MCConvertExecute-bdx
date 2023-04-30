from CommandUpdater.utils import CommandReader
from CommandUpdater.utils import searchForHeader, getSelector, getPos, detectBlock


def ExecuteCommandUpdater(command: str) -> list:
    """
    概述
        将 command 升级为新的 Execute 命令格式
    参数
        command:str | 指代待升级的 Execute 命令
    返回值
        返回一个列表且只有四个元素。
        其第一项代表升级结果，是一个字符串；
        其第二项代表升级状态，为真时表示升级成功，否则失败；
        其第三项代表错误信息，是一个字符串；
        其第四项代表指令中可能错误的字段，是一个字符串
    """
    ans = []
    newReader = CommandReader(command, 0)

    def failedFunc(errInfo: str):
        return [
            "",
            False,
            errInfo,
            f"{newReader.context[newReader.pointer:]}"
        ]
    # init values
    while True:
        if searchForHeader(newReader, 'execute', True):
            selector = getSelector(newReader)
            if selector[1] == False:
                return failedFunc(f"无法解析位于 {newReader.pointer} 处的选择器及其参数，请更正格式")
            # selector
            tmp = newReader.pointer
            newReader.jumpSpace(False)
            save = newReader.pointer
            # check prepare
            pos = getPos(newReader)
            if pos.verified == False:
                return failedFunc(f"无法解析位于 {newReader.pointer} 处的坐标，请更正格式")
            posString = pos.format()
            # pos
            if tmp == save and pos.posx.isNotNumber == False and pos.posx.header == '' and selector[0][0] == "@" and selector[0][-1] != "]":
                newReader.pointer = tmp - 5
                return failedFunc(f"位置 {newReader.pointer} 附近发生了语法错误，请更正格式")
            # for example, "@s1 ~5~3" is wrong
            tmp = newReader.pointer
            newReader.jumpSpace(False)
            if tmp == newReader.pointer and pos.posz.isNotNumber == False:
                newReader.pointer = newReader.pointer - 5
                return failedFunc(f"位置 {newReader.pointer} 附近发生了语法错误，请更正格式")
            # for example, "~~ +5w @s" is wrong
            tmp = newReader.pointer
            detect = detectBlock(newReader)
            if detect[0] == True and detect[2] == False:
                return failedFunc(f"无法解析位于 {newReader.pointer} 处的 Detect Block 数据，请更正格式")
            # detect
            if posString == "~ ~ ~" or posString == "^ ^ ^":
                ans.append(
                    f"as {selector[0]} at @s{detect[1]} "
                )
            else:
                ans.append(
                    f"as {selector[0]} at @s positioned {posString}{detect[1]} "
                )
            # submit subcommand
        else:
            ans.append(newReader.context[newReader.pointer:])
            break
    # get all the subcommand
    if len(ans) <= 1:
        return ["".join(ans), True, "", ""]
    else:
        ans[-1] = f'run {ans[-1]}'
        return [
            f'execute {"".join(ans)}',
            True, "", ""
        ]
    # return

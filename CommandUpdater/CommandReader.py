class CommandReader:
    """
    CommandReader 是一个命令阅读器，用于从中阅读 Execute 命令
    """

    def __init__(self,context:str,pointer:int) -> None:
        """
        概述
            此函数用于初始化一个命令阅读器，其内部包含一条完整的命令和阅读进度。
        参数
            context:str | 一个完整的 execute 命令
            pointer:int | 用于指示当前阅读进度
        """
        self.context:str = context
        self.pointer:int = pointer
    
    def read(self, length:int) -> str:
        """
        概述
            从 self.context 的 self.pointer 处阅读 length 个字符。
            当 self.pointer 为负数时，将会自动修正到 0 并阅读 length 个字符
        参数
            length:int | 要阅读的长度
        """
        if self.pointer < 0:
            self.pointer = 0
        string = self.context[self.pointer:self.pointer+length]
        self.pointer = self.pointer + length
        return string
    
    def jumpSpace(self,jumpSlash:bool):
        """
        概述
            持续阅读直到读到非空格或 / 字符
        参数
            jumpSlash:bool | 为真时将会同时跳过字符 "/" 但只会跳过一次
        """
        slashIsJumped = False
        while True:
            readAns = self.read(1)
            if jumpSlash == True and readAns == "/" and slashIsJumped == False:
                slashIsJumped = False
                jumpSlash = False
                continue
            if readAns != " " and readAns != "\t" and readAns != "\n":
                self.pointer = self.pointer - 1
                break
    
    def index(self,search:str) -> list:
        """
        概述
            从 self.context 的 self.pointer 处查找 search
        参数
            search:str | 要查找的字符串
        返回值
            返回一个列表且只有两个元素。
            其第一项代表 search 在 self.context 的起始位置，
            其第二项代表查找结果，且只有为真时代表找到，否则反之
        """
        location =  self.context.find(search,self.pointer)
        if location == -1:
            return [-1,False]
        return [location,True]
    
    def highSearching(self,searchList:list[str]) -> list:
        """
        概述
            枚举 searchList 中的每个字符串并得到
            距离 self.pointer 最近的字符串，
            同时在找到目标字符串时更新阅读器的阅读进度
        参数
            searchList:list[str] | 一个列表且其内部只装有字符串，对应上文中的列表
        返回值
            返回一个列表且只有三个元素。
            self.context[第一项: 第二项] 代表找到的距离 self.pointer 最近的字符串。
            第三项代表查找结果，且只有为真时代表找到，否则反之
        """
        tmp = [] # tmp = [ [0,1], [2,3] ]
        returnValue = [] # ans = [0, 1]
        minToRecord = 2147483647
        # init values
        for i in searchList:
            ans = self.index(i)
            if ans[1] == False:
                continue
            tmp.append([ans[0],ans[0]+len(i)])
        # get each result
        for i in tmp:
            if i[1] < minToRecord:
                returnValue = i
                minToRecord = i[1]
        # get the min values
        if len(returnValue) > 0:
            self.pointer = returnValue[1]
            return [returnValue[0],returnValue[1],True]
        else:
            return [-1,-1,False]
        # return
    
    def getRightBarrier(self,mode:int) -> list:
        """
        概述
            从 self.context 的 self.pointer 处寻找下一个边界符号，
            也就是 "]" 或 "\"" 并返回其所在位置加一的值。
            当找到时，将同时更新阅读器的阅读进度
        参数
            mode:int | 指代寻找模式，为 0 时寻找 "]" ，否则寻找 "\""
        返回值
            返回一个列表且只有两个元素。
            其第一项代表边界符号在 self.context 中所在位置加一的值，
            其第二项代表查找结果，且只有为真时代表找到，否则反之
        """
        tmp = self.pointer
        def exitFunc(value:int,states:bool):
            if states == False:
                self.pointer = tmp
            else:
                self.pointer = value
            return [value,states]
        # init values
        if mode == 0:
            while True:
                quotationMark = self.index('"')
                rightBarrier = self.index(']')
                #
                if rightBarrier[1] == False:
                    return exitFunc(-1,False)
                if quotationMark[1] == False:
                    return exitFunc(rightBarrier[0]+1,True)
                #
                elif quotationMark[0] < rightBarrier[0]:
                    self.pointer = quotationMark[0]+1
                    tmpFindAns = self.getRightBarrier(1)
                    if tmpFindAns[1] == False:
                        return exitFunc(-1,False)
                else:
                    return exitFunc(rightBarrier[0]+1,True)
        # find "]"
        else:
            while True:
                readAns = self.read(1)
                match readAns:
                    case '':
                        return exitFunc(-1,False)
                    case '\\':
                        self.read(1)
                        continue
                    case '"':
                        returnValue = self.pointer
                        return exitFunc(returnValue,True)
        # find "\""
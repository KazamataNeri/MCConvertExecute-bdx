from CommandUpdater.CommandReader import CommandReader


class SinglePos:
    """
    SinglePos 类用于描述一个单个的坐标
    """

    def __init__(self) -> None:
        """
        概述
            此函数用于初始化一个坐标，其内部包含以下信息
                header:str | 指代坐标的前缀，也就是 "^"、"~"、"+" 和 "-"
                number:int|float | 指代坐标的实际值(可正可负)，且类型只可能为 int 或 float
                string:str | 该坐标的字符串表达形式
                self.isNotNumber:bool | 用于标识该坐标是否不为纯数字，为真时不为纯数字，否则反之
        """
        self.header: str = ""
        self.number: int | float = 0
        self.string: str = "0"
        self.isNotNumber: bool = False

    def format(self) -> None:
        """
        概述
            将规范且最简的形式的坐标保存到 self.string 中
        """
        self.header.replace(' ', '', -1)
        # remove all the space
        if type(self.number) == int:
            numberString = str(int(self.number))
        else:
            numberString = str(float(self.number))
        # get correct string of the number
        if self.isNotNumber == True and (numberString == '0' or numberString == '0.0' or numberString == '-0.0'):
            numberString = ''
        if self.header == '+' or f'{self.header}{numberString}' == '-0.0' or f'{self.header}{numberString}' == '-0':
            header = ''
        else:
            header = self.header
        # make it minimization
        self.string = f'{header}{numberString}'
        # write datas

    def parse(self, reader: CommandReader) -> bool:
        """
        概述
            从 reader.context 的 reader.pointer 处解析一个坐标
            并在解析成功时更新 reader 的阅读进度。
            解析结果不会直接返回，而是保存在 self.string 中
        参数
            reader:CommandReader | 指代一个命令阅读器，用于从中阅读 Execute 命令
        返回值
            返回一个布尔值以指代解析的结果，且为真时代表解析成功，
            为假时代表解析失败
        """
        tmp = reader.pointer

        def failedFunc():
            reader.pointer = tmp
            return False
        # init values
        reader.jumpSpace(False)
        # jump space
        string = reader.read(1)
        # read header
        if string == '~' or string == '^':
            self.isNotNumber = True
            self.header = string
        elif string == '+' or string == '-':
            self.isNotNumber = False
            self.header = string
        else:
            self.isNotNumber = False
            self.header = ''
        # set header
        if self.header == '':
            reader.pointer = reader.pointer - 1
        # correct the pointer of reader
        startLocation = reader.pointer
        while True:
            string = reader.read(1)
            if string != '0' and string != '1' and string != '2' and (
                    string != '3') and string != '4' and string != '5' and (
                    string != '6') and string != '7' and string != '8' and (
                    string != '9') and string != '.' and string != '+' and (
                    string != '-'):
                reader.pointer = reader.pointer - 1
                break
        numberString = reader.context[startLocation:reader.pointer]
        if numberString.find('.') > 0:
            if self.header == '' and numberString[0] == '.':
                return failedFunc()
            # for example, ".2" is wrong but "+.2" or "~.2" is correct
            try:
                self.number = float(numberString)
            except:
                return failedFunc()
        else:
            try:
                if numberString == '':
                    self.number = int(0)
                else:
                    self.number = int(numberString)
            except:
                return failedFunc()
        # get the numbers
        self.format()
        return True
        # return

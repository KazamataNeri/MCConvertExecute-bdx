from CommandUpdater.SinglePos import SinglePos


class Pos:
    """
    类 Pos 用于描述一个完整的坐标
    """

    def __init__(self, posx: SinglePos, posy: SinglePos, posz: SinglePos) -> None:
        """
        概述
            此函数用于初始化一个完整的坐标
        参数
            posx:SinglePos | X 轴坐标
            posx:SinglePos | Y 轴坐标
            posx:SinglePos | Z 轴坐标
            self.verified:bool | 标识坐标是否完整，为真时代表完整，否则反之
        """
        self.posx: SinglePos = posx
        self.posy: SinglePos = posy
        self.posz: SinglePos = posz
        self.verified: bool = False

    def Checker(self):
        """
        概述
            此函数用于检验 self 中保存的三个坐标所
            构成的一个完整坐标是否满足语法规则。
            如果满足，则 self.verified 会被更新为
            True ，否则会被更新为 False
        """
        if self.posx.header == '^' or self.posy.header == '^' or (
                self.posz.header == '^'):
            if self.posx.header != '^' or self.posy.header != '^' or (
                    self.posz.header != '^'):
                self.verified = False
                return
        self.verified = True

    def format(self) -> str:
        """
        概述 & 返回值
            返回字符串形式的坐标(规范格式)
        """
        return f'{self.posx.string} {self.posy.string} {self.posz.string}'
        # write datas

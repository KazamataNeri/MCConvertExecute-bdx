import os


class GetBDXPath:
    def __init__(self):
        self.bdx_list = []
        self.inputFrom = ''
        self.inputTo = ''

    def main(self, inputFrom='', inputTo=''):
        if (self.searching_BDX()):
            while (inputFrom.strip() == ''):
                inputFrom = input('输入 BDX 文件路径或序号: ')
                if (self.is_int(inputFrom)):
                    if (int(inputFrom) <= len(self.bdx_list)):
                        inputFrom = self.bdx_list[int(inputFrom)-1]
                    else:
                        print('未找到此序号')
                        inputFrom = ''
        else:
            while (inputFrom.strip() == ''):
                inputFrom = input('输入 BDX 文件路径: ')
        while (inputTo.strip() == ''):
            inputTo = input('输入结果文件的保存路径: ')
        self.inputFrom = inputFrom
        self.inputTo = inputTo

    def searching_BDX(self):
        dir_list = os.listdir(os.getcwd())
        for filename in dir_list:
            lowerFileSuffix = filename[-3:].lower()
            if (lowerFileSuffix == 'bdx'):
                self.bdx_list.append(filename)
        if (len(self.bdx_list) > 0):
            i = 1
            print(f'已找到 {str(len(self.bdx_list))} 个 BDX 文件')
            for filename in self.bdx_list:
                print(f'    {i}: {filename}')
                i = i + 1
            return True
        else:
            print('未在当前目录找到 BDX 文件')
            return False

    def is_int(self, str):
        try:
            int(str)
            return True
        except:
            return False

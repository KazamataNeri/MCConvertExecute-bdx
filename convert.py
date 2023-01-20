import os
import sys
import brotli
#brotli 版本 (1.0.9)

class BDump:
    def __init__(self):
        self.prt = 0
        self.bdxData = ""
        self.bdxDataLen = 0
        self.inputPath = ""
        self.outputPath = ""
        self.newBdxData = b"BDX\x00"
        self.block_list = []
        
    def main(self,inputPath,outputPath):
        self.inputPath = inputPath
        self.outputPath = outputPath
        if (not self.readBDX()):
            print ("bdx文件读取错误.")
            return
        while (self.prt < self.bdxDataLen):
            self.newBdxDataSend()
        self.sendBDX(brotli.compress(self.newBdxData,quality=6))

    #-------------
    def readBDX(self):
        if (not os.path.isfile(self.inputPath)):
            print("文件路径为空")
            return False
        with open(self.inputPath, "rb+") as f:
            data = f.read()
        f.close()
        if (data[:3] == b"BD@"):
            data = data[3:]
            data = brotli.decompress(data)
            if (data[:3] == b"BDX"):
                self.bdxData = data
                self.bdxDataLen = len(data)
                self.prt = 4
                return True
            else:
                print("这不是一个标准的 BDump v4 文件格式.")
                return False
        else:
            print("这不是一个标准的 BDump v4 文件格式.")
            return False

    def sendBDX(self,newBdx):
        os.makedirs(os.path.dirname(self.outputPath), exist_ok=True)
        if (self.outputPath[-3:] != ".bdx"):
            self.outputPath = self.outputPath + ".bdx"
        send = open(self.outputPath, "wb")
        send.write(b"BD@")
        send.write(newBdx)
        send.close()
        print(f"文件保存在 {self.outputPath}")
    #---------------------------
    def newBdxDataSend(self):
        i = self.prt
        if (self.bdxData[i] == 26): 
            self.newBdxDataAdd(self.commandExecute(1,False))
            return

        if (self.bdxData[i] == 27): 
            self.newBdxDataAdd(self.commandExecute(5,False))
            return

        if (self.bdxData[i] == 34):
            self.newBdxDataAdd(self.commandExecute(3,False))
            return

        if (self.bdxData[i] == 35):
            self.newBdxDataAdd(self.commandExecute(5,False))
            return

        if (self.bdxData[i] == 36):
            self.newBdxDataAdd(self.commandExecute(3,False))
            return

        jump = self.BDumpCommandPool()
        self.newBdxDataAdd(self.bdxData[self.prt:self.prt + jump])
        self.prt = self.prt + jump

    #---------
    def newBdxDataAdd(self,data):
        self.newBdxData = self.newBdxData + data

    def toint(self,byte):
        return (int.from_bytes(byte, byteorder='big'))
    
    def strlen(self,num):
        i = 0
        while(num < self.bdxDataLen):
            if (self.bdxData[num] == 0):
                return i+1
            i = i+1
            num = num+1
        return i
    #------
    def commandExecute(self,jump,printf = True):
        i = self.prt
        data = self.bdxData
        returnstr = b""
        jump = jump + 4
        returnstr = data[i:i+jump]
        str_len = self.strlen(i+jump)
        command = bytes.decode(data[i+jump:i+jump+str_len])
        jump = jump + str_len
        commandend = jump
        str_len = self.strlen(i+jump)
        jump = jump + str_len
        str_len = self.strlen(i+jump)
        jump = jump + str_len + 4
        if (printf):
            return jump+4
        #---
        ConvertExecute = MCConvertExecute()
        newexecute = ConvertExecute.main(command,self.prt,self.bdxDataLen)
        returnstr = returnstr + newexecute.encode('utf-8') + \
                    data[i+commandend:i+jump+1] + b'\x01' + data[i+jump+2:i+jump+4]
        #print (f"command: {command}")
        #print (f"     to: {newexecute}")
        #print ("----------")
        self.prt = self.prt + jump +4
        return returnstr

    #------
    def ChestData(self,jump,slotCount):
        i = self.prt
        data = self.bdxData
        tmp = 1
        while(tmp <= slotCount):
            str_len = self.strlen(i+jump)
            jump = jump + str_len + 4
            tmp = tmp +1
        return jump
    #------
    def BDumpCommandPool(self):
        i = self.prt
        bdxData = self.bdxData
        if (self.prt == 4):
            str_len = self.strlen(i)
            if (str_len == 1):
                print ("未定义用户名")
                return 1
            else:
                author = bytes.decode(bdxData[i+1:i+str_len+1])
                print("用户名: "+author)
                return str_len +1

        if (bdxData[i] == 1):
            str_len = self.strlen(i+1)
            ConstantString = bytes.decode(bdxData[i+1:i+str_len+1])
            self.block_list.append(ConstantString)
            return str_len +1

        if (bdxData[i] == 5):
            return 5

        if (bdxData[i] == 6):
            return 3

        if (bdxData[i] == 7):
            return 5

        if (bdxData[i] == 8):
            return 1

        if (bdxData[i] == 9):
            return 1

        if (bdxData[i] == 12):
            return 5

        if (bdxData[i] == 13):
            str_len = self.strlen(i+4)
            return str_len +4

        if (bdxData[i] == 14):
            return 1

        if (bdxData[i] == 15):
            return 1

        if (bdxData[i] == 16):
            return 1

        if (bdxData[i] == 17):
            return 1

        if (bdxData[i] == 18):
            return 1

        if (bdxData[i] == 19):
            return 1

        if (bdxData[i] == 20):
            return 3

        if (bdxData[i] == 21):
            return 5

        if (bdxData[i] == 22):
            return 3

        if (bdxData[i] == 23):
            return 5

        if (bdxData[i] == 24):
            return 3

        if (bdxData[i] == 25):
            return 5

        if (bdxData[i] == 26): 
            return self.commandExecute(1)

        if (bdxData[i] == 27): 
            return self.commandExecute(5)

        if (bdxData[i] == 28):
            return 2

        if (bdxData[i] == 29):
            return 2

        if (bdxData[i] == 30):
            return 2

        if (bdxData[i] == 31):
            str_len = self.strlen(i+2)
            return str_len +2

        if (bdxData[i] == 32):
            return 3


        if (bdxData[i] == 33):
            return 5

        if (bdxData[i] == 34):
            return self.commandExecute(3)

        if (bdxData[i] == 35):
            return self.commandExecute(5)

        if (bdxData[i] == 36):
            return self.commandExecute(3)

        if (bdxData[i] == 39):
            length = self.toint(bdxData[i+1:i+5])
            buffer_list = []
            parjum = 6
            temp = 0
            while(temp < length):
                str_len = self.strlen(i+parjum)
                buffer = bytes.decode(bdxData[i+6:i+str_len+1])
                buffer_list.append(buffer)
                parjum = parjum + str_len
                temp = temp + 1
            return parjum

        if (bdxData[i] == 37):
            slotCount = bdxData[i+3]
            return self.ChestData(4,slotCount)


        if (bdxData[i] == 38):
            slotCount = bdxData[i+5]
            return self.ChestData(6,slotCount)

        if (bdxData[i] == 40):
            slotCount = bdxData[i+5]
            return self.ChestData(6,slotCount)

        if (bdxData[i] == 88):
            print("停止读入")
            self.newBdxData = self.newBdxData + b"X"
            self.prt = self.bdxDataLen +1
        return 1


class MCConvertExecute:
    def __init__(self):
        self.oldExecute = ""
        self.oldExeLenght = 0
        self.prt = 0
        self.local_prt = 0
        self.exit_interpret = False
    
    class ExecuteType:
        def __init__(self):
            self.command_type = ""
            self.exe_list = []
            self.list_len = 0

        def setExecuteType(self,command_type,exe_list,list_len = None):
            self.command_type = command_type
            self.exe_list = exe_list
            if (list_len == None):
                self.list_len = len(exe_list)
            else:
                self.list_len = list_len
    
    #------------
    def main(self,oldExecute,BDumpPrt=0,BDumpLen=0):
        self.oldExecute = oldExecute
        self.oldExeLenght = len(oldExecute)
        self.prt = 0
        splitExecute_list = []
        #---
        if (len(oldExecute) < 2):
            return oldExecute
        if (oldExecute[0] != "/"):
            if (self.isalpha(oldExecute[0])):
                oldExecute = "/" + oldExecute
        if (oldExecute[:9] != "/execute "):
            return oldExecute
        #------
        while(self.exit()):
            re = self.splitExecute()
            splitExecute_list.append(re)
        #------
        newExecute = self.SyntaxConversion(splitExecute_list)
        print (f"command: {oldExecute}")
        print (f"     to: {newExecute}")
        if (BDumpLen == 0):
            print ("-------------")
        else:
            print("------- {:.1f}% ------".format(BDumpPrt/BDumpLen*100))
        return newExecute

    #---------------
    def SyntaxConversion(self,splitExecute_list):
        """ /execute 
            @a[选择器] > at @a[选择器]
            ~ ~ ~ >  positioned ~ ~ ~ 
            detect ~ ~ ~ glass 0 > if block ~ ~ ~ glass 0
            然后在尾部添加 run 
        """
        Command_header = True
        execstr = ""
        for spexe in splitExecute_list:
            exe_list = spexe.exe_list
            if (spexe.command_type == "execute"):
                if (Command_header):
                    execstr = execstr + exe_list[0] + " "
                    Command_header = False
                execstr = execstr + "at "+ exe_list[1] +" "
                if (exe_list[2] != "~ ~ ~"):
                    execstr = execstr + "positioned " + exe_list[2] + " "
                if (spexe.list_len == 7):
                    if (exe_list[3] == "detect"):
                        execstr = execstr + "if block "+ exe_list[4] + " " +exe_list[5] + " " +exe_list[6]+" "
            if (spexe.command_type == "other"):
                if (not Command_header):
                    execstr = execstr + "run "
                execstr = execstr + exe_list[0]
        return execstr
    #-----------------------------
    def splitExecute(self):
        execute_list = []
        oldExe = self.oldExecute[self.prt:]
        exeStructure = self.ExecuteType()
        #---
        if (self.ifexit(oldExe[:1] != "/")):
            oldExe = "/" + oldExe 
            self.prt = self.prt - 1
        
        if (self.ifexit(oldExe[:9] == "/execute ")):
            self.local_prt = 9
            execute_list.append(oldExe[:8])
            self.local_prt_Add(self.SpaceEnd())
        else:
            self.exit_interpret = True

        if (self.ifexit(oldExe[self.local_prt:self.local_prt+1] == "@")):
            str_len = self.findSpace()
            execute_list.append(oldExe[self.local_prt:self.local_prt+str_len])
            self.local_prt_Add(str_len)
            self.local_prt_Add(self.SpaceEnd())
        else:
            self.exit_interpret = True

        if (self.exit()):
            execute_list.append(self.getCoordinate(oldExe))
            if (self.prt + self.local_prt == self.oldExeLenght):
                self.prt = self.prt + self.local_prt
                exeStructure.setExecuteType("execute",execute_list,3)
                return exeStructure
        #----
        if (self.exit()):
            if (oldExe[self.local_prt:self.local_prt+7] == "detect "):
                execute_list.append(oldExe[self.local_prt:self.local_prt+6])
                self.local_prt_Add(self.SpaceEnd() + 6)
            else:
                self.prt = self.prt + self.local_prt    
                exeStructure.setExecuteType("execute",execute_list,3)
                return exeStructure
        if (self.exit()):
            execute_list.append(self.getCoordinate(oldExe))

        if (self.exit()):
            str_len = self.findSpace()
            execute_list.append(oldExe[self.local_prt:self.local_prt+str_len])
            self.local_prt_Add(str_len + self.SpaceEnd())

        if (self.ifexit(self.isCoord(oldExe[self.local_prt:self.local_prt+1]))):
            str_len = self.findSpace()
            execute_list.append(oldExe[self.local_prt:self.local_prt+str_len])
            self.local_prt_Add(str_len + self.SpaceEnd())
            self.prt = self.prt + self.local_prt
            exeStructure.setExecuteType("execute",execute_list,7)
            return exeStructure
        else:
            self.exit_interpret = True
        #---
        self.exit_interpret = True
        if (self.exit_interpret):
            #print ("**Not execute**")
            exeStructure.setExecuteType("other",[oldExe],1)
        return exeStructure
    #---------

    def getCoordinate(self,oldExe):
        #输出标准化的坐标系
        times = 0
        Coord_list =[]
        while (times < 3):
            if (self.isCoord(oldExe[self.local_prt:self.local_prt+1])):
                str_len = self.CoordEnd()
                Coord_list.append(oldExe[self.local_prt:self.local_prt+str_len])
                self.local_prt = self.local_prt+str_len
                if (oldExe[self.local_prt] == " "):
                    self.local_prt = self.local_prt + self.SpaceEnd()
                times = times + 1
            else:
                self.exit_interpret = True
                times = 10
        if (times == 3):
            return f"{Coord_list[0]} {Coord_list[1]} {Coord_list[2]}"
        return ""

    def local_prt_Add(self,jump):
        self.local_prt = self.local_prt + jump

    def isalpha(self,char):
        char = ord(char)
        if ((char >= 97 and char <= 122) or (char >= 65 and char <= 90)):
            return True
        return False

    def isCoord(self,char):
        list = ['1','2','3','4','5','6','7','8','9','0','~','+','-','^']
        for value in list:
            if (char == value):
                return True
        self.exit_interpret = True
        return False

    def CoordEnd(self):
        i = self.prt + self.local_prt+1
        leng = 0
        while(i < self.oldExeLenght):
            if (self.oldExecute[i] == ' ' or self.oldExecute[i] == '~' or self.oldExecute[i] == "^"):
                return leng+1
            i = i+1
            leng = leng+1
        self.exit_interpret = True
        return 0

    def findSpace(self):
        i = self.prt + self.local_prt
        leng = 0
        while(i < self.oldExeLenght):
            if (self.oldExecute[i] == ' '):
                return leng
            i = i+1
            leng = leng+1
        self.exit_interpret = True
        return 0
        
    def SpaceEnd(self):
        i = self.prt + self.local_prt
        leng = 0
        while(i < self.oldExeLenght):
            if (self.oldExecute[i] != ' '):
                return leng
            i = i+1
            leng = leng+1
        self.exit_interpret = True
        return leng

    def exit(self):
        return not self.exit_interpret

    def ifexit(self,bool):
        return (not self.exit_interpret and bool)

class GetBDXPath:
    def __init__(self):
        self.bdx_list = []
        self.inputFrom = ""
        self.inputTo = ""

    def main(self,inputFrom = "",inputTo = ""):
        if (self.searching_BDX()):
            while (inputFrom.strip() == ""):
                inputFrom = input("输入bdx文件路径或序号: ")
                if (self.is_int(inputFrom)):
                    if (int(inputFrom) <= len(self.bdx_list)):
                        inputFrom = self.bdx_list[int(inputFrom)-1]
                    else:
                        print ("未找到此序号")
                        inputFrom = ""
        else:
            while (inputFrom.strip() == ""):
                inputFrom = input("输入bdx文件路径: ")
        while (inputTo.strip() == ""):
            inputTo = input("输入bdx保存路径: ")
        self.inputFrom = inputFrom
        self.inputTo = inputTo

    def searching_BDX(self):
        dir_list = os.listdir(os.getcwd())
        for filename in dir_list:
            if (filename[-4:] == ".bdx"):
                self.bdx_list.append(filename)
        if (len(self.bdx_list) > 0):
            i = 1
            print ("已找到"+str(len(self.bdx_list))+"个bdx文件.")
            for filename in self.bdx_list:
                print (f"  {i}: {filename}")
                i = i+1
            return True
        else:
            print ("未在当前目录找到.bdx文件")
            return False

    def is_int(self,str):
        try:
            int(str)
            return True
        except:
            return False

if __name__ == '__main__':
    if (len(sys.argv) >= 2):
        inputPath = os.path.abspath(sys.argv[1])
        outputPath = os.path.abspath(sys.argv[2])
    else:
        getPath = GetBDXPath()
        getPath.main()
        inputPath = os.path.abspath(getPath.inputFrom)
        outputPath = os.path.abspath(getPath.inputTo)
    #----
    BDump = BDump()
    BDump.main(inputPath,outputPath)

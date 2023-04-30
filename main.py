import sys
import os
from getBDXPath import GetBDXPath
from Bridge.updateExecuteCommand import upgradeExecuteCommand


if __name__ == '__main__':
    if (len(sys.argv) >= 2):
        inputPath = os.path.abspath(sys.argv[1])
        outputPath = os.path.abspath(sys.argv[2])
    else:
        getPath = GetBDXPath()
        getPath.main()
        inputPath = os.path.abspath(getPath.inputFrom)
        outputPath = os.path.abspath(getPath.inputTo)

    upgradeExecuteCommand(inputPath, outputPath)

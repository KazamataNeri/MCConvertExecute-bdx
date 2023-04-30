from BDXConverter.Converter import ReadBDXFile, VisualStructs

# 将当前目录下的 test.bdx 标准化为 ans.json
# ans.json 将生成在当前目录下
readResult, _ = ReadBDXFile('test.bdx')  # 读取 test.bdx
VisualStructs(readResult, 'ans.json')  # 标准化为 JSON

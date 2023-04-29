from BDXConverter.Converter import ReadBDXFile, ConvertListIntoJSONFile

# 将当前目录下的 test.bdx 标准化为 ans.json
# ans.json 将生成在当前目录下
ConvertListIntoJSONFile(ReadBDXFile('test.bdx'), 'ans.json')

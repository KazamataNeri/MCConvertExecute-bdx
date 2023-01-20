# MCConvertExecut-bdx
适用于bdx文件的execute语法转换器
***
在Minecraft 1.19.10.20 中更新了execute语法<br>
MCConvertExecute_bdx 可以将 `bdx` 文件内旧版execute语法替换为新版execute语法<br>
## 安装依赖
```
pip install brotli
```
## 使用方法
```
python convert.py [inputPath] [outputPath]
```
也可直接执行 `python convert.py`
### 对于 `Termux` 
您应该授予 `Termux` 存储权限，否则您将无法运行本程序。
***
下载和使用<br>
1. 在 Termux 执行此命令：
```shell
apt install python && apt install git && pip install brotli -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com && cd /sdcard/Download && git clone https://github.com/KazamataNeri/MCConvertExecute-bdx.git && cd MCConvertExecute-bdx
```
2. 然后在 `Termux` 执行命令 `python convert.py` <br>
   - `convert.py` 文件在目录 `/sdcard/Download/MCConvertExecute-bdx`
 ***
#### `Termux`官方源下载速度过慢?
 - [替换为TUNA源](https://mirrors.tuna.tsinghua.edu.cn/help/termux/)

## 什么是.bdx？
1.  `FastBuilder`支持`.bdx`文件，所以您可以使用`FastBuilder`导入`中国-我的世界基岩版服务器`中的建筑
2. 您可以通过此链接访问“FastBuilder”存储库
   - [ PhoenixBuilder ](https://github.com/LNSSPsd/PhoenixBuilder/)
3. 如果您想购买和使用`FastBuilder`，以下链接可能对您有所帮助
   - [用户中心](https://uc.fastbuilder.pro/)
   - [官方网站](https://fastbuilder.pro/)
## 免责声明(This is not translated into English)
- 若因为使用本软件而造成了任何可能的问题，我不会对此负责。 
- 作者保留有关此工具的所有解释权。
- 特别应当注意的是，您不得将本工具用于盈利用途，除非得到作者的授权。

# 目录
- [目录](#目录)
- [`MCConvertExecut-bdx`](#mcconvertexecut-bdx)
- [依赖项](#依赖项)
- [使用方法](#使用方法)
  - [从源代码运行](#从源代码运行)
- [在 `Termux` 上从源代码运行程序](#在-termux-上从源代码运行程序)
  - [注意事项](#注意事项)
  - [下载和使用](#下载和使用)
  - [`Termux`官方源下载速度过慢?](#termux官方源下载速度过慢)
- [什么是 `BDX` 文件](#什么是-bdx-文件)
- [关于 `PhoenixBuilder`](#关于-phoenixbuilder)
- [免责声明](#免责声明)





# `MCConvertExecut-bdx`
`MCConvertExecut-bdx` 是一个适用于 `BDX` 文件的 `Execute` 语法转换器。

由于 `Minecraft 1.19.10.20` 中更新了命令 `Execute` 的命令格式，为此，我们推出了 `MCConvertExecute_bdx` ，它可以升级 `BDX` 文件中所记录的 `Execute` 命令。

_[注：现在尚且还未支持 `detect block` 中 `方块数据值` 的升级，这是一个待办事项]_


# 依赖项
本项目依赖于 `BDXConverter` 库，因此您需要执行下述命令以安装其。

```
pip install BDXConverter
```





# 使用方法
## 从源代码运行
```
python main.py [inputPath:string] [outputPath:string]
```

当然，您亦可直接执行 `python main.py`





# 在 `Termux` 上从源代码运行程序
## 注意事项
- 您应该授予 `Termux` 存储权限，否则您将无法运行本程序
- 如果您在安装 `BDXConverter` 库时遭遇了错误，请尝试执行下述命令

   ```
   pkg i python-numpy && pip install BDXConverter
   ```



## 下载和使用
1. 在 `Termux` 中执行此命令以拷贝本存储库
```shell
apt install python && apt install git && pip install brotli -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com && pip install numpy -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com && cd /sdcard/Download && git clone https://github.com/KazamataNeri/MCConvertExecute-bdx.git && cd MCConvertExecute-bdx
```

2. 在 `Termux` 执行命令 `python main.py`
   - `main.py` 文件位于路径 `/sdcard/Download/MCConvertExecute-bdx`



## `Termux`官方源下载速度过慢?
 - [替换为 `TUNA` 源](https://mirrors.tuna.tsinghua.edu.cn/help/termux/)





# 什么是 `BDX` 文件
`PhoenixBuilder` 是一个用于 `网易我的世界中国版 · 基岩版租赁服` 的商业化快速建造器，而 `BDX` 文件则是此建造器用于存储 `Minecraft` 建筑结构的 `私有文件格式` 。

如果您希望解析 `BDX` 文件，敬请参阅 [`bdump-cn.md`](https://github.com/LNSSPsd/PhoenixBuilder/blob/main/doc/bdump/bdump-cn.md) 。





# 关于 `PhoenixBuilder`
- 您可以通过此链接访问 `PhoenixBuilder` 的存储库
   - [`PhoenixBuilder`](https://github.com/LNSSPsd/PhoenixBuilder/)
- 您可以通过下述链接访问 `PhoenixBuilder` 的相关网站
   - [`用户中心`](https://uc.fastbuilder.pro/)
   - [`官方网站`](https://fastbuilder.pro/)





# 免责声明
- 基于使用此工具而造成的各种问题，请自行承担
- 此项目的所有贡献者将保留有关此工具的所有解释权
- 此项目使用 [`GNU General Public License v3.0`](https://github.com/KazamataNeri/MCConvertExecute-bdx/blob/main/LICENSE) 协议进行许可和授权
- 当且仅当征得此项目所有贡献者的同意后，您才可以将此项目商业化
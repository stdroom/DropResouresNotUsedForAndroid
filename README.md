# DropResouresNotUsedForAndroid
Drop Resourse Not Used For Android
#删除Android项目中 无用的png资源文件 达到app瘦身目的

后续将继续添加其它app瘦身功能
比如 无用的资源文件 等

##使用方法：
1. 搭建python使用环境 
python3.x不向下兼容，本脚本使用python2.x版本
链接地址：https://docs.python.org/2/
2. 执行脚本 

- linux或者mac系统
./AndroidFilter.py -d 项目路径/app/src/main
- windows系统
python AndroidFilter.py -d 项目路径/app/src/main/

##原理：
1. 采用正则表达式 找到java文件 及 xml文件中的drawable名称
2. 找到drawble*目录下png文件结尾的文件名
3. 将第二步找到的文件名检测是否存在于第一步第一步的结果中，不存在即为准备废弃的文件

##tips:
第一份python代码，不喜勿喷

- mail: leixun33@163.com
- QQ: 378640336

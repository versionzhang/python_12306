Python 12306 抢票小工具
-----------------

# 目前项目不在维护，只修复bug


[12306](http://www.12306.cn/)用python实现的12306抢票小工具

对比另外的两个python项目自己封装了一些数据结构, 添加了自己觉得比较方便的逻辑

具体的更新日志请参考[Changelog](/Changelog.md)

如果有bug欢迎来提issue, 也欢迎开发者PR

## 2019.4.1 修改注意

    1. 添加了对设备指纹的获取, 增加使用依赖库selenium以及chrome driver
    2. 需要自行配置selenium的运行环境,具体可参考网上的教程
    3. 使用缓存文件保存获取的设备指纹, 防止不必要重复获取请求

## python版本支持

3.5以上

## 更新日志

[更新日志文件](Changelog.md)

## Features

- [x] 多日期查询余票
- [x] 自动打码下单
- [x] 用户状态自动检查
- [x] 下单成功邮件通知
- [x] 小黑屋策略
- [x] 预售模式
- [x] 两套下单接口(稳妥起见请选用正常下单流程, 因为是官网web端现在使用的接口)
- [x] 打包项目
- [x] 添加多线程查票模式 (由于查询过于频繁, 可能会被12306限制, 预售的时候建议不要使用)
- [x] CDN加速
- [x] 多组出发到达站配置, 具体参考配置文件`config.yaml_example`
- [x] 代理(已完成,目前此功能在对应的后台管理程序中集成),项目地址[webadmin](https://github.com/versionzhang/python_12306_web)
- [x] web管理后台自动生成项目配置(已完成,目前此功能在对应的后台管理程序中集成),项目地址[webadmin](https://github.com/versionzhang/python_12306_web)

## Usage

### clone项目

适合查看代码并开发

1. `git clone https://github.com/versionzhang/python_12306.git`克隆项目
1. 进入`python_12306`目录, 安装依赖库, `pip install -r requirement.txt`
2. 修改config.yaml_exmpale为config.yaml, 按照说明修改配置文件
3. 安装好依赖之后, 运行`python mainloop.py`来进行抢票

### 使用pip安装项目

适合开箱即用

1. 使用命令 `pip install git+https://github.com/versionzhang/python_12306@master`
即可安装此项目，项目会生成py12306的命令
2. 在你需要运行的文件夹内创建`config.yaml`，编辑好配置文件即可使用 `py12306` 运行程序


## Notice

1. 按照`yaml`的语法修改配置文件
2. 乘车日期已经为多日期, 需要修改对应配置项为列表
3. 现在clone项目之后的直接在项目的根目录下运行mainloop.py文件即可
4. 目前的查询由于加了cdn功能, 改用了未登录的session进行查询, 但是不操作登录后的session会导致登录后的session会频繁掉线,
现在改回来使用登录后的session进行查询. 因为cdn列表是网上获取的,里面有没有伪造的12306cdn服务器不确定,所以开启cdn功能需要谨慎.
后续看如何优化这一块功能

## Repo Status

目前由于12306已经全面开通了候补购票，这个应该不再维护了。不过如果有bug的话还是可以提issue，有时间我会把bug修掉。

## Thanks

1. 感谢[EasyTrain](https://github.com/Why8n/EasyTrain)仓库的创建者Why8n的详细过程分析, 正常下单流程逻辑参考仓库的源代码
2. 感谢[testerSunshine 12306](https://github.com/testerSunshine/12306)仓库的创建者testerSunshine, 参考了仓库的配置文件,以及快速下单的模块接口实现

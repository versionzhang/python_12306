Python 12306 抢票小工具
-----------------

[12306](http://www.12306.cn/)用python实现的12306抢票小工具

对比另外的两个python项目自己封装了一些数据结构, 添加了自己觉得比较方便的逻辑

具体的更新日志请参考[Changelog](/Changelog.md)

如果有bug欢迎来提issue, 也欢迎开发者PR

**2019.1.14 更新了日期查询为多日期,需要修改对应的配置项为列表**

**2019.1.14 dev分支完成了打包功能，使用说明参考下文**

## python版本支持

3.5以上

## Features

- [x] 多日期查询余票
- [x] 自动打码下单
- [x] 用户状态自动检查
- [x] 下单成功邮件通知
- [x] 小黑屋策略
- [x] 预售模式
- [x] 两套下单接口(稳妥期间请选用正常下单流程, 因为是官网web端现在使用的接口)
- [x] 打包项目（目前在dev分支，测试稳定之后合并到主分支）


## TODO List

- [ ] CDN加速(待定)
- [ ] 代理(待定)
- [ ] web管理后台自动生成项目配置

## Usage
### master 分支：

1. 安装依赖库, `pip install -r requirement.txt`
2. 进入python12306文件夹,然后复制config.yaml_exmpale为config.yaml,按照说明修改配置文件
3. 安装好依赖之后,进入python12306文件夹, 运行`python mainloop.py`来进行抢票

### dev 分支

1. 使用命令 `pip install git+https://github.com/versionzhang/python_12306@dev`
即可安装此项目，项目会生成py12306的命令
2. 在你需要运行的文件夹内创建`config.yaml`，编辑好配置文件即可使用 `py12306` 运行程序


## Notice
1. 之前程序会生成pickle文件作为缓存,现在已经删除这个pickle缓存功能, 已经不需要手动删除pickle文件. 改在主程序运行前检查并保存在内存中. 需要注意的是在程序运行期间编辑联系人的话联系人信息并未同步,这种情况需要重新启动程序进行同步
2. 现在乘车日期已经为多日期,需要修改配置文件

## Repo Status
项目还在开发中,目前正常下单流程已经可以跑通, 如果整个流程有什么大的问题欢迎提issue
目前有两种下单模式, 正常下单和快速下单, 快速下单模式有些车次日期会出票失败, 有些则不会. 稳妥期间请使用正常下单模式

## Thanks

1. 感谢[EasyTrain](https://github.com/Why8n/EasyTrain)仓库的创建者Why8n的详细过程分析, 正常下单流程逻辑参考仓库的源代码
2. 感谢[testerSunshine 12306](https://github.com/testerSunshine/12306)仓库的创建者testerSunshine, 参考了仓库的配置文件,以及快速下单的模块接口实现

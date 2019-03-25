Python 12306 抢票小工具
-----------------

[12306](http://www.12306.cn/)用python实现的12306抢票小工具

对比另外的两个python项目自己封装了一些数据结构, 添加了自己觉得比较方便的逻辑

具体的更新日志请参考[Changelog](/Changelog.md)

如果有bug欢迎来提issue, 也欢迎开发者PR

**2019.1.14 更新了日期查询为多日期, 需要修改对应的配置项为列表**

**2019.1.14 完成了打包功能, 使用说明参考下文**

```
使用命令 pip install git+https://github.com/versionzhang/python_12306@master
即可安装此项目，项目会生成py12306的命令
在你需要运行的文件夹内创建config.yaml，编辑好配置文件即可使用
```

**2019.1.16 添加多线程支持**

配置项添加这两个配置
```
# 在线检查时间间隔, 单位秒, 整数
online_check_time: 120

# 是否开启多线程查票
# 不开启多线程查票的话, 多日期的查询是串行的, 开启多线程查询多个日期的查询模式是并行的
# 但是多线程对12306是并发请求的,有可能会导致ip被12306暂时封禁. 这个捡漏的时候可以试一下看看效果
# 预售的时候就暂时不要启用这个选项,会影响你的登录状态,如果被12306视为异常你的登录就会失效, 需要
# 重新登录
multi_threading_enable: False
```

**2019.1.16 添加CDN支持**

```
cdn检测放在程序刚运行时候进行检测, 大概需要10分钟才能检测完毕
```

**2019.1.17 添加多组出发目的地配置**

```
相关的配置项目有修改,请查看下面的几个配置项以及`config.yaml_example`



  # 出发城市列表 只用填写城市名称即可, 比如深圳北，就填深圳就搜得到
  from_stations:
    - "广州"
    - "深圳"

  # 到达城市列表 只用填写城市名称即可, 比如深圳北，就填深圳就搜得到
  to_stations:
    - "郑州"
    - "洛阳"

  # 是否使用车站组, 如果使用车站组, 站点的内容设置的为下面的分组信息, 不使用的话则使用上面的设置, 即
  # from_stations与to_stations的直积, 出发地为[A, B] 到达为[C, D], 则产生的结果为
  # [('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D')]
  # 注意不要配置太多的选项, 配置太多则产生的组合也很多, 组合数为车站出发到达的组合数 * 日期数
  # 处理的优先顺序为日期优先, 例如["DAY1", "DAY2"] 与 [('A', 'C'), ('A', 'D')] 生成的结果为
  # [('DAY1', ('A', 'C')),
  #  ('DAY1', ('A', 'D')),
  #  ('DAY2', ('A', 'C')),
  #  ('DAY2', ('A', 'D'))]
  use_station_group: True

  station_groups:
    # 出发
    - from_station: "郑州"
    # 到达
      to_station: "深圳"
    - from_station: "郑州"
      to_station:  "广州"
    - from_station: "郑州"
      to_station:  "珠海"
```


**2019.1.17 添加是否保存图片在本地的配置项, 添加微信通知**

```
auto_code_enable: False
# 是否保存图片在当前文件夹内，如果开启则直接保存图片到当前文件夹内
# 如果不开启则直接前台显示图片
save_img_enable: True

# 是否开启微信通知
weixin_notice_enable: True
# server酱key
weixin_sckey: server酱key
```


**2019.3.25 添加免费打码平台**

使用[https://12306.jiedanba.cn/](https://12306.jiedanba.cn/)免费打码
具体配置文件内修改配置项

```
auto_code_method: freeapi
```

## python版本支持

3.5以上

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

## TODO List

- [ ] 代理(待定)
- [ ] web管理后台自动生成项目配置

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

项目还在开发中,目前正常下单流程已经可以跑通, 如果整个流程有什么大的问题欢迎提issue

目前有两种下单模式, 正常下单和快速下单, 快速下单模式有些车次日期会出票失败, 有些则不会. 稳妥起见请使用正常下单模式

## Thanks

1. 感谢[EasyTrain](https://github.com/Why8n/EasyTrain)仓库的创建者Why8n的详细过程分析, 正常下单流程逻辑参考仓库的源代码
2. 感谢[testerSunshine 12306](https://github.com/testerSunshine/12306)仓库的创建者testerSunshine, 参考了仓库的配置文件,以及快速下单的模块接口实现

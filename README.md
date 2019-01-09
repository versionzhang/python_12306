Python 12306 抢票小工具
-----------------

[12306](http://www.12306.cn/)用python实现的12306抢票小工具

临时起意就写了个这样的小工具来玩.对比另外的两个python项目自己封装了一些数据结构, 自己使用起来更顺手.

由于是还在开发过程中,运行程序时会有大量的接口以及json返回的数据,请多见谅.

所有的log信息除了直接输出到console里面,在logs目录下会生成一个buy_ticket.log文件,可以用来debug程序的运行.

完成的有点仓促,也就花了三四天时间写出来的, 多多少少都会有一些bug,如果使用的话, 请见谅

如果有明显的流程性的bug欢迎来提issue, 也欢迎开发者PR

python版本支持
-------------

3.5以上

Usage
---------------------------------
1. 安装依赖库, `pip install -r requriement.txt`
2. 进入python12306文件夹,然后复制config.yaml_exmpale为config.yaml,按照说明修改配置文件
3. 安装好依赖之后,进入python12306文件夹, 运行`python run.py`来进行抢票

Notice
---------------------------------
如果中途更换12306账号需要将已经生成的pickle文件删除
`utils/logincookie.pickle`以及`pre_processing/passengers.pickle`删除, `citydata.pickle`文件不用删除
主要是dump了登录之后的cookie信息以及账号的乘客信息.更换之后需要删除进行重新生成

Repo Status
---------------------------------
项目还在开发中,目前正常下单流程已经可以跑通, 但是代码并未全部覆盖测试,请谨慎使用


Thanks
-------------

1. 感谢[EasyTrain](https://github.com/Why8n/EasyTrain)仓库的创建者Why8n的详细过程分析, 程序下单流程逻辑参考仓库的源代码
2. 感谢[testerSunshine 12306](https://github.com/testerSunshine/12306)仓库的创建者testerSunshine, 参考了仓库的配置文件,以及快速下单的模块接口实现

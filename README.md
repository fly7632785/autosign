# autosign
python写的练手项目,是针对公司的自动签到

### 效果
<img src="screenshot/shot.png" width="100%"/>

### 功能
python自动签到脚本

1、每天早上固定时间签到（可设置固定时间）

2、每天晚上固定时间签离（可设置固定时间）

3、不设置就是用默认值

4、每天循环（定时器，每天执行（周一到周五））

5、可装在Android手机上一直保持运行

### 思路
1、抓包获取登录接口及其相关的请求信息，包括header和一些请求参数

2、抓包获取签到、签离的登录接口及其信息

3、python脚本编写模拟浏览器请求，在header里面加入抓包获取的header

4、python编写好定时器脚本

5、完了python脚本之后，可以在Android手机上装一个[Qpython3](http://www.qpython.com)

6、然后在Android手机上跑python脚本就ok了，注意国产的rom一般带有防杀后台功能，比如小米手机有可以锁住应用不杀


## 腾讯会议自动入会脚本(Auto sign in the tencent meeting)
此脚本的前身功能不太完善,因此有了此次优化



###1. 按要求编辑lessons.csv文件(可用记事本打开)

`大概按设置的时间前5分钟进入会议,会议结束1分钟左右退出会议`
`如有更精密的开会时间要求,num(几节课)可以为小数,开会时间为40*num+10(num-1)即50*num-10`

###2. Run

`python AutoSignIn.py`


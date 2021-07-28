# 介绍
Jetson Nano 是一款简易的边缘深度学习（DL）设备，这是[基准评测](http://finance.sina.com.cn/stock/relnews/us/2019-10-24/doc-iicezzrr4560753.shtml)。  
我们已经将nano用于真实建筑室内统计人员项目中，并且较稳运行。作为智能边缘硬件，它完成的工作有每分钟统计摄像头视野内人员数量，并且通过wifi发送到树莓派Mysql数据库中。为方便小伙伴们复刻使用，本文将介绍如何安装nano系统，配置DL和FCHD环境，以及与摄像头和树莓派通讯。整体安装分为**快速安装版**和**逐步安装版**，选择其一进行即可。


# 逐步安装版
此节我们会一步步介绍如何安装配置和调试nano。在此之前，请准备一个USB摄像头，显示屏，鼠标键盘，电源，并连接nano。

## 安装系统和配置环境

我们已将该部分放到此[链接](https://blog.csdn.net/qq_32747775/article/details/105716591?spm=1001.2014.3001.5501)。

## 人头检测

我们考虑FCHD作为人头检测算法，这是我们更新后的代码[链接](https://cloud.tsinghua.edu.cn/d/389746fe05f442d08bd5/)。

下载的文件说明：  
1.demo_video.py：主程序，每分钟读取摄像头，统计人数并发送给树莓派。  
2.demo_video_show.py：同上，但带有展示画面。 
3.interface.py：nano发送到树莓派的代码。  
4.binding.csv：nano和树莓派对应的ip，可根据实际地址修改。  
5.initial_nano.py：读取binding.csv，获取接收方树莓派的ip。

在nano里，删除之前的FCHD文件，将上述链接下载，并放到Desktop目录下。

现在，你可以观看人头检测结果（如果USB摄像头已连接nano），运行：

    python3 demo_video_show.py


## 开机自启动

请参考此[链接](https://shumeipai.nxez.com/2020/06/30/linux-usage-systemd.html)。
当然，myscript.service应该改为

    [Unit]
    Description=My service
    After=network.target
    
    [Service]
    ExecStart=/usr/bin/python3 -u demo_video.py
    WorkingDirectory=/home/skl/Desktop/FCHD-Fully-Convolutional-Head-Detecto
    StandardOutput=inherit
    StandardError=inherit
    Restart=always
    User=skl
  
    [Install]
    WantedBy=multi-user.target
  
然后设置自启动：

    sudo systemctl enable myscript.service
    
现在，nano配置工作已经全部完成。连接USB摄像头，重启nano，可以移去显示屏键盘和鼠标，你只需要在树莓派端查看人数即可。

# 快速安装版

上述步骤比较繁琐，现在我们把所有步骤都汇总成了一个镜像，你需要会使用[镜像拷贝](https://www.cnblogs.com/mr-bike/p/10590275.html)就可以获得上述所有功能！

连接USB摄像头，重启nano，你只需要在树莓派端查看人数即可。


# 附录

## 制作nano镜像

参考使用ubuntu的自带startup Disk Creator工具制作nano镜像。


## 手动修改ip和启动算法

参考[链接](https://cloud.tsinghua.edu.cn/f/56b314cadb7443a189a8/)。


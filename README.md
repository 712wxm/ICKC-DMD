# ICKC-DMD
 
实验安装环境过程
以下一些通过Apt安装的软件都是必须的:
1.	sudo apt-get install python python-pip python-dev libffi-dev libssl-dev
2.	sudo apt-get install python-virtualenv python-setuptools
3.	sudo apt-get install libjpeg-dev zlib1g-dev swig
如果要使用基于Django开发的Web界面, 则MongoDB是必须要安装的:
sudo apt-get install mongodb
出现错误  文件被锁无法安装
解锁被锁住的文件Sudo chmod -R 7777   /var/lib/dpkg/lock-frontend
 
成功安装
如要使用PostgreSQL数据库(推荐), PostgreSQL也必须安装:
sudo apt-get install postgresql libpq-dev
Tcpdump用于抓取恶意软件运行过程中产生的所有流量。安装命令:
sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump
getcap /usr/sbin/tcpdump
输出：
/usr/sbin/tcpdump = cap_net_admin,cap_net_raw+eip则表示已正确安装

Volatility 用于分析内存转储文件的可选工具. Cuckoo与Volatility配合，可以更深度和全面的分析，可以防止恶意软件利用rookit技术逃逸沙箱的监控。为了能够工作正常，Cuckoo要求Volatility版本不低于 2.3， 推荐最新版本2.5。
sudo pip install openpyxl ujson pycrypto distorm3  pytz  -i https://pypi.douban.com/simple
下载
git clone https://github.com/volatilityfoundation/volatility.git
cd volatility
sudo python setup.py build
sudo python setup.py install
确认volatility安装无误
python vol.py -h
输出相关命令

当前 M2Crypto 库需要 SWIG 支持. Ubuntu/Debian-like 系统下可以通过以下命令安装:
sudo apt-get install swig
SWIG 安装好之后，通过以下命令安装 M2Crypto:
sudo pip install m2crypto  -i https://pypi.douban.com/simple

	wget http://sourceforge.net/projects/ssdeep/files/ssdeep-2.13/ssdeep-2.13.tar.gz/download -O ssdeep-2.13.tar.gz
	tar -zxf ssdeep-2.13.tar.gz
	cd ssdeep-2.13
	sudo ./configure
	sudo  make install
	ssdeep -V #检查版本 成功

安装request包
pip install request  -i https://pypi.douban.com/simple

使用pip安装dateutil包
pip install python-dateutil  -i https://pypi.douban.com/simple

安装VirtualBox（直接安装）：
实现嵌套虚拟化
sudo apt-get install virtualbox
然后使用VirtualBox安装windows xp
安装完成后安装增强功能工具（类似于VMware的VMware Tools）

Xp镜像讯雷ed2k://|file|zh-hans_windows_xp_professional_with_service_pack_3_x86_cd_x14-80404.iso|630239232|CD0900AFA058ACB6345761969CBCBFF4|/

  直接将下载好的镜像导入到virtualbox 装好以后启动
还需要配置使得两个机器之间互通，设置为host-only

设置共享文件夹，设置增强便于复制粘贴，
在host cuckoo 虚拟机下面的home新建一个文件夹share
cd ~/.cuckoo/agent  里面有个agent.py 需要拷贝到共享文件夹下面
wget https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi
wget http://effbot.org/media/downloads/PIL-1.1.7.win32-py2.7.exe（下载不了，网上找一个能下载的即可）
三个文件准备好，后续需要共享到guest  xp虚拟机里面  可以自己访问网址下载如果网速较慢
配置agent

我们想要agent.py运行但是不能有运行窗口，因为如果有窗口的话，到后面运行cuckoo提交样本时客户机会出错。
	把 agent.py 后缀改成 agent.pyw
	将agent.pyw复制到C:\Python27\文件夹下，双击运行（是没有任何反应的）
	打开cmd，输入netstat -an，查看本地8000端口是否在监听
记得保存一个快照，guest设置基本完毕

虚拟机启动必须通过sudo vitrualbox 
还要继续转发ip




安装Cuckoo
sudo pip install -U pip setuptools
sudo pip install -U cuckoo -i   https://pypi.douban.com/simple
 遇到错误 需要卸载scapy 2.3.3 
sudo apt-get remove python-scapy 即可卸载

重新运行安装成功
 
先启动一下知道配置文件在哪个位置sudo cuckoo -d
后续进入配置即可，前提是已经把host和guest的ip地址都已经设置合适
还需要配置文件
cuckoo.conf
machinery = virtualbox
[resultserver]
ip = 192.168.xx.xx #This is the IP address of the host
port = 2042 #leave default unless you have services running
auxiliary.conf
[sniffer]
# Enable or disable the use of an external sniffer (tcpdump) [yes/no].
enabled = yes
# Specify the path to your local installation of tcpdump. Make sure this
# path is correct.
# You can check this using the command: whereis tcpdump
tcpdump = /usr/sbin/tcpdump
# Specify the network interface name on which tcpdump should monitor the
# traffic. Make sure the interface is active.
# The ifconfig command will show you the interface name.
#自己选择的网络名称    
interface = vboxnet0
virtualbox.conf
machines = 你的虚拟机名字
[你的虚拟机名字]
label = 你的虚拟机名字
platform = windows
ip = 192.168.56.101 # IP address of the guest
snapshot = 你创建的快照名字
reporting.conf
[mongodb]
enabled = yes
还需要注释一部分代码，否则报错
 

运行web界面出现mongodb启动失败
解决方式

创建目录 /data/db
cd /
mkdir data
cd data
mkdir db
查找到mongo的安装路径
root@instance-tbbjrcnc:/# whereis mongo
mongo: /usr/bin/mongo 
然后手动启动mongo
root@instance-tbbjrcnc:/# cd /usr/bin/
root@instance-tbbjrcnc:/usr/bin# sudo ./mongod  -dbpath /data/db/
启动成功！
创建 service 启动，使用命令启动：service  mongodb restart

继续运行web界面 sudo cuckoo web runserver
 
 

正常启动web界面




安装所需要的数据包时候，出现设备空间不足
解决方式 
方式一
cd /tmp/
rm -rf *
方式二
sudo apt-get autoclean
sudo apt-get clean

更换源以后记得要update一下， 安装之前要更新
sudo apt-get update


安装intel-tensorflow
 
$ pip3 install --upgrade setuptools
$ pip3 install --upgrade pip
再次安装即可


清楚垃圾 /var/log  直接rm -rf *
 sudo apt autoremove --purge snapd  清理snapd
磁盘容量不足，可以关机直接克隆一个新的虚拟机，在这个克隆好的虚拟机上面直接扩充足够大的容量，然后下载
sudo apt-get install gparted
下载以后，根据这个博客来更改容量(32条消息) VMware虚拟机扩展磁盘容量_C晨海的博客-CSDN博客_虚拟机扩展磁盘容量

通过df -h 产看已经扩充好了
 

现在来安装所需要的环境
先更新源  sudo apt-get update
再安装一个pip3来安装
sudo apt install python3-pip

再来安装所需要的库
Sudo pip3 install sklearn  intel-tensorflow pandas scikit-learn  imblearn seaborn  -i    https://pypi.douban.com/simple
 

还需要安装 sudo ./install_required_packages.sh


运行出错，将guest 名称设置为默认配置里面的cuckoo1,代码里面需要更改为http
 

Api调用出错  is_xhr  需要将flask依赖的Werkzeug下降到0.17版本
 
使用api  需要 ~/.cuckoo/coonf中cuckoo.conf中的token

启动API服务器
$ sudo service uwsgi start cuckoo-api
$ sudo service nginx start
$ cuckoo api -H 127.0.0.1 -p 8090


启动步骤
1、	先查看host本地虚拟机ip地址(ifconfig)，是否和cuckoo配置文件里面的cuckoo.conf  ip地址一样 
 

2、	再启动guest 靶机 xp 查看ip地址(ipconfig) ，是否和cuckoo配置文件里面的virtualbox.conf ip地址一样  sudo  virtualbox 启动虚拟机 ，特别注意这个虚拟机的名称 快照名称 以及 ip 都要与配置文件里面的一样
  
开始进入文件夹点击agent.pyw  查看端口是否监听8000  netstat -a
 
 
3、	ip一定要在同一个网段，互相在命令窗口ping一下，看是否能够相通
  

4、设置mongdb 初始化状态
cd   /usr/bin/
sudo  ./mongod   -dbpath  /data/db/  (mongod斜杠前有一个点)
 
5、开始启动命令行的cuckoo  sudo cuckoo -d
 
6、开始启动web界面  sudo cuckoo web runserver
 
 

得到报告
 两端中英文报告通过映射ATT&CK来做预测，总体相同
3、	可以在右边查看所映射的相关战术和使用的技术，显示的数字百分比是预测的概率
4、	可以根据更正结果按钮来自己手动点击报告为预测到的字段或者预测错的字段
5、	可以保存为结构化威胁信息表达式（STIX）的输出报告（STIX（Structured Threat Information Expression）是一种用于交换网络威胁情报（cyber threat intelligence，CTI）的语言和序列化格式。STIX的应用场景包括：协同威胁分析、自动化威胁情报交换、自动化威胁检测和响应等。）


# i南航校外自动打卡小工具

## Description

自动进行每天i南航校外打卡，并且邮件通知，可以多人打卡

**免责声明: 此项目只可以用于技术学习讨论，请勿用于实际用于打卡，如果出现信息错误等后果概不负责**

有问题欢迎提出issue~


## Usage

### Step 0

安装Python3、Python3-pip、git、vim和screen，安装requests库

如果没有安装，请及时下载安装

如使用Yum安装包管理器，可以使用如下命令
``` sh
sudo yum install python3 python3-pip git vim -y
```
然后使用pip3安装requests库
``` sh
sudo pip3 install requests
```

### Step 1

下载本项目，可以git clone或Download Zip

例如
``` sh
git clone https://github.com/Wood1314/inuaa.git
```

### Step 2

配置`config.json`

``` sh
cd inuaa
vim config.json
```

然后使用vim编辑`config.json`

|  KEY   | 作用  |
|  ----  | ----  |
| mail_username  | 使用该邮件地址发送邮件提醒，如果不需要发邮件无则填空 |
| mail_password  | 邮件smtp的密码，不同于邮箱密码，请登录邮箱进行设置 |
|  users  |  收件人列表，可以一人或多人  |
|  name  |  收件人名称，可以写昵称，随便写  |
|  student_id  |  打卡学生的学生id  |
|  student_password  | 打卡学生教务密码  |
|  receiver_mail  | 打卡学生的收信箱，用于接收打卡提示  |

建议使用QQ邮箱向QQ邮箱发送。

**举个🌰**

``` json
{
    "mail_username": "123456@qq.com",
    "mail_password": "qwertyuiopasdfgh",
    "smtp_host": "smtp.qq.com",
    "users": [
        {
            "name": "xxxx",
            "student_id": "xxxxx",
            "student_password": "xxxxx",
            "receiver_mail": "xxxx@qq.com"
        },
        {
            "name": "yyyy",
            "student_id": "yyyy",
            "student_password": "yyyy",
            "receiver_mail": "yyyy@qq.com"
        }
    ]
}
```
## Step 3
发送通知的邮箱配置smtp邮箱服务，如qq邮箱的配置方法


https://www.ujcms.com/documentation/351.html
## Step 4

后台运行程序

``` bash
nohup python3 -u sign.py >out.log 2>&1 &
```

之后只要主机一直开机就会每天在0点时打卡辣。

https://m.nuaa.edu.cn/ncov/wap/default
https://m.nuaa.edu.cn/ncov/wap/nuaa/index

## Last but not least
如果后续教务处修改打卡规则，可通过f12后进入控制台查看所需的变量信息（当然直接查看元素也是可行的)
![](https://pic.imgdb.cn/item/6254050b239250f7c5d1450f.png)
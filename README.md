# Tsinghua-Internet-Auth

## 起因

最近疑似清华校园网认证网址 [auth4.tsinghua.edu.cn](http://auth4.tsinghua.edu.cn) 挂了，转而使用  [tauth4.tsinghua.edu.cn](http://tauth4.tsinghua.edu.cn) 。但原来的 Windows 认证客户端仍然不能使用，故写了一个小东西用来自动认证校园网。

## 环境需求

- python >= 3.11.9
- 见 requirements.txt

## 使用方法

### 直接使用二进制可执行文件

从 [Release页面](https://github.com/FHYQ-Dong/Tsinghua-Internet-Auth/releases) 下载最新版本的自解压压缩包，双击解压后在命令行中使用：

```bash
# 首次使用
./Tsinghua-Internet-Auth -l "http://login.tsinghua.edu.cn" -u [your-username] -p [your-password]

# 程序会把配置保存到当前目录下 config.json 中，其中包括用户名和密码，虽进行了加密处理，但仍请勿泄露
# 若当前目录下存在由程序生成的 config.json，程序可以自动加载该配置，而不用从命令行传递参数
./Tsinghua-Internet-Auth
```

### 运行Python源码

1. 克隆本项目

   ```bash
   git clone https://github.com/FHYQ-Dong/Tsinghua-Internet-Auth
   cd Tsinghua-Internet-Auth
   ```
2. 创建虚拟环境并安装依赖包

   ```bash
   python -m venv ./venv
   ./venv/Scripts/activate
   pip install -r requirements.txt
   ```
3. 运行

   ```bash
   # 首次使用
   python ./Tsinghua-Internet-Auth.py -l "http://login.tsinghua.edu.cn" -u [your-username] -p [your-password]

   # 程序会把配置保存到当前目录下 config.json 中，其中包括用户名和密码，虽进行了加密处理，但仍请勿泄露
   # 若当前目录下存在由程序生成的 config.json，程序可以自动加载该配置，而不用从命令行传递参数
   python ./Tsinghua-Internet-Auth.py
   ```

**注意：认证成功后程序自动退出，认证失败才会显示失败信息**

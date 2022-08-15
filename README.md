# Shekou-Watchdog

[![License](https://img.shields.io/github/license/BenjiaH/Shekou-Watchdog.svg)](LICENSE)
[![Release](https://img.shields.io/github/release/BenjiaH/Shekou-Watchdog.svg)](https://github.com/BenjiaH/Shekou-Watchdog/releases/latest)
[![Release Date](https://img.shields.io/github/release-date/BenjiaH/Shekou-Watchdog.svg)](https://github.com/BenjiaH/Shekou-Watchdog/releases/latest)

```N/A
   _____ _          _                   __          __   _       _         _             
  / ____| |        | |                  \ \        / /  | |     | |       | |            
 | (___ | |__   ___| | _____  _   _ _____\ \  /\  / /_ _| |_ ___| |__   __| | ___   __ _ 
  \___ \| '_ \ / _ \ |/ / _ \| | | |______\ \/  \/ / _` | __/ __| '_ \ / _` |/ _ \ / _` |
  ____) | | | |  __/   < (_) | |_| |       \  /\  / (_| | || (__| | | | (_| | (_) | (_| |
 |_____/|_| |_|\___|_|\_\___/ \__,_|        \/  \/ \__,_|\__\___|_| |_|\__,_|\___/ \__, |
                                                                                    __/ |
                                                                                   |___/ 
```

一个用于监控蛇口母港至香港国际机场船票的工具，支持微信、邮件实时推送通知。

**代码复用了我之前的自动化项目：[https://github.com/BenjiaH/CDU-ISP-AutoReport](https://github.com/BenjiaH/CDU-ISP-AutoReport)、[Gitee镜像](https://gitee.com/BenjiaH/CDU-ISP-AutoReport)**

## 特别声明

- 本仓库发布的`Shekou-Watchdog`项目中涉及的任何脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。

- 本项目内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布。

- 本仓库拥有者对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害.

- 间接使用脚本的任何用户，包括但不限于建立VPS或在某些行为违反国家/地区法律或相关法规的情况下进行传播, 本仓库拥有者对于由此引起的任何隐私泄漏或其他后果概不负责。

- 请勿将`Shekou-Watchdog`项目的任何内容用于商业或非法目的，否则后果自负。

- 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关脚本。

- 以任何方式查看此项目的人或直接或间接使用`Shekou-Watchdog`项目的任何脚本的使用者都应仔细阅读此声明。本仓库拥有者保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或`Shekou-Watchdog`项目，则视为您已接受此免责声明。

- 您必须在下载后的24小时内从计算机或手机中完全删除以上内容。

- 本项目遵循[`GPL-3.0 License`](LICENSE)协议，如果本特别声明与`GPL-3.0 License`协议有冲突之处，以本特别声明为准。

## 1.托管

- 已开通[托管服务](https://benjiah.gitee.io/page/wechat-push-tutorials/wechat-push-tutorials)

## 2.Features/TODO

- [X] 自动监控
- [X] WeChat、邮件双通道推送结果
- [X] 定时执行
- [X] 多账户
- [X] 实时刷新配置文件
- [X] 高安全性：随机`User-Agent`、HTTPS加密、SSL加密
- [X] 购票直达链接（不完美）
- [ ] 后期计划运行两个服务，分别用来查票和通知，以更高频率查票并缓存结果，需要推送时直接取出对应缓存
- [ ] **急需能共同完成以上TODO的小伙伴，请联系 [benjia.h@qq.com](mailto:benjia.h@qq.com)**

## 3.安装依赖

```bash
pip install -r requirements.txt
```

## 4.使用方法

### 4.1.生成`sendkey`(用作微信推送)(可选)

- 打开[Server酱](https://benjiah.gitee.io/redirect/serversauce)。
- 申请一个`sendkey`，并记录下来。

### 4.2.填写[`config/config.json`](config/config_example.json)

- 重命名`config_example.json`文件为`config.json`。
- 参照[`config.json`文件](config/config_example.json)内说明填写其余内容。

### 4.3.填写[`config/account.csv`](config/account_example.csv)(可选)

- 重命名`account_example.csv`文件为`account.csv`。
- 仿照示例填写内容。
- 可录入多行信息，即可为多账户使用。
- `wechat_push`值为`1`则代表当前账户选择微信推送，`email_push`同理。

### 4.4.运行脚本

```bash
python main.py
```

- 在`Windows`平台下，你可以运行[`run.bat`](run.bat)

```bash
.\Shekou-Watchdog\run.bat 
```

- 在`GNU/Linux`平台下，你可以运行[`run.sh`](run.sh)

```bash
chmod +x Shekou-Watchdog/run.sh
./Shekou-Watchdog/run.sh
```

## 5.CHANGE LOG

- [CHANGELOG.md](CHANGELOG.md)

## 6.程序结构

```N/A
│  .gitignore
│  CHANGELOG.md         <---更新日志
│  LICENSE
│  main.py              <---入口程序
│  README.md
│  run.bat              <---Windows下运行文件
│  run.sh               <---GNU/Linux下运行文件
│
├─common
│      account.py       <---多账户读取模块
│      config.py        <---配置读取模块
│      logger.py        <---日志模块
│      push.py          <---推送模块
│      report.py        <---自动化报告模块
│      service.py       <---服务管理模块
│      utils.py         <---工具模块
│
├─config
│      account.csv      <---多账户管理文件
│      config.json      <---配置文件
│      email_tmpl.html  <---Email模板文件
│
└─log
       log.log          <---日志文件

```

## 7.致谢

- [tangyisheng2/tuixue.cmkschp](https://github.com/tangyisheng2/tuixue.cmkschp/blob/main/LICENSE)
- [easychen/wecomchan](https://github.com/easychen/wecomchan/blob/main/LICENSE)
- [riba2534/wecomchan](https://github.com/riba2534/wecomchan/blob/main/LICENSE)
- [fake_useragent](https://github.com/hellysmile/fake-useragent/blob/master/LICENSE)
- [lxml](https://github.com/lxml/lxml/blob/master/LICENSES.txt)
- [requests](https://github.com/psf/requests/blob/main/LICENSE)
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
- [loguru](https://github.com/Delgan/loguru/blob/master/LICENSE)
- [retrying](https://github.com/rholder/retrying/blob/master/LICENSE)

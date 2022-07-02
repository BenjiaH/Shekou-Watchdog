# Change Log

All notable changes to this project will be documented in this file.

---

## [1.4.0.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.4.0.release)

### (2022-5-10)

- **Incompatible added:[supported json in config file](../../commit/634e5c6538d0da4e175bd803b19cd8c817868f96)**
- Removed:`config/config.ini`
- Changed:adapt to the latest CDU-ISP
- Added:hide personal info and private api in log files
- Added:3 versions of WeChat push code
- Changed:report process
- Changed:moved `res/email_tmpl.html` to `config/email_tmpl.html`
- Changed:moved `scripts/run.sh` to `./run.sh`
- Changed:moved `scripts/run.bat` to `./run.bat`
- Fixed:bugs

---

## [1.3.0.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.3.0.release)

### (2022-3-9)

- **Incompatible changed:[remove single account mode settings segments](../../commit/60093c15c98f1ed23193ac03150aa67a9290fa36)**
- Added:[teacher version](../../tree/teacher)
- Changed:optimized the report process
- Changed:log mode in different levels
- Changed:log file location(move to "CDU-ISP-AutoReport/log/log.log")
- Fixed:check hosts status

---

## [1.2.0.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.2.0.release)

### (2022-1-3)

- **Incompatible changed:configuration segments format([`wechat_type`, `api`, `sendkey`, `userid`](../../commit/bcd6e8304fef833eef22d4940259baa1acec61c9#diff-00064dc5d2c5e2552c4d60b93722af776e9efca92fda5d9c9c06f33ce355f58b))**
- Added:go-scf push channel
- Added:sct.ftqq push channel
- Added:retry to push WeChat message and email
- Removed:sc.ftqq push channel
- Fixed:bugs

---

## [1.1.2.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.1.2.release)

### (2021-7-25)

- Added:error message prompt
- Changed:enable SSL in SMTP
- Fixed:parse the latest record correctly
- Fixed:bugs

---

## [1.1.1.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.1.1.release)

### (2021-6-14)

- Fixed:reset the error flag correctly
- Optimized:other details

---

## [1.1.0.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.1.0.release)

### (2021-4-2)

- **Incompatible changed:configuration segments format([time](../../commit/8f859965bbb635a19ef750daa857c8c7e081dd3e) & [switch](../../commit/1a9f69d8efd757b897bfcacc1249e809bc9b9219))**
- Added:fake_useragent to get random user-agents
- Added:BeautifulSoup4 to match information more stably
- Added:loguru for better logging
- Added:modify Email style by template html file
- Added:debug mode
- Optimized:report process
- Changed:WeChat push style
- Fixed:bugs

---

## [1.0.1.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.0.1.release)

### (2021-2-27)

- Fixed:bugs

---

## [1.0.0.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.0.0.release)

### (2021-2-18)

- Added: Report automatically
- Added: Push notifications in dual channels(Email, Wechat)
- Added: Multiple accounts mode
- Added: Security
- Added: Hosts status checks

---

## 0.0.1

### (2020-6-25)

- Init repo

---

```N/A
   _____ _____  _    _      _____  _____ _____                    _        _____                       _   
  / ____|  __ \| |  | |    |_   _|/ ____|  __ \        /\        | |      |  __ \                     | |  
 | |    | |  | | |  | |______| | | (___ | |__) ______ /  \  _   _| |_ ___ | |__) |___ _ __   ___  _ __| |_ 
 | |    | |  | | |  | |______| |  \___ \|  ___|______/ /\ \| | | | __/ _ \|  _  // _ | '_ \ / _ \| '__| __|
 | |____| |__| | |__| |     _| |_ ____) | |         / ____ | |_| | || (_) | | \ |  __| |_) | (_) | |  | |_ 
  \_____|_____/ \____/     |_____|_____/|_|        /_/    \_\__,_|\__\___/|_|  \_\___| .__/ \___/|_|   \__|
                                                                                     | |                   
                                                                                     |_|                   
```
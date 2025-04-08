# 🌟 An Optimal Sample Selection System Project

## 🛠 技术栈  
- Flask + HTML  

## 📁 项目结构
```
flask_demo/
├── app.py
├── algorithm.py
└── templates/        # 这里必须新建一个文件夹，用于存放index.html，不能与 app.py 并列
    └── index.html
```

## 📱 如何用手机浏览项目页面

你可以通过以下方法在手机上访问本地开发的 Flask 页面：

1. **确保手机和电脑连接在同一个热点或局域网中**
2. **在电脑终端输入命令**（以 macOS 为例）：
   ```bash
   ipconfig getifaddr en0
   ```
   这将显示你的本地 IP 地址（例如：`172.20.10.2`）

3. **在手机浏览器中输入**：
   ```
   http://172.20.10.2:5050
   ```
   注意：
   - `5050` 是你在 `app.py` 中设置的端口号
   - 如果该端口已被占用，你可以在代码中更换为其他未被使用的端口
  
  # 补充方案： 使用 ngrok 实现手机访问本地服务（不需同一局域网）

借助 ngrok，你可以让手机通过公网访问你电脑上的本地服务（比如 http://localhost:5050），不再局限于同一局域网。

---
（一）获取你的真实 Authtoken
1. 登录 ngrok 官网：<https://dashboard.ngrok.com>  
2. 点击左侧菜单：“Your Authtoken” 或直接访问：  
   👉 <https://dashboard.ngrok.com/get-started/your-authtoken>  
3. 你将看到一串长长的字符串，例如：2J8gC2Bq6FHTe3Axxxxx9Gp4wxxxxxxzFXXXXXXd2
（二）绑定你的 ngrok Token 到本地配置
打开终端（Terminal），运行以下命令（用你的 token 替换）：

```bash
ngrok config add-authtoken 2J8gC2Bq6FHTe3Axxxxx9Gp4wxxxxxxzFXXXXXXd2

成功后会显示：
Authtoken saved to configuration file: ~/.ngrok2/ngrok.yml
（三）启动 ngrok 代理本地端口
假设你本地服务运行在 http://localhost:5050，运行：

```bash
ngrok http 5050
你将看到如下内容：

Forwarding                    https://xxxx-xx-xx-xx.ngrok.io -> http://localhost:5050
复制这个 https 开头的链接，在手机浏览器打开即可访问你本地的服务！





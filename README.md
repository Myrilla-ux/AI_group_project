# 🌟 AI Group Project

## 🛠 技术栈  
- Flask  
- HTML  

## 📁 项目结构
```
flask_demo/
├── app.py
├── algorithm.py
└── templates/        # 用于存放前端页面（如 index.html），不能与 app.py 并列
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

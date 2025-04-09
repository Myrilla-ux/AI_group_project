
# 🌟 An Optimal Sample Selection System Project
A Flask-based web application for generating and storing optimal sample groupings based on user-defined parameters.

## 📁 项目结构

```
flask_demo/
├── app.py
├── algorithm.py
├── db_utils.py
├── samples.sql
└── templates/        # 这里必须新建一个文件夹，用于存放 index.html，不能与 app.py 并列
    └── index.html
    └── results.html
```

---
## 🛠 前端技术栈  
- Flask + HTML  

---



## 📱 如何用手机浏览项目页面（局域网）

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

   **注意事项：**
   - `5050` 是你在 `app.py` 中设置的端口号
   - 如果该端口已被占用，你可以在代码中更换为其他未被使用的端口

---

## 🌐 补充方案：使用 ngrok 实现手机访问本地服务（不需同一局域网）

借助 ngrok，你可以让手机通过公网访问你电脑上的本地服务（如 http://localhost:5050），无需处于同一局域网。

---

### ✅ 第一步：获取你的真实 Authtoken

1. 登录 ngrok 官网：<https://dashboard.ngrok.com>  
2. 点击左侧菜单：“Your Authtoken” 或直接访问：  
   👉 <https://dashboard.ngrok.com/get-started/your-authtoken>  
3. 你将看到一串长长的字符串，例如：

   ```
   2J8gC2Bq6FHTe3Axxxxx9Gp4wxxxxxxzFXXXXXXd2
   ```

---

### ✅ 第二步：绑定你的 ngrok Token 到本地配置

打开终端（Terminal），运行以下命令（用你的 token 替换）：

```bash
ngrok config add-authtoken 2J8gC2Bq6FHTe3Axxxxx9Gp4wxxxxxxzFXXXXXXd2
```

成功后会显示：

```bash
Authtoken saved to configuration file: ~/.ngrok2/ngrok.yml
```

---

### ✅ 第三步：启动 ngrok 代理本地端口

假设你本地服务运行在 `http://localhost:5050`，运行：

```bash
ngrok http 5050
```

你将看到类似如下内容：

```
Forwarding                    https://xxxx-xx-xx-xx.ngrok.io -> http://localhost:5050
```

复制这个 `https` 开头的地址，在手机浏览器打开即可访问你的本地服务！

---

##  📦 数据库（本地 MySQL 配置）
以下是如何在 **macOS** 和 **Windows** 上安装、启动、使用 MySQL，并连接到你的 Flask 项目的步骤。
---

### 📥 第一步：安装 MySQL
#### 🖥️ macOS：

打开终端，执行：

```bash
brew install mysql
```

> 请先安装 Homebrew：https://brew.sh/

---

#### 🪟 Windows：

1. 访问官网下载地址：  
   https://dev.mysql.com/downloads/installer/

2. 下载 "MySQL Installer for Windows"

3. 安装时勾选：
   - MySQL Server
   - MySQL Workbench（推荐）
   - MySQL Shell

4. 设置 root 密码（务必记住！）

---

### 🚀 第二步：启动 MySQL 服务

#### 🖥️ macOS：

```bash
brew services start mysql
```

停止服务：

```bash
brew services stop mysql
```

---

#### 🪟 Windows：

使用方式一（推荐）：
- 打开 **XAMPP** 控制面板，点击 MySQL Start

或方式二：
- 打开“服务” (`services.msc`)，找到 `MySQL`，右键 → 启动

---

### 🔑 第三步：登录 MySQL 并设置密码

#### macOS (首次登录不需要密码)：

```bash
mysql -u root
```

然后设置密码：

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY '你的密码';
FLUSH PRIVILEGES;
EXIT;
```

此后用密码登录：

```bash
mysql -u root -p
```

#### Windows：
使用安装时设置的密码：

```bash
mysql -u root -p
```

---

### 🗃️ 第四步：创建数据库和表

```sql
CREATE DATABASE optimal_samples;
USE optimal_samples;

CREATE TABLE results (
  id INT AUTO_INCREMENT PRIMARY KEY,
  identifier VARCHAR(255),
  sample_groups TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### ✅ 第五步：验证是否创建成功

```sql
SHOW TABLES;
DESCRIBE results;
SELECT * FROM results;
```

---

### 🧪 第六步：让 Flask 连接数据库

📁 在 `db_utils.py` 中配置：

```python
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='你的密码',
    database='optimal_samples',
    charset='utf8mb4'
)
```

---

### 📄 页面说明：results.html

该页面用于显示数据库中保存的历史分组结果。

#### 📁 页面文件路径：

```
templates/results.html
```

#### 📞 对应 Flask 路由：

```python
@app.route('/results')
def show_results():
    records = get_all_results()
    return render_template('results.html', records=records)
```

### 🛠 数据查询函数（`db_utils.py`）：

```python
def get_all_results():
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, identifier, sample_groups, created_at FROM results ORDER BY id DESC")
        return cursor.fetchall()
```
---

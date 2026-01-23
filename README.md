# Cross Referencer

本系统通过 Docker Compose 集成 OpenGrok 与 Jenkins，实现代码仓库的自动同步与全文检索索引的持续构建。

## 启动 Docker 容器

```bash
# 使用当前用户创建目录，确保权限充足
mkdir -p ~/opengrok/{src,data,dist,etc,log}
mkdir -p ~/jenkins_home

# 拉取源代码
git clone https://github.com/zhyantao/cross-referencer.git
cd cross-referencer
docker-compose -f docker-compose.yml up -d
```

## 登录 Jenkins 网站

```bash
# Jenkins 依赖 Java 环境
sudo apt install openjdk-25-jre-headless

# 查看 Jenkins 网站密码
docker exec repo-sync cat /var/jenkins_home/secrets/initialAdminPassword
```

- Jenkins: <http://127.0.0.1:8081>

## 同步代码和构建索引

Jenkins 配置方法：<https://pan.quark.cn/s/bb39e2b31f67>

```bash
# 手动拉取代码
python3 scripts/get-code.py

# 手动构建索引
scripts/build-index.sh
```

## 登录 OpenGrok 网站

- OpenGrok: <http://127.0.0.1:8080>

## 定时同步代码

```bash
crontab -e

# 每天 22:30 执行 Python 脚本，并将输出追加到日志文件中
# 格式：分钟 小时 日期 月份 星期 命令
30 22 * * * python3 /path/to/cross-referencer/scripts/get-code.py >> ~/opengrok_logs/cron_check.log
```

重启 cron 服务

```bash
sudo systemctl restart cron
```

## 停止服务

```bash
cd cross-referencer
docker-compose down
```

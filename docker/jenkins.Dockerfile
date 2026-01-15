FROM jenkins/jenkins:lts

USER root

# 备份原文件
RUN cp /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/debian.sources.bak

# 替换为国内源（阿里云）
RUN sed -i 's|http://deb.debian.org/debian|http://mirrors.aliyun.com/debian|g' /etc/apt/sources.list.d/debian.sources
RUN sed -i 's|http://deb.debian.org/debian-security|http://mirrors.aliyun.com/debian-security|g' /etc/apt/sources.list.d/debian.sources

# 清除原有源并更新
RUN apt-get clean && apt-get update

# 设置工作目录
WORKDIR /var/jenkins_home

# 暴露 Jenkins 端口
EXPOSE 8080
EXPOSE 50000

# 启动 Jenkins
CMD ["/usr/bin/tini", "--", "/usr/local/bin/jenkins.sh"]

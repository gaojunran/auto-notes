# 后端项目启动教程

## 安装uv

https://docs.astral.sh/uv/getting-started/installation/

uv是Python环境和包管理器。

## 安装依赖

**在api目录下**运行：

```shell

uv sync

```

## 运行服务端项目

```shell

uv run fastapi dev main.py --port 5100

```

(注意，必须加上`uv run`才是在Python虚拟环境下运行！)

## 建议开发环境

PyCharm + Pydantic 插件

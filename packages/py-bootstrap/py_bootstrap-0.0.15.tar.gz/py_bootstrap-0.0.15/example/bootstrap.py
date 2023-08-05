"""
    需要一些启动项,负责配置加载
"""
from qg_tool.tool import get_host_ip
import os

# eureka app 名称 与获取的配置文件相关
app_name = os.getenv('app_name', 'ttt')
ip = os.getenv('ip', get_host_ip())  # 本机的ip
port = os.getenv('port', 8881)            # 端口需要一个配置表
config_server_name = os.getenv(
    'config_server_name', 'qg-spider-config-server')
eureka_url = os.getenv('eureka_url', 'http://192.168.117.102:8108')
register = os.getenv('register', True)  # 是否注册到eureka
profile = 'prod'
extra_profiles = 'database'
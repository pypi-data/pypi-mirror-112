# from feapder.utils import tools
#
# EMAIL_SENDER = "feapder@163.com"  # 发件人
# EMAIL_PASSWORD = "YPVZHXFVVDPCJGTH"  # 授权码
# EMAIL_RECEIVER = "564773807@qq.com"  # 收件人 支持列表，可指定多个
# # 时间间隔
# WARNING_INTERVAL = 3600  # 相同报警的报警时间间隔，防止刷屏
# WARNING_LEVEL = "DEBUG"  # 报警级别， DEBUG / ERROR
# EMAIL_SMTPSERVER="smtp.163.com"
#
#
# tools.email_warning(
#     message="test3",
#     title="test",
#     message_prefix=None,
#     email_sender=EMAIL_SENDER,
#     email_password=EMAIL_PASSWORD,
#     email_receiver=EMAIL_RECEIVER,
#     rate_limit=WARNING_INTERVAL,
#     email_smtpserver=EMAIL_SMTPSERVER
# )
import feapder

class Mba(feapder.Spider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    __custom_setting__ = dict(
        # MYSQL_IP="localhost",
        # MYSQL_PORT=3306,
        # MYSQL_DB="yinliu_m40_cn",
        # MYSQL_USER_NAME="root",
        # MYSQL_USER_PASS="root",

        # REDIS

        # SPIDER
        SPIDER_THREAD_COUNT=10,  # 爬虫并发数
        SPIDER_SLEEP_TIME=[0.2, 0.5],  # 设置为0,不延时， 下载时间间隔 单位秒。 支持随机 如 SPIDER_SLEEP_TIME = [2, 5] 则间隔为 2~5秒之间的随机数，包含2和5
        SPIDER_MAX_RETRY_TIMES=100,  # 每个请求最大重试次数

        # # 设置代理
        PROXY_EXTRACT_API='http://127.0.0.1:5000/proxy',  # 代理提取API ，返回的代理分割符为\r\n
        PROXY_ENABLE=True,

        # 默认为DEBUG
        LOG_LEVEL='DEBUG',
    )

    failed_num = 0
    failed_max_retry_num = 0

    def start_requests(self):
        # proxy = None
        # # 如果需要添加代理，打开这两行注释即可
        # p = Proxy(crawlerType='requests', proxyType='qingting', username='proxypool', password='123456')
        # proxy = p.get_proxy()
        request = feapder.Request(url="http://httpbin.org/get")
        yield request

    def parse(self, request, response):
        print(response.text)


if __name__ == "__main__":
    Mba(redis_key='feapder:mba').start()  # 采集
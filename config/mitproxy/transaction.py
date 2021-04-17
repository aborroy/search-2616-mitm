from mitmproxy import http, ctx
import time
from os import environ
from json import dumps


class TextContent:

    def request(self, flow: http.HTTPFlow) -> None:
        start = time.time()
        endpoint = flow.request.path
        port = 9999
        url = flow.request.url.replace("172.17.0.2", environ['REPO_URL'])
        if "lastIndexedTxCommitTime" in url and "lastIndexedTxId" in url:
            print(url)
            params = {}
            for key, value in flow.request.query.items():
                params[key] = value
            text_content = {
                "transactions": [],
                "maxTxnCommitTime": params["lastIndexedTxCommitTime"],
                "maxTxnId": params["lastIndexedTxId"]
            }
            text_content = bytes(dumps(text_content), encoding="utf-8")
            flow.response = http.HTTPResponse.make(
                200,
                text_content,
                {"Content-Type": "application/json", "charset": "UTF-8"}
            )
        else:
            flow.request.url = url
            flow.request.port = port
        end = time.time()
        ctx.log.info("*********************************************")
        ctx.log.info(flow.request.url)
        ctx.log.info(str(end - start) + " sec")
        ctx.log.info("*********************************************")


addons = [
    TextContent()
]


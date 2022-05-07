import src.utility.Connector_func as udf
import os
import time


class Connector:

    def __init__(self, urls: dict or list, proxies=udf.spys_proxy()):
        self.urls = urls
        self.proxies = proxies
        self.good_proxies = list()
        self.dict_response = dict()
        self.single_response = list()
        self.data = self.exec()

    def exec(self):

        if isinstance(self.urls, dict):
            print(f"Check list...urls")
            for i, (name_html, url) in enumerate(self.urls.items()):
                # print(f"{i + 1}/{len(self.urls)}")
                succeeded = False

                if not os.path.exists(f"./data/html/{name_html}.html"):

                    print(f"Try to establish connection to: {url},")

                    for proxy in self.good_proxies:
                        time.sleep(200)
                        print(f"using: {proxy['IP']}:{proxy['PORT']}", end=" ")
                        data_response = udf.make_request(url, proxy)

                        if data_response is not None:
                            self.dict_response[name_html] = data_response
                            udf.to_html(name_html, data_response)
                            succeeded = True
                            break

                    if not succeeded:
                        for proxy in self.proxies:
                            print(f"using: {proxy['IP']}:{proxy['PORT']}")
                            data_response = udf.make_request(url, proxy)

                            if data_response is not None:
                                if proxy not in self.good_proxies:
                                    self.good_proxies.append(proxy)
                                self.dict_response[name_html] = data_response
                                udf.to_html(name_html, data_response)
                                break
                            else:
                                self.proxies.remove(proxy)



                else:

                    # print(f"{name_html} already exist. Delete it before retrying connection")

                    file = open(f"./data/html/{name_html}.html", "rb")

                    self.dict_response[name_html] = file

            return self.dict_response




        elif isinstance(self.urls, list):

            for url in self.urls:
                for proxy in self.proxies:

                    data_response = udf.make_request(url, proxy)

                    if data_response is not None:
                        self.single_response = data_response
                        break
            return self.single_response


if __name__ == "__main__":
    pass

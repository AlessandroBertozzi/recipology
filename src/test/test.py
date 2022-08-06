from Connector_func import open_json, make_request
import time


def test_proxy():
    url = "http://ipinfo.io/json"
    proxy_list = "./list_daily_proxy.json"
    proxies = open_json(proxy_list)
    proxies_tested = open_json("./tested_proxy.json")

    for i, proxy in enumerate(proxies):
        tested = False
        print(f"{i + 1}/{len(proxies)}")
        for proxy_tested in proxies_tested:
            if proxy == proxy_tested[0]:
                print(f"{proxy}: Already tested!")
                tested = True
        if not tested:
            start = time.time()
            print(f"Start testing proxy: {proxy}")
            response = make_request(url, proxy)
            end = time.time()
            if response is not None:
                proxies_tested.append([proxy, end - start])
                print(f"SUCCEEDED, {end - start}")
                open_json("./tested_proxy.json", mode="write", data=proxies_tested)
            else:
                proxies_tested.append([proxy, "FAILED"])
                open_json("./tested_proxy.json", mode="write", data=proxies_tested)
                print(f"FAILED")

    return proxies_tested


def working_proxy_list(tested_list):
    proxy_list = list()

    for proxy in tested_list:
        if proxy[1] != "FAILED":
            proxy_list.append(proxy)
    proxy_list.sort(key=lambda x: x[1])

    sorted_proxy_list = list()
    for proxy in proxy_list:
        sorted_proxy_list.append(proxy[0])

    open_json("sorted_proxies_tested.json", mode="write", data=sorted_proxy_list)

    return sorted_proxy_list


if __name__ == "__main__":

    pass

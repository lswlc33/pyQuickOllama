import os
import requests
import json
from configparser import ConfigParser


HOME = "http://localhost:11434"


def get_config():
    config = ConfigParser()
    if not os.path.exists("config.ini"):
        # init config
        config["DEFAULT"] = {
            "model": "",
            "stream": "True",
        }
        with open("config.ini", "w") as f:
            config.write(f)

    config.read("config.ini")
    return {
        "model": config["DEFAULT"]["model"],
        "stream": config["DEFAULT"]["stream"],
    }


def request_api(model, text, stream=True, keep_alive="5m"):
    url = HOME + "/api/generate"

    payload = {
        # 模型名称
        "model": model,
        # 对话内容
        "prompt": text,
        # 是否流式生成
        "stream": stream,
        # 对话预设
        # "template": "",
        # 模型存活时间
        "keep_alive": keep_alive,
    }
    response = requests.post(url, json=payload, stream=stream, timeout=99999)

    os.system("cls")
    print("\nCAT >> ", end="")

    if response.status_code != 200:
        print("Error:", response.status_code)
        print(response.json())
        return

    if stream:
        for chunk in response.iter_content(chunk_size=1024):
            print(json.loads(chunk)["response"], end="")
    else:
        print(response.text)
        print(response.json()["response"])


def get_model_list():
    results = []
    url = HOME + "/api/tags"
    response = requests.get(url)
    response = response.json()
    models = response["models"]
    for model in models:
        result = {
            "name": model["name"],
            "size": f"{round(model['size'] / 1024**3, 2):.2f} G",
            "family": model["details"]["family"],
            "par_size": model["details"]["parameter_size"],
        }
        results.append(result)
    return results


def main_loop(model, stream):
    first_input = 1
    text = ""
    while True:
        if first_input:
            text = input("\nYOU >> ")
            first_input = 0

        os.system("cls")
        print("\nCAT >> Generating...", end="")
        request_api(model, text, stream=stream)
        text = input("\nYOU >> ")


if __name__ == "__main__":
    config = get_config()
    model = ""
    stream = bool(config["stream"])

    os.system("title QuickOllama V2")
    os.system("cls")

    # 如果配置文件中有模型名称，则直接开始对话
    if config["model"]:
        model = config["model"]
        os.system(f"title {model.split(':')[0]} - QuickOllama V2")
        main_loop(model, stream)

    # 否则，列出模型列表供用户选择
    print("模型列表:\n")
    print("加载中...")
    models = get_model_list()

    os.system("cls")
    print("模型列表:\n")
    for index in range(len(models)):
        model_ = models[index]
        print(
            f"{index + 1}. {model_['name']}\t\t   类别: {model_['family']}\t大小: {model_['size']}\t参数大小: {model_['par_size']}"
        )

    index = input("\n请输入序号: ")

    if index not in [str(i) for i in range(1, len(models) + 1)]:
        print("输入有误")
    else:
        model = models[int(index) - 1]["name"]
        os.system(f"title {model.split(':')[0]} - QuickOllama V2")
        os.system("cls")
        print(f"\n选择模型: {model}")

    main_loop(model, stream)

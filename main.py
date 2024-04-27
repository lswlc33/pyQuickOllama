import os

model_list = []


def run_model(model_name):
    os.system("cls")
    os.system(f"ollama run {model_name}")


def check_input(str):
    return 0 <= int(str) - 1 < len(model_list)


def get_model_list():
    f = os.popen("ollama list")
    data = f.readlines()
    # remove header
    for i in range(len(data)):
        if "NAME" in data[i]:
            data = data[i + 1 :]
            break
    # get name from line
    for i in range(len(data)):
        data[i] = data[i].split("\t")[0].strip()
    f.close()
    return data


if __name__ == "__main__":
    os.system("title QuickOllama")
    model_list = get_model_list()

    if not model_list:
        print("No models available")
        os.system("pause")
    else:
        os.system("cls")

        print("Available models:\n")
        for i in range(len(model_list)):
            print(f"{i + 1}. {model_list[i]}")

        print("\nchoose the index to enter")
        index = input("\nType index here:")

        if check_input(index):
            run_model(model_list[int(index) - 1])
        else:
            print("Invalid input")
            os.system("pause")

import json

data_name = 'data_base.json'


def open_json_file_and_write():
    with open(data_name, encoding="utf-8") as file:
        data = json.load(file)

    return data


def save_json_file_and_write(data):
    with open(data_name, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)


def save_text(text, message):
    data = open_json_file_and_write()
    data["users"][message.chat.username] = data["users"][message.chat.username] + text + ". "
    save_json_file_and_write(data)


def start_json_file(message):
    data = open_json_file_and_write()
    data["users"][message.chat.username] = ""
    save_json_file_and_write(data)

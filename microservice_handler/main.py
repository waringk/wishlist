from time import sleep
import json


import requests

if __name__ == '__main__':

    def get_input_string(string):
        return string.replace(' ', '%20')

    def get_microservice_info(data):

        r = requests.get('http://localhost:4758/words?mode=rel_spc&input='+get_input_string(data))
        return r.text

    while True:
        f = open("C:\\Users\\dairy\\followish\\microservice.txt", "r")
        response = f.readline()
        f.close()
        if response and response[0] == '#':
            response_text = response[1:]
            words = response_text.split(' ')
            combined_json = []
            for word in words:
                json_item = json.loads(get_microservice_info(word))
                for item in json_item:
                    combined_json.append(item)
            f = open("C:\\Users\\dairy\\followish\\microservice.txt", "w")
            combined_json.sort(key=lambda x: x["score"], reverse=True)
            f.write(json.dumps(combined_json))
            # print(json.dumps(microservice_result))
            f.close()

        sleep(0.05)

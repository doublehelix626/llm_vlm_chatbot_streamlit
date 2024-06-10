import re
import json
import openai_api_request_glm
import ast
import cv2
import numpy as np


# -*- coding: utf-8 -*-


def draw_coordinate_object(str, response):
    num_str = re.findall(r'\[\[(.*?)\]\]', response)
    print(num_str)
    print(num_str[0])
    print(type(num_str[0]))
    parts = num_str[0].split(';')
    result = [[int(x) for x in part.split(',')] for part in parts]
    print("----")
    print(result)
    # coordinate_num = [int(num) for num in re.findall(r'\b\d{3}\b', num_str[0])]

    if str is not None:
        result_dict = {str: result}
        return result_dict
    result_dict = {"default": result}
    return result_dict


def draw_coordinate_all_object(response):
    # response_llm = "请处理一下这句话"+response
    wrong_dict = {}
    # # global array
    # # num_str = re.findall(r'\[\[(.*?)\]\]', response)
    # # if num_str:
    # #     for i in range(len(num_str)):
    # #         coordinate_num = [int(num) for num in re.findall(r'\b\d{3}\b', num_str[i])]
    # #         if coordinate_num:
    # #             if len(coordinate_num) <= 4:
    # #                 for n in range(len(coordinate_num)):
    # #                     pass
    # messages = [
    #     {
    #         "role": "system",
    #         "content": "You are ChatGLM3, a large language model trained by Zhipu.AI. Follow the user's "
    #                    "instructions carefully. Respond using markdown.",
    #     },
    #     {
    #         "role": "user",
    #         "content": "现在我会给你一段话，在这一段话中会隐藏一些我需要的正确的数字，每个正确的数字都是三位数，包括“000”，按照在句子中出现的顺序，每四个三位数会组成一个形如[x1,y1,x2,"
    #                    "y2]或[[x1,y1,x2,"
    #                    "y2]]的坐标，句子中已经框选的肯定是我要的坐标，但有时候会框选一半，有时候会同时框选多个数字，有时候不会框选，你要根据我的提示语利用我给出的话中的正确的数字，来输出给我多个形如[x1,"
    #                    "y1,x2,y2]格式的坐标，并且要加上每个坐标对应的事物是什么，最后形成python的dict类型。如“A river [[320,417,998,928]] runs through a"
    #                    "city, with a bridge [[302,371,670,447]] crossing it. People [[236,460,262,580;192,465,223,"
    #                    "583;000,543,037,794]] walk along the sidewalk [[000,441,396,932]] next to the river [[320,"
    #                    "417,998,928]].”，最后输出的应该是“{“river”:“[[320,417,998,928]]”,“bridge”:“[[302,371,670,447]]”,"
    #                    "“people”:”[[236,460,262,580]][[192,465,223,583]][[000,543,037,794]]”,”sidewalk”:”[[000,441,"
    #                    "396,932]]”}”"
    #     },
    #     {"role": "assistant",
    #      "content": "好的，我会根据你的指示找出句子中的正确数字并组织成所需的格式。由于你并没有提供具体的句子，我无法开始工作。请提供一个句子，我将尽快为你完成任务。"},
    #     # {
    #     #     "role": "user",
    #     #     "content": "处理这句话,Men [[642,420,740,669;814,435,968,779;137,387,326,819;490,323,552,588]] with dogs [["
    #     #                "596,615,672,726;462,402,516,591;744,638,912,801]] are in a wooded area."
    #     # },
    #     # {
    #     #     "role": "assistant",
    #     #     "content": "好的，这是你要处理的句子。我将根据句子中出现的数字为您生成所需的坐标。首先，我们从左到右扫描句子，寻找四个三位数组成的坐标。 Men 的坐标是 [642, 420, 740, "
    #     #                "669]，这是一个有效的坐标。然后，我们继续寻找下一个坐标。接着，我们发现了一个新的有效坐标：[[814, 435, 968, "
    #     #                "779]]。然后，我们再次扫描句子，寻找下一个坐标。接下来，我们找到了一个新的有效坐标：[[137, 387, 326, "
    #     #                "819]]。然后，我们继续扫描句子，寻找下一个坐标。最后，我们找到了最后一个有效坐标：[[490, 323, 552, "
    #     #                "588]]。现在我们已经收集了所有有效的坐标。以下是根据句子中出现的数字生成的字典：```python{\"men\": [[642, 420, 740, 669], [814, 435, "
    #     #                "968, 779], [137, 387, 326, 819], [490, 323, 552, 588]],\"dogs\": [[596, 615, 672, 726], [462, "
    #     #                "402, 516, 591], [744, 638, 912, 801]]}```"
    #     # },
    #     {
    #         "role": "user",
    #         "content": response_llm
    #     }
    #
    # ]
    # response_raw = openai_api_request_glm.client.chat.completions.create(model="chatglm3-6b",
    #                                                                      messages=messages,
    #                                                                      stream=False,
    #                                                                      max_tokens=512,
    #                                                                      temperature=0.8,
    #                                                                      presence_penalty=1.1,
    #                                                                      top_p=0.8)
    # response_llm = response_raw.choices[0].message.content
    # print(response_llm)
    # # print(type(response_llm))
    # code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)
    # dict_blocks = code_block_regex.findall(response_llm)
    # # print(dict_blocks)
    # if dict_blocks:
    #     full_dict = "\n".join(dict_blocks)
    #     print(full_dict)
    #     print(type(full_dict))
    #     if full_dict.startswith("python"):
    #         full_dict = full_dict[7:]
    #         print(full_dict)
    #         print(type(full_dict))
    #         result_dict = ast.literal_eval(full_dict)
    #         print(result_dict)
    #         print(type(result_dict))
    #         return result_dict
    pattern = r'(\w+)\s*\[\[(.*?)\]\]'
    matches = re.findall(pattern, response)
    if matches is not None:
        result = {}
        for match in matches:
            word, bracket_content = match
            result[word] = bracket_content.split(';')
        print(result)
        print(type(result))
        for key, value_list in result.items():
            result[key] = [list(map(int, item.split(','))) for item in value_list]
        print(result)
        return result
    return wrong_dict


def draw_bbox(img, coordinate_dict):
    print(type(img))
    img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
    height, width, channels = img.shape
    for key, coords_list in coordinate_dict.items():
        for i in range(len(coords_list)):
            x0 = coords_list[i][0]
            y0 = coords_list[i][1]
            x1 = coords_list[i][2]
            y1 = coords_list[i][3]
            print(x0)
            print(x1)
            x0 = int((x0 * width) / 1000)
            y0 = int((y0 * height) / 1000)
            x1 = int((x1 * width) / 1000)
            y1 = int((y1 * height) / 1000)
            cv2.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, key, (x0, y0 - 10), font, 0.5, (36, 255, 12), 2)
            _, img_binary = cv2.imencode('.jpg', img)
            img = cv2.imdecode(img_binary, cv2.IMREAD_COLOR)
    _, final_binary = cv2.imencode('.jpg', img)
    return final_binary


# text = ("A river [[320,417,998,928]] runs through a city, with a bridge [[302,371,670,447]] crossing it. People [[236,"
#         "460,262,580;192,465,223,583;000,543,037,794]] walk along the sidewalk [[000,441,396,932]] next to the river "
#         "[[320,417,998,928]].")
# results = re.findall(r'\[(.*?)\]', text)
# print(results)
# print(type(results))
# results = re.findall(r'\[\[(.*?)\]\]', text)
# if results:
#     for i in range(len(results)):
#         numbers = [int(num) for num in re.findall(r'\b\d{3}\b', results[i])]
#         if numbers:
#             for n in range(len(numbers)):
#                 pass

# data = {"river": "[[320,417,998,928]]", "bridge": "[[302,371,670,447]]",
#         "people": "[[236,460,262,580]][[192,465,223,583]][[000,543,037,794]]", "sidewalk": "[[000,441,396,932]]"}
# data_json = json.dumps(data)
# print(data_json)
# print(type(data_json))

if __name__ == "__main__":
    text = ("Three men [[356,000,642,997;020,002,306,997;686,000,978,997]] with the same name and same hair [[356,000,"
            "642,997;686,000,978,997;018,000,308,447]] are shown in three different ages, from young to old.")
    text = "A river [[320,417,998,928]] runs through a city, with a bridge [[302,371,670,447]] crossing it. People [[236,460,262,580;192,465,223,583;000,543,037,794]] walk along the sidewalk [[000,441,396,932]] next to the river [[320,417,998,928]]."

    # str = "[[356,000,642,997]]"
    # coordinate_dict = draw_coordinate_all_object(str)
    # # coordinate_dict = draw_coordinate_object("people",str)
    # image = cv2.imread('./cvtest.jpg')
    # _, img_binary = cv2.imencode('.jpg', image)
    # img = draw_bbox(img_binary, coordinate_dict)
    # img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
    # cv2.imshow("Image", img)
    # cv2.waitKey(0)
    # print(test)
    # print(type(test))
    # pattern = r'(\w+)\s*\[\[(.*?)\]\]'
    # matches = re.findall(pattern, text)
    # result = {}
    # for match in matches:
    #     word, bracket_content = match
    #     result[word] = bracket_content.split(';')
    # print(result)
    # print(type(result))
    # for key, value_list in result.items():
    #     result[key] = [list(map(int, item.split(','))) for item in value_list]
    # print(result)
    str = "[[812, 429, 965, 779;495, 329, 551, 586;647, 420, 735, 660;137, 394, 326, 814]]"
    result = draw_coordinate_object("people", str)
    print(result)

# -*- coding: UTF-8 -*-
import json

ddist = [
    {
        "en_name": "void",
        "cn_name": "其他",
        "color": (0, 0, 0),
    },
    {
        "en_name": "road",
        "cn_name": "道路",
        "color": (0, 192, 0),
    },
    {
        "en_name": "Lane Mark",
        "cn_name": "道路线",
        "color": (128, 0, 192),
    },
    {
        "en_name": "sign",
        "cn_name": "标志牌",
        "color": (192, 128, 128),
    },
    {
        "en_name": "Traffic Light",
        "cn_name": "交通灯",
        "color": (255, 0, 0),
    },
    {
        "en_name": "building",
        "cn_name": "建筑",
        "color": (128, 0, 0),
    },
    {
        "en_name": "tree",
        "cn_name": "树",
        "color": (128, 128, 0),
    },
    {
        "en_name": "sky",
        "cn_name": "天空",
        "color": (128, 128, 128),
    },
    {
        "en_name": "Pedestrain",
        "cn_name": "行人",
        "color": (130, 200, 200),
    },
    {
        "en_name": "car",
        "cn_name": "汽车",
        "color": (64, 0, 128),
    },
    {
        "en_name": "Animal",
        "cn_name": "动物",
        "color": (243, 152, 64),
    }
]

with open("label.json", "w") as f:
    f.write(json.dumps(ddist, indent=2, ensure_ascii=False))
print ddist

from random import choice
import argparse
import json


def route_find(s_a, r_a, r_dir):
    with open(r_dir + '/' + s_a + '-' + r_a + '.json', 'r', encoding="cp949") as f:
        result = dict(json.load(f))

    now = s_a
    route = [s_a]
    history_list = [s_a]
    while now != r_a:
        for k, v in result.items():
            if now in v.keys():
                v.pop(now)

        if not result[now]:
            result.pop(now)
            del route[-1]
            del history_list[-1]
            now = history_list[-1]
            continue

        max_v = max(result[now].values())

        max_k_list = list()
        for k, v in result[now].items():
            if v == max_v:
                max_k_list.append(k)

        now = choice(max_k_list)
        route.append(now)
        history_list.append(now)

    return route


def parse_args():
    parser = argparse.ArgumentParser('algolab')
    parser.add_argument('-s', '--send', type=str)
    parser.add_argument('-r', '--receive', type=str)
    parser.add_argument('-d', '--data_dir', type=str, default='data/result')

    return parser.parse_args()


def route_find_cli():
    args = parse_args()
    data_dir = args.data_dir
    s_a = args.send
    r_a = args.receive
    return route_find(s_a, r_a, data_dir)


if __name__ == '__main__':
    # import os
    # base_data = 'D:/PycharmProjects/PRT'
    # f_list = os.listdir(base_data)
    #
    # for f in f_list:
    #     path = base_data + f
    #     # send_address, receive_address = f.split('.')[0].split('-')
    #     send_address, receive_address = '가능동', '쌍문동'
    #     print(send_address, receive_address)
    #     route_find(send_address, receive_address, base_data)
    #     break

    # 직접 파일 실행 시 cli로 실행 가능
    route_find_cli()

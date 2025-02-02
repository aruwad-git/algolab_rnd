import pandas as pd
import json

# -*- encoding: utf-8 -*-

same_dong = dict()
total_dong = list()


def wrong_word_replace(word):
    """
    특수 띄어쓰기와 대쉬가 있어서 바꾸기 위함
    :param word:
    :return:
    """
    replace_word_list = ['\xa0', '\u2764']
    for r_w in replace_word_list:
        word = word.replace(r_w, '')

    return word


def dong_matching(address):
    """
    주소를 법정동으로 변경
    :param address: 주소
    :return: 법정동 or 법정동이 포함되지 않은 경우 원래 주소로 반환
    """

    address = wrong_word_replace(address)

    for s_d in same_dong.keys():
        if s_d in address:

            for gu in same_dong[s_d]:
                if gu in address:
                    return s_d + gu

            else:
                break

    for d in total_dong:
        if d in address:
            return d

    else:
        print('등록되지 않은 동입니다', address)
        return address


def dong_deduplication(route_list):
    """
    중복으로 동이 들어가 있는 경우 제거
    :param route_list: 경로 리스트
    :return: 제거 후 경로 리스트 반환
    """
    conversion_list = [route_list[0]]
    for r in route_list[1:]:
        if r != conversion_list[-1]:
            conversion_list.append(r)
    return conversion_list


def dong_conversion(route_list):
    """
    법정동 기준으로 변환 및 중복 제거
    :param route_list: 경로 리스트
    :return: 최종 변환된 경로 리스트
    """
    route_list = dong_deduplication(route_list)
    route_list = list(map(lambda x: dong_matching(x), route_list))
    return dong_deduplication(route_list)


def make_json(same_dong_file_path, total_dong_file_path, excel_file_path, save_file_path):
    """
    법정동 경로 리스트를 추출하여 json 파일로 저장
    :param same_dong_file_path: 이름이 같은 동들의 정보 파일 경로
    :param total_dong_file_path: 전체 동의 정보 파일 경로
    :param excel_file_path: 엑셀 파일 경로
    :param save_file_path: 저장할 파일 경로
    :return:
    """
    global same_dong, total_dong

    with open(same_dong_file_path, 'r', encoding="cp949") as f:
        same_dong = dict(json.load(f))

    with open(total_dong_file_path, 'r', encoding="cp949") as f:
        total_dong = list(json.load(f))

    # 전달받은 데이터
    ori_df = pd.read_csv(excel_file_path)

    make_list = list()

    for i in ori_df[['sender_address', 'route', 'receiver_address']].iterrows():
        route = list(map(lambda x: x.split('address\': \'')[1], i[1]['route'].split('\'}, {\'')))
        total_route = [i[1]['sender_address']] + route + [i[1]['receiver_address']]

        total_route = dong_conversion(total_route)
        make_list.append(total_route)

    with open(save_file_path, 'w', encoding="cp949") as make_file:
        json.dump({'route': make_list}, make_file, ensure_ascii=False, indent="\t")

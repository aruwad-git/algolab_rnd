"""
학습된 파일로부터 결과  확인 하기
"""
from algolab.preferred_route import route_find
import json
import io
import os


"""
학습된 결과 모두 확인 시
"""
# 학습결과가 저장된 폴더 경로,  경로 안에 출발지-목적지.json 형식의 파일 이름이어야 함
result_dir_path = 'algolab/data/result'
# f_list = os.listdir(result_dir_path)
#
# # 폴더 안 전체 확인
# for f in f_list:
#     path = f'{result_dir_path}/{f}'
#     send_address, receive_address = f.split('.')[0].split('-')
#     result_route = route_find(send_address, receive_address, result_dir_path)
#     print(result_route)


"""
하나의 결과만 확인할 시
"""
send_address = '남대문로1가'
receive_address = '정자동_장안구'
# 같은 이름을 가진 동들에 대한 정보 파일 경로
same_dong_file_path = 'algolab/dong_info/same_dong.json'
with io.open(same_dong_file_path, 'r', encoding='cp949') as f:
    same_dong_dict = json.load(f)

name_check = True

if send_address in same_dong_dict.keys():
    print(f'이름이 같은 동이 존재합니다. {same_dong_dict[send_address]} 중에서 해당하는 지역을 골라 {send_address}_xx구 형태로 변경해야 합니다.')
    name_check = False

if receive_address in same_dong_dict.keys():
    print(f'이름이 같은 동이 존재합니다. {same_dong_dict[receive_address]} 중에서 해당하는 지역을 골라 {receive_address}_xx구 형태로 변경해야 합니다.')
    name_check = False

if name_check:
    result_route = route_find(send_address, receive_address, result_dir_path)
    print(result_route)

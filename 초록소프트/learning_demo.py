"""
경로 추출부터 환경 만들기, 학습 진행하기 데모 파일
"""
from algolab.route_extraction import make_json
from algolab.environment import make_environment
from algolab.reinforcement_learning import learning_start

"""
엑셀 파일에서 법정동 주소를 법정동 기준으로만 추출하여 json 파일로 저장
"""

# # 같은 이름을 가진 동들에 대한 정보 파일 경로
# same_dong_file_path = 'algolab/dong_info/same_dong.json'
# # 전체 동에 대한 정보 파일 경로
# total_dong_file_path = 'algolab/dong_info/total_dong.json'
# # 엑셀 파일 경로
# excel_file_path = 'algolab_data/algoquick_convert_route.csv'
# # 세이브 파일 경로
# save_file_path = 'route_data.json'
# # 실행
# make_json(same_dong_file_path, total_dong_file_path, excel_file_path, save_file_path)

"""
강화학습을 위한 출발지와 목적지별 환경 파일 만들어 json으로 저장
"""

# # 변환된 json 파일 경로
# route_json_file_path = 'algolab/data/last_route_data.json'
# # 전체 동 정보 파일 경로
# dong_json_file_path = 'algolab/dong_info/total_dong.json'
# # 출발지-목적지 별 환경 파일들을 저장할 폴더 경로
# environment_save_dir_path = 'algolab/data/environment'
# # 해당 정보가 없는 파일들을 저장할 폴더 경로
# no_route_save_dir_path = 'algolab/data/no_route'
# make_environment(route_json_file_path, dong_json_file_path, environment_save_dir_path, no_route_save_dir_path)


"""
강화학습 진행
"""

# 환경이 저장된 폴더 경로
environment_dir_path = 'algolab/data/environment'
# 학습 결과를 저장할 폴더 경로
save_dir_path = 'algolab/data/result'
# 학습
learning_start(environment_dir_path, save_dir_path)



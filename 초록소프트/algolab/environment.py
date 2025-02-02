"""
강화학습을 위한 출발지와 목적지별 환경 만들기
"""

from multiprocessing import Pool
from itertools import permutations
from time import time
import json
import io


# -*- coding:utf-8 -*-


class EnvironmentMake:

    def __init__(self):
        self.ori_j_d = None
        self.t_dong = None

        self.route_json_file_path = ''
        self.total_dong_file_path = ''
        self.environment_save_dir_path = ''
        self.no_route_save_dir_path = ''

    def load_json(self):
        print('json load start')
        st = time()
        with io.open(self.route_json_file_path, 'r', encoding='cp949') as f:
            self.ori_j_d = json.load(f)['route']

        print(time() - st, 'json load complete')

    def total_dong(self):
        with io.open(self.total_dong_file_path, 'r', encoding='cp949') as f:
            t_dong = json.load(f)
        self.t_dong = t_dong

    def find_route(self, send, receive, j_d):
        """
        출발지에서 목적지로 이동한 경로 추출
        :param send: 출발지
        :param receive: 목적지
        :param j_d: 실제 루트 리스트
        :return: 실제 루트 리스트, 1차 경로 추출 리스트
        """
        r_l = list()

        for rdx, route in enumerate(j_d):
            if send in route and receive in route:
                send_idx = route.index(send)
                receive_idx = route.index(receive)
                if send_idx < receive_idx:
                    r_l.append(route[send_idx: receive_idx + 1])
                    j_d[rdx].clear()

        return j_d, r_l

    def route_combinations_sort(self, n_r_l):
        """
        길이가 긴 경우의 수로 정렬 - 범위가 작은 경로부터 추출할 경우 큰 범위의 경로가 추출되지 않을 수 있거나 중복 요소가 있을 수 있음
        :param n_r_l: 1차 경로 리스트
        :return: 정렬된 리스트
        """
        s_r_by_len_dict = dict()

        for n_r in n_r_l:
            for rdx, r in enumerate(n_r[:-1]):
                for rdx2, r2 in enumerate(n_r[rdx + 1:]):
                    length = rdx2 + 1

                    if length in s_r_by_len_dict.keys():
                        s_r_by_len_dict[length] = s_r_by_len_dict[length] | {(r, r2)}

                    else:
                        s_r_by_len_dict[length] = {(r, r2)}

        sort_list = list()
        for r_length in sorted(s_r_by_len_dict.keys(), reverse=True):
            reserve = s_r_by_len_dict[r_length] - set(sort_list)

            sort_list += list(reserve)

        return sort_list

    def reward_cal(self, n_r_l):
        """
        리워드 계산
        :param n_r_l: 1,2차를 통해 필요한 경로만 추출된 리스트
        :return: 리워드 값이 포함된 환경
        """
        e = dict()

        for r_l in n_r_l:
            for rdx in range(len(r_l) - 1):
                r = r_l[rdx]
                r2 = r_l[rdx + 1]
                if r != r2:
                    if r in e.keys():
                        if r2 in e[r].keys():
                            e[r][r2] += 1

                        else:
                            e[r][r2] = 1
                    else:
                        e[r] = {r2: 1}

        return e

    def deep_copy(self, data):
        """
        중복된 경로를 사용하지 않기 위해 원본 실제 경로 리스트를 복사
        :param data: 실제 경로 리스트
        :return:
        """
        copy_data = list()
        for d in data:
            route = list()
            for d2 in d:
                route.append(d2)
            copy_data.append(route)

        return copy_data

    def second_find_route(self, s_r_l, j_d):
        """
        1차 경로 추출에서 생성된 2차 경로 찾기
        :param s_r_l: 1차 경로에서 추출된 2차 경우의 수
        :param j_d: 실제 사용된 경로 리스트
        :return: 2차 경우의 수에 따른 경로 리스트 반환
        """
        r_l = list()
        for route in j_d:
            for s, r in s_r_l:
                if s in route and r in route:
                    send_idx = route.index(s)
                    receive_idx = route.index(r)
                    if send_idx < receive_idx:
                        r_l.append(route[send_idx: receive_idx + 1])
                        break

        return r_l

    def make_environment(self, send_receive):
        """
        환경 json 만들기
        :param send_receive: 출발지, 목적지
        :return:
        """
        print(send_receive, 'start')

        send, receive = send_receive

        j_d = self.deep_copy(self.ori_j_d)
        j_d, need_route_list = self.find_route(send, receive, j_d)

        first_len = len(need_route_list)

        if first_len > 0:
            send_receive_list = self.route_combinations_sort(need_route_list)
            need_route_list += self.second_find_route(send_receive_list, j_d)
            environment = self.reward_cal(need_route_list)

            if environment:
                environment['info'] = {'first_len': first_len, 'route_len': len(need_route_list)}
                file_path = f'{self.environment_save_dir_path}/{send}-{receive}.json'

                with io.open(file_path, 'w', encoding="cp949") as make_file:
                    json.dump(environment, make_file, ensure_ascii=False, indent="\t")

        else:
            # 해당 출발지와 도착지의 해당하는 루트가 없는 경우
            file_path = f'{self.no_route_save_dir_path}/{send}-{receive}'
            t = io.open(file_path, 'w', encoding="cp949")
            t.close()

        print(send_receive, 'complete')

    def load_route(self):
        """
        경로 파일 로드 및 경우의 수 반환
        :return:
        """
        self.load_json()
        self.total_dong()

        # 전체 동에서 경우의 수 추출
        route_case = sorted(list(permutations(self.t_dong, 2)), reverse=True)

        # 실제 가지고 있는 동에서만 추출
        # dong_set = set()
        # for i in self.ori_j_d:
        #     dong_set = dong_set.union(set(i))
        #
        # route_case = list(permutations(dong_set, 2))

        print(len(route_case))
        return route_case

    def make(self, multiprocess, core_count):
        """
        환경 만들기
        :param multiprocess: 코어 사용 유무
        :param core_count: 워커 수
        :return:
        """
        route_case = self.load_route()

        if multiprocess:
            p = Pool(core_count)
            p.map(self.make_environment, route_case)
            p.close()
            p.join()

        else:
            for d in route_case:
                self.make_environment(d)


def make_environment(route_json_file_path, total_dong_file_path, environment_save_dir_path,
                     no_route_save_dir_path, multiprocess=False, core_count=16):
    """
    환경 만들기
    :param route_json_file_path: 최종 변환된 경로 json 파일 경로
    :param total_dong_file_path: 전체 동에 대한 정보 파일 경로
    :param environment_save_dir_path: 환경 파일을 저장할 파일 경로
    :param no_route_save_dir_path: 경로가 없는 경우 저장할 폴더 경로
    :param multiprocess: 멀티프로세스 사용 유무
    :param core_count: 사용할 워커 수(코어 수 이하 추천)
    :return:
    """
    e_m = EnvironmentMake()
    e_m.route_json_file_path = route_json_file_path
    e_m.total_dong_file_path = total_dong_file_path
    e_m.environment_save_dir_path = environment_save_dir_path
    e_m.no_route_save_dir_path = no_route_save_dir_path
    e_m.make(multiprocess, core_count)

from multiprocessing import Pool
from random import randint
from copy import deepcopy
import json
import os

s_d_path, e_d_path = '', ''


class ReinforcementLearning:

    def __init__(self, send, receive, random_ratio=100, learning_count=100):

        global s_d_path, e_d_path

        self.environment_dir_path = e_d_path
        self.save_path = s_d_path

        self.send = send
        self.receive = receive

        self.random_ratio = random_ratio
        self.learning_count = learning_count

        self.environment = dict()
        self.value_table = dict()
        self.before_state = ''
        self.now_state = self.send

        self.action = list()

        self.route_list = list()

        self.reward = 0

        self.load_state = False

        self.load_environment()

        if self.load_state:
            self.setting()

    def load_environment(self):
        """
        환경 로드
        :return:
        """
        file_path = f'{self.environment_dir_path}/{self.send}-{self.receive}.json'

        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='cp949') as f:
                    self.environment = dict(json.load(f))
                self.load_state = True

            except Exception as e:
                print('오류 발생', self.send, self.receive)
                e_t = open(f'{self.send}_{self.receive}_environment_load_fail.txt', 'w', encoding='cp949')
                e_t.write(str(e))
                e_t.close()

            self.learning_count = min(self.learning_count, max(map(len, self.environment.values())) * (len(self.environment.items()) - 1))

    def setting(self):
        """
        value_table 생성
        :return:
        """
        self.value_table = deepcopy(self.environment)
        self.value_table.pop('info')
        for k, v in self.value_table.items():
            for k2, v2 in v.items():
                self.value_table[k][k2] = 0.0

    def get_action(self, state):
        """
        다음으로 이동할 수 있는 지역 반환
        :param state: 현재 지역
        :return: 다음으로 이동할 수 있는 지역 반환
        """
        return list(self.value_table[state].keys())

    def get_reward(self, next_state):
        """
        리워드 계산
        :param next_state: 다음 이동 지역
        :return: 현재에서 다음 지역으로 이동할 시에 얻을 수 있는 리워드 값 반환
        """
        return self.environment[self.now_state][next_state]

    def q_value_update(self, next_state):
        """
        q_value 업데이트
        :param next_state: 다음 이동 지역
        :return:
        """
        action = list(set(self.get_action(next_state)) - set(self.route_list))

        value_list = list()
        for a in action:
            value_list.append(self.value_table[next_state][a])

        self.value_table[self.now_state][next_state] = self.reward + sum(map(lambda x: x / len(action), value_list))

    def reset(self):
        """
        하나의 학습 완료 시 초기화
        :return:
        """
        self.before_state = ''
        self.now_state = self.send
        self.reward = 0

        self.route_list = list()

    def learning_start(self):
        """
        학습 진행
        :return:
        """
        if self.load_state:
            l_count = 0

            while self.learning_count > l_count:

                while self.now_state != self.receive:
                    # 이동했던 적이 있는 지역 제외
                    action = list(set(self.get_action(self.now_state)) - set(self.route_list))

                    # 이동 가능한 지역이 없을 시 뒤로
                    if not len(action):
                        self.now_state, next_state = self.before_state, self.now_state
                        self.route_list.pop()
                        break

                    # 랜덤 이동
                    next_state_idx = randint(0, len(action) - 1)
                    next_state = action[next_state_idx]
                    self.route_list.append(next_state)

                    # 보상
                    self.reward = self.get_reward(next_state)

                    # 값 업데이트
                    if next_state != self.receive:
                        self.q_value_update(next_state)

                    self.before_state, self.now_state = self.now_state, next_state

                    # 도착시 계산
                    if self.now_state == self.receive:
                        self.value_table[self.before_state][self.now_state] = self.environment[self.before_state][
                            self.now_state]

                self.reset()
                l_count += 1

            print(self.send, self.receive, '학습 종료')

            with open(f'{self.save_path}/{self.send}-{self.receive}.json', 'w',
                      encoding="cp949") as make_file:
                json.dump(self.value_table, make_file, ensure_ascii=False, indent="\t")

        else:
            print(f'{self.send}-{self.receive}의 환경 파일 없음')


def learning(s_r):
    """
    학습
    :param s_r: 출발지, 목적지
    :return:
    """
    send_address, receive_address = s_r
    rl = ReinforcementLearning(send_address, receive_address, learning_count=10000, random_ratio=100)
    rl.learning_start()


def learning_start(environment_dir_path, save_dir_path, multiprocess=False, core_count=16):
    """
    강화 학습 시장
    :param environment_dir_path: 환경 파일들이 있는 폴더 경로
    :param save_dir_path: 저장할 폴더 경로
    :param multiprocess: 멀티 프로세스 사용 유무
    :param core_count: 멀티프로세스 사용시 사용할 워커 수(코어 갯수 이하 추천)
    :return:
    """
    global s_d_path, e_d_path

    e_d_path = environment_dir_path
    s_d_path = save_dir_path

    f_list = os.listdir(environment_dir_path)
    environment_list = list(map(lambda x: tuple(x.replace('.json', '').split('-')), f_list))

    if multiprocess:
        for e in environment_list:
            learning(e)

    else:
        p = Pool(core_count)
        p.map(learning, environment_list)
        p.close()
        p.join()

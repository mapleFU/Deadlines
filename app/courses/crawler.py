#!/usr/bin/env python3

# This crawler scrape your course table
# from 4m3.tongji.edu.cn
from typing import Tuple

import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery


class Course:
    WEEK_MAP = {
        1: "双",
        2: "单",
        3: "全",
    }

    def parse_tuple(self, beg: int, class_info: list)->Tuple[int, bool]:
        """
        :param beg: 起始序号
        :param class_info: 课程信息的LIST
        :return: int->结束序号，bool能否再入
        """
        # ['42003201',
        # '刘岩', '星期三', '5-6', '双[10-16]', '济事楼516',
        # '曹布阳', '星期三', '5-6', '双[2-8]', '济事楼516',
        # '刘岩', '星期四', '5-6', '[9-17]', '济事楼516',
        # '曹布阳', '星期四', '5-6', '[1-8]', '济事楼516',
        # '系统分析与设计']
        if (len(class_info) - 2) % 5 != 0:
            if (len(class_info) - 2) % 4 == 0:
                step = 4
            else:
                # print(class_info)
                # step = 5
                print("cannot find!")
                return
        else:
            step = 5

        self.teacher.append(class_info[beg * step + 1])
        self.time.append(tuple(class_info[beg * step + 3].split('-')))
        self.week_time.append(class_info[beg * step + 2])
        if step == 5:
            self.location.append(class_info[beg * step + 5])
        else:
            step.location.append('None')
        weekdata = class_info[beg * 5 + 4]
        if weekdata.find('双') != -1:
            week_has = 1
        elif weekdata.find('单') != -1:
            week_has = 2
        else:
            week_has = 3
        weekdata = weekdata[weekdata.find('[') + 1: weekdata.find(']')].split('-')
        self.week_data.append((Course.WEEK_MAP[week_has], *weekdata))

    def __init__(self, class_list):
        """
        解析的SCHEMA
        课程号 -- (教师, 周, beg-end, (单/双)*[第几周开始-第几周最后], 授课地点)+ -- 课程名称
        :param class_list:
        """
        class_list.replace('\n', ' ')
        class_info = class_list.split()
        self.id = class_info[0]
        self.name = class_info[-1]
        run_times = (len(class_info) - 2) // 5
        # 上课老师
        self.teacher: list = list()
        # 上课地址，可能空缺！
        self.location: list = list()
        # 周几上课: 星期一等格式
        self.week_time: list = list()
        # 课时: (beg,end)
        self.time: list = list()
        # 单双周信息(全/单/双, beg , end)
        self.week_data = list()

        for i in range(run_times):
            self.parse_tuple(i, class_info)

    def __str__(self):
        return f'Course({self.get_course_info()})'

    def show(self):
        print(self.id)
        print(self.name)
        print(self.teacher)
        print(self.location)
        print(self.time)
        print(self.week_data)
        print(self.week_time)

    def get_course_info(self):
        course_info = {
            'id': self.id,
            'name': self.name,
            'teacher': self.teacher,
            'location': self.location,
            'time': self.time,
        }
        return course_info


def login(header, s, username=None, password=None):
    '''登陆4m3'''
    if username is None:
        username = input('your student id')
    if password is None:
        password = input('your password')

    startURL = 'http://4m3.tongji.edu.cn/eams/login.action'
    href = 'http://4m3.tongji.edu.cn/eams/samlCheck'
    res = s.get(startURL)
    header['Upgrade-Insecure-Requests'] = '1'
    res = s.get(href, headers=header)
    soup = BeautifulSoup(res.content, 'html.parser')
    jumpURL = soup.meta['content'][6:]
    header['Accept-Encoding'] = 'gzip, deflate, sdch, br'
    res = s.get(jumpURL, headers=header)

    soup = BeautifulSoup(res.content, 'html.parser')
    logPageURL = 'https://ids.tongji.edu.cn:8443' + soup.form['action']
    res = s.get(logPageURL, headers=header)

    data = {'option': 'credential', 'Ecom_User_ID': username, 'Ecom_Password': password, 'submit': '登录'}
    soup = BeautifulSoup(res.content, 'html.parser')
    loginURL = soup.form['action']
    res = s.post(loginURL, headers=header, data=data)

    soup = BeautifulSoup(res.content, 'html.parser')
    str = soup.script.string
    str = str.replace('<!--', ' ')
    str = str.replace('-->', ' ')
    str = str.replace('top.location.href=\'', ' ')
    str = str.replace('\';', ' ')
    jumpPage2 = str.strip()
    res = s.get(jumpPage2, headers=header)

    soup = BeautifulSoup(res.content, 'html.parser')
    message = {}
    messURL = soup.form['action']
    message['SAMLResponse'] = soup.input['value']
    message['RelayState'] = soup.input.next_sibling.next_sibling['value']
    s.post(messURL, headers=header, data=message)


def get_course_table(header, s):
    # get ids
    id_url = 'http://4m3.tongji.edu.cn/eams/courseTableForStd.action?_='
    req_id = s.get(id_url, headers=header)
    find_text = "addInput(form,\"ids\","
    my_file = str(req_id.text)
    start_index = my_file.find(find_text) + len(find_text) + 1
    ids = my_file[start_index:start_index + 9]
    # get semester_id
    find_text = "value:\""
    start_index = my_file.find(find_text) + len(find_text)
    semester_id = my_file[start_index:start_index + 3]

    form_data = {
        'ignoreHead': 1,
        'startWeek': 1,
        'semester.id': str(semester_id),
        'ids': ids,
        'setting.kind': 'std'
    }
    # print(form_data)
    table_url = 'http://4m3.tongji.edu.cn/eams/courseTableForStd!courseTable.action'
    req_table = s.post(table_url, headers=header, data=form_data)
    return req_table


def parse_table(req_table):
    req_bs = BeautifulSoup(req_table.text, 'html.parser')
    raw_table_info = req_bs.findAll('tbody')[0]
    course_info_list = raw_table_info.findAll('td')
    n_class = int(len(course_info_list) / 11)
    class_info_list = []
    for i in range(n_class):
        class_id_num = i * 11 + 1
        class_info_num = i * 11 + 8
        class_name_num = i * 11 + 2
        class_name = str(course_info_list[class_name_num])
        class_info = str(course_info_list[class_info_num])
        class_id = str(course_info_list[class_id_num])
        class_name_pq = PyQuery(class_name).text()
        class_info_pq = PyQuery(class_info).text()
        class_id_pq = PyQuery(class_id).text()
        class_name = class_name_pq.strip()
        class_info = class_info_pq.strip()
        class_id = class_id_pq.strip()
        # if class_info.endswith(']'):
        #     # TODO: 无教室情况处理
        #     class_info = class_info + ' None '
        class_info_list.append(class_id + ' ' + class_info + ' ' + class_name)
    my_class = []
    for each_class in class_info_list:
        my_class.append(Course(each_class))
    return my_class


class TimetableCrawler:
    HEADER = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

    def __init__(self, student_id, student_pwd):
        self.session = requests.session()
        login(TimetableCrawler.HEADER, self.session, student_id, student_pwd)

    def run(self):
        req_table = get_course_table(TimetableCrawler.HEADER, self.session)
        table_contents = parse_table(req_table)
        return table_contents


if __name__ == '__main__':
    t = TimetableCrawler(student_id=1652728, student_pwd=809001)
    for each_course in t.run():
        each_course.show()
        print('--------')
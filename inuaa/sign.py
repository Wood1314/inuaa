# -*- coding: UTF-8 -*-

import requests
import time
import json
import re
import json
from send_mail import send_mail


# 如果发包过快会造成502，如果给多个同学打卡请注意一下请求速度
try_times = 2

# 每次requests请求的延迟(s秒)，太低会封IP
delay = 3


'''
教务处的垃圾命名规则
info: {
                sfzhux: 0,
                zhuxdz: '',
                szgj: '',
                szcs: '',
                szgjcs: '',
                sfjwfh: 0,
                sfyjsjwfh: 0,
                sfjcjwfh: 0,
                sflznjcjwfh: 0,
                sflqjkm: '0',
                jkmys: 0,
                sfjtgfxdq: 0,
                nuaaxgymjzqk:"1",  //新冠疫苗接种情况：
                dyzjzsj:"", //第一针接种时间
                bfhzjyq:"3", //不符合接种要求
                hxyxjzap:"2", //后续意向接种安排
                yjzjsj:"", //预计接种时间
                sftjlkjc: '',
                lkjctlsj: '',
                sfsylkjcss: '',
                gjzsftjlkjc: '',
                gjzlkjctlsj: '',
                gjzsfsylkjcss: '',
                ifhxjc:'', //你是否进行了核酸检测
                hsjconetime:"", //第一次检测时间
                hsjconeplace:"", //第一次检测地点
                hsjconejg:"", //第一次检测结果（1/2/3）
                hsjctwotime:"", //第二次检测时间
                hsjctwoplace:"", //第二次检测地点
                hsjctwojg:"", //第二次检测结果（1/2/3）
                hsjcthreetime:"", //第三次检测时间
                hsjcthreeplace:"", //第三次检测地点
                hsjcthreejg:"", //第三次检测结果（1/2/3）
                hsjcfourtime:"", //第四次检测时间
                    hsjcfourplace:"", //第四次检测地点
                    hsjcfourjg:"", //第四次检测结果（1/2/3）
                    ywchxjctime:"",  //已完成核酸检测次数
                hsjclist:"{}",
                // 新增2
                njrddz:"", //您的今日住址（详细到门牌号、宿舍号）
                gzczxq:"", //工作常驻校区(1,2,3)
                ifznqgfxljs:"",  //7月10日后是否有江宁区中高风险地区旅居史
                iflsqgfxljs:"",  //7月10日后是否有溧水区中高风险地区旅居史
                // ifjrglkjc:"", //7月10日以来是否进入过禄口机场大厅或与机场工作人员有密切接触
                // gtjjsfhm:"", //共同居住人员中是否有黄码或7月10日以来经停机场人员
                // ywchscs:"",  //已完成核酸检测次数
                // gtjzsfhzl:"",  //共同居住人是否已黄码转绿或已解除14天隔离观察
                // sffhddjjgc:"",//是否符合单独居家观察条件（与共同居住人用餐等不交叉）
                // end
                // 新增3
                // ifjgzgfxq:"", //7月10日后是否经过除禄口机场外其他中高风险区
                // jgzgfxrq:"",  //7月10日后最后一次经过中高风险区的日期
                // jgzgfxdq:"",  //7月10日后最后一次经过中高风险区的地区
                //  jgzgfxxxdz:"", //7月10日后最后一次经过中高风险区的详细地址
                 zrwjtw:"",  //昨日晚间体温范围
                 jrzjtw:"", //今日早间体温范围
                 jrlvymjrq:"", //7月10日后最后一次进入过禄口机场大厅或与机场工作人员有密切接触的日期
                 ifcyglq:"", //是否处于隔离期/医学观察期
                // end
                // 新增4
                // newwchsjccs:"",  //替换以前的已完成核酸检测次数
                // dsdecjcsj:"", //倒数第二次核酸检测时间
                // dsdechsjcjgtype:"", //倒数第二次核酸检测地点
                // dsdrchsjcdd:"",  //倒数第二次核酸检测地点
                
                // dsdechsjcjg:"",  //倒数第二次核酸检测结果
                // zhyccjcsj:"", //最后一次核酸检测时间
                // zhycchsjcjgtype:"", //最后一次核酸检测地点
                // zhycchsjcdd:"",  //最后一次核酸检测地点
                
                // zhycchsjcjg:"",  //最后一次核酸检测结果
                wskmyy:"",//请简要说明无苏康码原因
                zhycjgdqifjn:"",//7月10日后最后一次经过中高风险区的地区为中国境内还是中国境外

                dqsfzgfxszqs:"", //当前是否在中高风险地区所在设区市（直辖市为区、县）
                gqsfyzgfxljs:"", //过去21天内是否有中高风险区旅居史（不含交通工具经停）
                gqsfyqzfhryjc:"",//过去21天内是否与确诊/疑似病例/无症状感染者/从中高风险区返回人员（已解除隔离观察的不算）有密切接触
                sfyjwljqyhg:"",//28天内是否有境外旅居史且已经回国


                cjfxsfhs:"", //2022年春季返校后是否已做核酸检测
                bzxyy:"", //不在校原因  1-4
                bzxyydesc:"", //不在校原因其他时候的时候
}
'''

def get_uid_id(cookies):
    '''
    获取id与uid
    '''
    for _ in range(try_times):
        try:
            time.sleep(delay)
            response = requests.get(
                'https://m.nuaa.edu.cn/ncov/wap/default', cookies=cookies)
            response.encoding = 'utf-8'

            # print(response.text)

            uid = re.search(r'"uid":"([0-9]*)"', response.text).group(1)
            id = re.search(r'"id":([0-9]*)', response.text).group(1)
            print(uid, id)
            return uid,id
        except Exception as e:
            print(e)
    # 就这样吧，让他崩溃，万一假打卡了就不好了
    print('获取id、uid失败')
    return False, '获取id、uid失败\n'

def login(login_id, login_password):
    '''
    登陆I南航，返回Cookie，失败返回空串
    '''
    # headers['Cookie'] = ''
    cookies = ''
    for _ in range(try_times):
        try:
            time.sleep(delay)
            r = requests.get(
                'https://m.nuaa.edu.cn/uc/wap/login', cookies=cookies)
            print('get login page:', r.status_code)
           
            cookies = dict(r.cookies)
            # print(r.cookies)


            time.sleep(delay)
            r = requests.get('https://m.nuaa.edu.cn/uc/wap/login/check', cookies=cookies,
                             data='username={}&password={}'.format(login_id, login_password))
            print('login...:', r.status_code)

        
            cookies.update(dict(r.cookies))

            # headers['Cookie'] = cookie
            uid, id = get_uid_id(cookies)
            return cookies, uid, id
        except Exception as e:
            print(e)
            print('login failed.')
            pass
    # raise Exception('lOGIN FAIL')
    return ''


def sign(m, d, user, smtp_host, mail_username, mail_password):

    '''
    签到，并且发送邮件提醒，成功返回True，失败返回False
    '''
    for _ in range(try_times):
        try:
            data = {
                'sfzhux': '0',
                'zhuxdz': '',
                'szgj': '',
                'szcs': '',
                'szgjcs': '',
                'sfjwfh': '0',
                'sfyjsjwfh': '0',
                'sfjcjwfh': '0',
                'sflznjcjwfh': '0',
                'sflqjkm': '4',
                'jkmys': '1',
                'sfjtgfxdq': '0',
                'tw': '2',
                'sfcxtz': '0',
                'sfjcbh': '0',
                'sfcxzysx': '0',
                'qksm': '',
                'sfyyjc': '0',
                'jcjgqr': '0',
                'remark': '',
                'address': '江苏省南京市江宁区秣陵街道慧园路南京航空航天大学将军路校区',
                'geo_api_info': {"type":"complete","position":{"Q":31.939607,"R":118.791155,"lng":118.791155,"lat":31.939607},"location_type":"html5","message":"Get geolocation success.Don't need convert.Get address success.","accuracy":29,"isConverted":1,"status":1,"addressComponent":{"citycode":"025","adcode":"320115","businessAreas":[{"name":"开发区","id":"320115","location":{"Q":31.925973,"R":118.80980399999999,"lng":118.809804,"lat":31.925973}}],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"将军大道","streetNumber":"29号","country":"中国","province":"江苏省","city":"南京市","district":"江宁区","towncode":"320115011000","township":"秣陵街道"},"formattedAddress":"江苏省南京市江宁区秣陵街道慧园路南京航空航天大学将军路校区","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"},
                'area': '江苏省 南京市 江宁区',
                'province': '江苏省',
                'city': '南京市',
                'sfzx': '0',
                'sfjcwhry': '0',
                'sfjchbry': '0',
                'sfcyglq': '0',
                'gllx': '',
                'glksrq': '',
                'jcbhlx': '',
                'jcbhrq': '',
                'bztcyy': '',
                'sftjhb': '0',
                'sftjwh': '0',
                'sftjwz': '0',
                'sfjcwzry': '0',
                'jcjg': '',
                'date': time.strftime("%Y%m%d", time.localtime()),  # 打卡年月日一共8位
                'uid': user['uid'],  # UID
                'created': round(time.time()), # 时间戳
                'jcqzrq': '',
                'sfjcqz': '',
                'szsqsfybl': '0',
                'sfsqhzjkk': '0',
                'sqhzjkkys': '',
                'sfygtjzzfj': '0',
                'gtjzzfjsj': '',
                'created_uid': '0',
                'id': user['id'],# 打卡的ID，其实这个没影响的
                'gwszdd': '',
                'sfyqjzgc': '',
                'jrsfqzys': '',
                'jrsfqzfy': '',
                'ismoved': '0',
                'dqsfzgfxszqs':'0', #当前是否在低风险地区
                'bfhzjyq': '3', #不符合接种要求
                'cjfxsfhs': '1', #春季返校后是否坐核酸
                'gzczxq': '2', #工作常驻校区
                'sfjkyc': '0',
                'sfmrhs': '1',
                'ifcyglq': '0',
                'cjfxsfhs': '1',
            }
            time.sleep(delay)
            r = requests.post('https://m.nuaa.edu.cn/ncov/wap/default/save',
                              data=data, cookies=user['cookie'])
            print('sign statue code:', r.status_code)
            print('sign return:', r.text)
            r.encoding = 'utf-8'
            
            if r.text.find('成功') >= 0:
                print('打卡成功')
                if user['receiver_mail'] != '':
                    send_mail(mail_username, mail_password, smtp_host,
                              user['receiver_mail'], user['name']+'校外打卡成功', '校外打卡成功', user['name'], '老王')
                return True
            else:
                print('打卡失败，尝试重新登陆')
                user['cookie'] = login(user['student_id'], user['student_password'])
        except Exception as e:
            print('尝试失败')
            print(e)
            pass
            # print(r.request.body)
    if user['receiver_mail'] != '':
        send_mail(mail_username, mail_password, smtp_host,
                  user['receiver_mail'], user['name']+'校外打卡GG', '校外打卡GG', user['name'], '老王')
    return False


def main():
    print('------>>>---->启动中<------<<<----')
    last_post = 10086   # 最后一次签到的日期
    
    # 读取配置文件
    with open('config.json', 'r',encoding='UTF-8') as f:
        config = json.loads(f.read())
    smtp_host = config['smtp_host']
    mail_password = config['mail_password']
    mail_username = config['mail_username']
    users = config['users']
    
    # 一起登陆啊，失败了就先空着，等打卡时候再来管他
    for user in users:
        print('Login...:', user['name'])
        user['cookie'], user['uid'], user['id'] = login(user['student_id'], user['student_password'])
    
   

    
    # 每一天先拷贝一下需要打卡的列表，然后打卡
    # 其他时间如果监测到待打卡的列表非空，就重新读打卡
    
    while True:
        t = time.localtime()

        if t.tm_mday != last_post:
            # 新的一天，拷贝一份完整的打卡清单，全部打一遍卡。但是这样做的话每次更新cookie，users也自动更新。

            print('----------开始每日打卡----------')
            to_sign_list = users.copy()

            # 给每个人打卡
            new_list = []   # 未完成打卡的暂时放这里
            for user in to_sign_list[:]:
                print('**********' + user['name'] + '**********')
                if sign(t.tm_mon, t.tm_mday, user, smtp_host, mail_username, mail_password):
                    print('{}邮箱 {}月{}日登陆成功!'.format(
                        user['name'], t.tm_mon, t.tm_mday))
                else:
                    print('{}邮箱 {}月{}日登陆失败!'.format(
                        user['name'], t.tm_mon, t.tm_mday))
                    new_list.append(user)
            to_sign_list = new_list
            last_post = t.tm_mday   # 更新日期

        elif len(to_sign_list) != 0:
            # 一天中的后续尝试，先等待2小时，然后再打卡
            time.sleep(3600)    # 失败用户每一个小时重试一次
        
            print('----------重新打卡尝试----------')
            # 给每个失败的人打卡
            new_list = []   # 未完成打卡的暂时放这里
            for user in to_sign_list[:]:
                print('**********' + user['name'] + '**********')
                if sign(t.tm_mon, t.tm_mday, user, smtp_host, mail_username, mail_password):
                    print('{}邮箱 {}月{}日登陆成功!'.format(
                        user['name'], t.tm_mon, t.tm_mday))
                else:
                    print('{}邮箱 {}月{}日登陆失败!'.format(
                        user['name'], t.tm_mon, t.tm_mday))
                    new_list.append(user)
            to_sign_list = new_list
        # else: 都打完了
        time.sleep(2)

if __name__ == '__main__':
    main()

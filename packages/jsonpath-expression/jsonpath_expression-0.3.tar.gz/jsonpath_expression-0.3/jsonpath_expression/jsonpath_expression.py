#!/usr/bin/env python
# -*- coding: utf-8 -*-

#解析json
import json,jsonpath
"""
yield就是return 返回一个值，并且记住这个返回的位置，下次迭代就从这个位置后(下一行)开始。
city_url = "https://www.zhipin.com/wapi/zpCommon/data/city.json"
res = requests.get(city_url).text     #请求接口
data = jsonpath_list(response=res)    #返回一个生成器generator
print(list(data))                     #返回结果集
"""

class JsonpathExpression(object):
    def jsonpath_list(self,response,re = []):
        """
        生成路径列表
        :param response: json字符串
        :param re: [key,key,value]
        :return: [[key,key,value],[...]] 列表
        """
        if isinstance(response,str) and response.startswith("{"):           #判断response是不是"{}"
            list_re = self.jsonpath_list(response=json.loads(response))          #递归，递归后返回的是该字典下的[[key,key,value],[...]] 列表
            for d in list_re:
                yield d                                                     #类似于 list.append(d)
        elif isinstance(response,dict):                                     #判断response是否为字典类型
            for k,v in response.items():                                    #遍历response,取key、value值
                if isinstance(v,dict):                                      #判断value是否为字典类型
                    list_re = self.jsonpath_list(v,re + [k])                     #递归，递归后返回的是该字典下的[[key,key,value],[...]] 列表
                    for d in list_re:
                        yield d
                elif isinstance(v,list):                                    #判断value是否为列表类型
                    for dic in v:                                           #遍历列表，list下面一定为dict
                        item = v.index(dic)                                 #获取遍历值的下标
                        list_re = self.jsonpath_list(dic, re + [f'{k}[{item}]']) #递归，递归后返回的是该字典下的[[key,key,value],[...]] 列表
                        for d in list_re:
                            yield d
                else:                                                       #如果value不是字典/列表返回键值对
                    yield re+[k,v]                                          #list+list=list 生成[key,key,value] 列表
        else:                                                               #非json字符串和字典
            yield response

    def jsonpath_expression(self,response,value=None):
        """
        生成路径列表
        :param response: json字符串
        :param value: json字符串中，被提取表达式value的值
        :return: （jsonpath_expression：value ）的字典
        """
        datas = {}
        lists = self.jsonpath_list(response=response)
        for list in lists:
            if value:
                if value in list:
                    datas['$.' + '.'.join(list[0:-1])] = list[-1]  #jsonpath表达式拼接
            else:
                datas['$.'+'.'.join(list[0:-1])] = list[-1]   #jsonpath表达式拼接
        return datas if len(datas) >= 1 else None

    def test_jsonpath_expression(self,response,dict_ex_value):
        '''
        测试jsonpath表达式
        :param response: json字符串
        :param dict_ex_value: jsonpath_expression()返回结果
        :return:
        '''
        for k,v in dict_ex_value.items():
            extract_value=jsonpath.jsonpath(json.loads(response),k)[0]
            print(f'表达式为：{k}，原有的值为：{v}，jsonpath取值为: {extract_value}')



#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsonpath_expression.jsonpath_expression import JsonpathExpression

if  __name__ == "__main__" :
    je= JsonpathExpression()
    str1='{}'
    exp_list = je.jsonpath_expression(str1,1)
    je.test_jsonpath_expression(str1,exp_list)

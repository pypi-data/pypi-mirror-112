#!/usr/bin/env python
# -*- coding:utf-8 -*-
from urllib import parse


def get_attributes_from_url(url: str) -> dict:
    """获取网址中的参数字典"""
    # url解码
    url_data = parse.unquote(url)
    # url结果
    result = parse.urlparse(url_data)
    # url里的查询参数
    return parse.parse_qs(result.query)


def get_attribute_value_from_url(url: str, attribute: str) -> str:
    """获取网址中某参数的值"""
    results = get_attributes_from_url(url)
    if attribute not in results:
        return ''
    if len(results[attribute]) == 1:
        return results[attribute][0]
    else:
        return results[attribute]

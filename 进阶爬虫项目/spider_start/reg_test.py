import re

#提取字符串
#替换
#搜索

# info = "姓名:bobby1987 生日:1987年10月1日 本科:2005年9月1日"
#
# # print(re.findall("\d{4}", info))
# match_result = re.match(".*生日.*?(\d{4}).*本科.*?(\d{4})", info)
# print(match_result.group(1))
# print(match_result.group(2))
#
# result = re.sub("\d{4}", "2019", info)
# print(info)
# print(result)
#
# # print(re.search("生日.*\d{4}", info))
# #match方法是从字符串的最开始匹配
#
# match_result = re.search("生日.*?(\d{4}).*本科.*?(\d{4})", info)
#
# print(match_result.group(1))
# print(match_result.group(2))
name = """my name is
bobby
"""
print(re.match(".*bobby", name, re.DOTALL).group())

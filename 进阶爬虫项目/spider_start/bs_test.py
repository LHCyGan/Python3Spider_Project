from bs4 import BeautifulSoup

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>bobby基本信息</title>
    <script src="//code.jquery.com/jquery-1.11.3.min.js"></script>
</head>
<body>
    <div id="info">
        <p style="color: blue">讲师信息</p>
        <div class="teacher_info info">
            python全栈工程师，7年工作经验，喜欢钻研python技术，对爬虫、
            web开发以及机器学习有浓厚的兴趣，关注前沿技术以及发展趋势。
            <p class="age">年龄: 29</p>
            <p class="name bobbyname" data-bind="bobby bobby2">姓名: bobby</p>
            <p class="work_years">工作年限: 7年</p>
            <p class="position">职位: python开发工程师</p>
        </div>
        <p style="color: aquamarine">课程信息</p>
        <table class="courses">
          <tr>
            <th>课程名</th>
            <th>讲师</th>
            <th>地址</th>
          </tr>
          <tr>
            <td>django打造在线教育</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/78.html">访问</a></td>
          </tr>
          <tr>
            <td>python高级编程</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/200.html">访问</a></td>
          </tr>
          <tr>
            <td>scrapy分布式爬虫</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/92.html">访问</a></td>
          </tr>
          <tr>
            <td>django rest framework打造生鲜电商</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/131.html">访问</a></td>
          </tr>
          <tr>
            <td>tornado从入门到精通</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/290.html">访问</a></td>
          </tr>
        </table>
    </div>

</body>
</html>

"""
# bs = BeautifulSoup(html, "html.parser")
# title_tag = bs.title
# print(title_tag.string)
# div_tag = bs.div
# print(div_tag.string)
import re
# div_tag = bs.find("div")
# div_tag = bs.find(id="info-955")
# div_tag = bs.find("div", id="info-955")
# div_tag = bs.find("div", id=re.compile("info-\d+"))
# childrens = div_tag.descendants
# for child in childrens:
#     if child.name:
#         print(child.name)
# parents = bs.find("p",{"class":"name"}).parents
# for parent in parents:
#     print(parent.name)

# previous_sibling = bs.find("p",{"class":"name"}).previous_sibling
# print(previous_sibling.string)
# name_tag = bs.find("p",{"class":"name"})
# print(name_tag["class"])
# print(name_tag["data-bind"])
# print(name_tag.get("class"))
# for sibling in previous_siblings:
#     print(sibling.string)
# div_tags = bs.find_all("div")
# for tag in div_tags:
#     print(tag.string)
#1. 对应库的接口
#2. 换一个库 就要重新学习
# xpath和css选择器

from scrapy import Selector

sel = Selector(text=html)

name_xpath = "//div[1]/div/p[1]/text()"
name = ""
tag_texts = sel.xpath(name_xpath).extract()
if tag_texts:
    name = tag_texts[0]
print(name)

teacher_tag = sel.xpath("//div[@class='teacher_info info']/p")
teacher_tag = sel.xpath("//div[contains(@class, 'teacher_info')]/p")
teacher_info_class = sel.xpath("//div[contains(@class, 'teacher_info')]/@class").extract()

teacher_info = sel.xpath("//p[@class='age']|//p[@class='work_years']")
# info = sel.xpath("//div[contains(@class, 'teacher_i')]/p[last()-1]/text()").extract()
print(teacher_info)

# tag = sel.xpath("//div[1]/div/p[1]/text()").extract()[0]
# tag_texts = sel.xpath("//div[1]/div/p[1]/text()").extract()
# if tag_texts:
#     text = tag_texts[0]
# tag = sel.xpath("//div[1]/div/p[1]/text()").extract()[0]
# #同一个元素可能会存在多种xpath的语法， xpath可以直接获取到值
# #xpath可以使得我们的解析变成可以配置的解析
# pass

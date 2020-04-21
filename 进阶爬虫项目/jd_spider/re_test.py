import re

text = '<a href="//xslsj.jd.com" clstag="shangpin|keycount|product|bbtn" class="hl_red">新松联手机旗舰店</a>'

re_match = re.search('<a href="//(.*).jd.com', text)
if re_match:
    print(re_match.group(1))

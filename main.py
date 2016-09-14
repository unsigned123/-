#注：中文变量为数据的暂存，英文变量为最终结果。

import urllib.request
import re
import os

req = urllib.request.urlopen('https://zhidao.baidu.com/daily')
html = req.read().decode('gbk')
buf = ''
daily_id_str = []
daily_name = []
daily_id = []
daily_buf = []
i = 0
日报 = re.findall(r'/daily/view?.*\n.*\n.*',html)
日报名称 = re.findall(r'title=".*" width="800" height="450"',html)
日报头条名称 = re.findall(r'<span class="banner-title">.*</span>',html)
for each in 日报头条名称:
    daily_buf = re.findall('[\u4E00-\u9FA5]',each)
    for each_name in daily_buf:
        buf += each_name
    daily_name.append(buf)
    buf = ''
for each in 日报名称:
    daily_buf = re.findall(r'[\u4E00-\u9FA5]',each)
    for each_name in daily_buf:
        buf += each_name
    daily_name.append(buf)
    buf = ''
print('欢迎进入百度知道日报 爬虫')
print('下面是今天的百度日报')
for each in 日报:
    daily_id_str = re.findall('id=.*',each)
    for each_id in daily_id_str:
        for each_str in re.findall('\\d',each_id):
            buf += each_str
            buf = buf.replace('2060','')
        daily_id.append(buf)
        buf = ''
b = list(set(daily_id))
b.sort(key=daily_id.index)
daily_id = b
for each_id in daily_id:
    print('id号:%s    日报名称:%s' % (each_id,daily_name[i]))
    i += 1

input_id = input('请输入要爬取的知道日报ID：')
try:
    input_id = int(input_id)
except ValueError:
    print('您的输入有误请检查!')
    exit(0)
print('爬取中...请稍后')
url = 'https://zhidao.baidu.com/daily/view?id=' + str(input_id)

req = urllib.request.urlopen(url)
html = req.read().decode('gbk')
text = re.findall('<p>.*</p>',html)
try:
    os.mkdir('D:\Images')
except OSError:
    pass

for each in text:
    buf += each

buf = buf.replace('<p>','\n')
buf = buf.replace('</p>','\n')
buf = buf.replace('<strong>','\n')
buf = buf.replace('<span style="text-indent:2em;">','\n')
buf = buf.replace('</span>','\n')
buf = buf.replace('</strong>','\n')
buf = buf.replace('&nbsp;','')
buf = buf.replace('<p style="line-height:56px">','\n')
buf = buf.replace('<p style="text-align:center;">','\n')
buf = buf.replace('<span style="text-decoration:underline;">','\n')
buf = buf.replace('<br />','\n')
buf = buf.replace('<br>','\n')
buf = buf.replace('</br>','\n')
buf = buf.replace('<b>','')
buf = buf.replace('<hr />','')
buf = buf.replace('</b>','')
buf = buf.replace('<a>','')
buf = buf.replace('</a>','')
imgs = re.findall('<img src="https://.*?.jpg" />',buf)
img_addrs = re.findall('https://.*?.jpg',buf)
头图 = re.findall('<img id="daily-img" src="https://.*?.jpg" alt=".*的头图">',html)
头图地址 = re.findall('https://.*?.jpg',头图[0])[0]
img_addrs.append(头图地址)
for each_imgs in imgs:
    buf = buf.replace(each_imgs,'[图片]\n')
    for each_addrs in img_addrs:
        imgreq = urllib.request.urlopen(each_addrs)
        with open('D:\\Images\\'+each_addrs.split('/')[len(each_addrs.split('/'))-1],'wb') as f:
            f.write(imgreq.read())

html = req.read().decode('gbk')
with open('知道日报.txt','w') as f:
    f.write('注:图片已经保存到D:\\Images\n\n[头图]')
    f.write(buf)
print('爬取成功!')
os.popen('NOTEPAD 知道日报.TXT')

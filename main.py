#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
from bs4 import BeautifulSoup
from os.path import exists
from lxml import etree

override = False


def delete_useless_content(d):
    # author = d.find('div', class_="_2LbT9q3y_0 _2QmGFWqF_0")
    # author.replaceWith('')

    author_words = d.find('div', class_="_3FoXPaWx_0")
    author_words.replaceWith('')

    navigator = d.find('div', class_="_2DmyW7ex_0 _2QmGFWqF_0")
    navigator.replaceWith('')

    comment = d.find('div', class_="_1qhD3bdE_0 _2QmGFWqF_0")
    comment.replaceWith('')

    image = d.find('img', class_="_1-ZfmNK8_0")
    image.replaceWith('')

    audio = d.find('div', class_="_1Bg5E78Y_0 _25ls2Q2l_0")
    if audio is not None:
        audio.replaceWith('')

    foot_ads = d.find('div', class_="_22WJb59B_0")
    foot_ads.replaceWith('')

    # footImage = d.find('img', class_="_1Bg5E78Y_0 _25ls2Q2l_0")
    # footImage.replaceWith('')

    return d


def do_parse(directory, result):
    files = os.listdir(directory)
    files.sort()
    for file_name in files:
        path = os.path.join(directory, file_name)
        if os.path.isdir(path):
            do_parse(path, result)
        elif not file_name.startswith("._") and file_name.endswith(".html"):
            fp = os.path.join(path)
            with open(fp, 'r') as f:
                content = f.read()
                soup = BeautifulSoup(content, "lxml")
                for tag in soup.find_all('div', class_="_50pDbNcP_0"):
                    result.append(delete_useless_content(tag))
            # break:


def build_pdf(data, fn):
    data = data.replace("（加微信：642945106 发送“赠送”领取赠送精品课程 发数字“2”获取众筹列表。）", "")

    with open("./template.html", 'r') as t:
        template_html = t.read()
    out = template_html.replace("WAIT_TO_REPLACE", data)

    with open("./" + fn + ".html", 'w') as f:
        f.write(out)

    #
    build_cmd = " ".join(["wkhtmltopdf", "'./" + fn + ".html'", "'./pdfs/"+fn + ".pdf'"])
    # build_cmd = " ".join(["wkhtmltopdf", "--minimum-font-size 25", "./" + fn + ".html", "./pdfs/"+fn + ".pdf"])
    print("---> Transform html to pdf\n\t" + build_cmd)
    code = os.system(build_cmd)
    if code == 0:
        os.remove("./" + fn + ".html")


def parse(dirs):
    for d in dirs:
        name = d.split("/")[-1]
        if not override and exists("./pdfs/"+name+".pdf"):
            print(name + " skipped....")
            continue
        print("---> Parse html: {}".format(name))
        # 提取文章 <div>
        result = []
        do_parse(d, result)
        # 拼凑文章成 list
        print("---> Found {} pages".format(len(result)))
        if len(result) == 0:
            print("---> Skipped...")
            continue
        page_html = ""
        for s in result:
            page_html = page_html + str(s) + "</br>"
        # 构建 PDF 文件
        build_pdf(page_html, name)
        print("---< Finished")


parse([
    "/Volumes/Share Disk/极客时间/13-深入剖析Kubernetes",
    "/Volumes/Share Disk/极客时间/09-Go语言核心36讲",
    "/Volumes/Share Disk/极客时间/06-MySQL实战45讲",
    "/Volumes/Share Disk/极客时间/01-数据结构与算法之美",
    "/Volumes/Share Disk/极客时间/24-Java并发编程实战",
    "/Volumes/Share Disk/极客时间/02-Java核心技术36讲",
    "/Volumes/Share Disk/极客时间/08-深入拆解Java虚拟机",
    "/Volumes/Share Disk/极客时间/46-Kafka核心技术与实战",
    "/Volumes/Share Disk/极客时间/47-Java性能调优实战",
    "/Volumes/Share Disk/极客时间/50-深入拆解Tomcat & Jetty",
    "/Volumes/Share Disk/极客时间/84-ZooKeeper实战与源码剖析",
])
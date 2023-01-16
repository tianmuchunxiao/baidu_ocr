# -*- coding: utf-8 -*-
# @Time     : 2022/6/20 11:27
# @Author   : 天目春辉
# @Email    : panxiaochun@yeah.net
# @QQ       : 273239889
# @File     : myocr.py
# @Software : PyCharm
# @Project  : powermath

import base64
import os
import re
import shutil
import sys

import fitz
import requests
import pathlib


class baiduApi(object):
    APIKey = "djgHhDWpnXYdkrqcZhRyVUtc"
    SecretKey = "8RprqrqeAnnaYQDkFxnpn6WgZgyqgTjR"
    token_url = "https://aip.baidubce.com/oauth/2.0/token"
    ocr_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/formula"
    first_text = ""
    second_text = ""
    third_text = ''
    text = ''
    count = 0

    def __init__(self, image):
        self.image = image
        self.get_token()
        self.ocr_image()
        self.divid_text(first_split=None)

    def get_token(self):
        host = f"{self.token_url}?grant_type=client_credentials&client_id={self.APIKey}&client_secret={self.SecretKey}"
        response = requests.get(host)
        self.access_token = response.json().get("access_token")

    def ocr_image(self):
        image = base64.standard_b64encode(self.image)
        body = {
            "image": image,
            "recognize_granularity": "small",
            "detect_direction": "true",
            "disp_formula": "false",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        request_url = f"{self.ocr_url}?access_token={self.access_token}"
        response = requests.post(request_url, headers=headers, data=body)
        print(response)

        self.results = response.json()["words_result"]

    def divid_text(self, first_split=None):

        for result in self.results:
            # print(result["location"]["left"])
            if first_split == None:
                self.first_text += result["words"]

            else:
                if result["location"]["left"] < first_split:
                    self.first_text += result["words"]
                else:
                    self.second_text += result["words"]

        self.text = self.first_text + self.second_text


class PDFToImage(object):
    def __init__(self,source_file):
        self.source_file = source_file


    def generateImage(self, start_page=1, end_page=None):

        pdf_doc = fitz.Document(self.source_file)
        pdf_pages = pdf_doc.page_count
        print(pdf_pages)

        if end_page is None:
            end_page = pdf_pages

        des_file = self.source_file.replace('.PDF','.txt').replace('.pdf','.txt')

        print(des_file)

        with open(des_file, 'a', encoding='utf-8') as f:
            for page_number in range(start_page, end_page):
                page = pdf_doc.load_page(page_number)

                zoom_x = 2
                zoom_y = 2
                mat = fitz.Matrix(zoom_x, zoom_y)

                pix = page.get_pixmap(matrix=mat,alpha=False).tobytes()


                try:
                    ocr_text = baiduApi(pix)

                except:
                    print('今天的额度已经用完了')
                    with open('record.txt', 'w', encoding='utf-8') as record:
                        record.write(self.source_file)
                        record.write('\n')
                        record.write(str(page_number))

                    sys.exit(0)
                f.write(modify(ocr_text.text))

def modify(words):
    words = words.replace(" ", "")
    words = re.sub(r'[^\u4e00-\u9fa5,]+[^\u4e00-\u9fa5]{4,}', lambda m: '$' + m.group(0) + '$', words)

    words = (
        words.replace(r"cos", r"\cos ")
        .replace(r"sin", r"\sin ")
        .replace(r"tan", r"\tan ")
        .replace(r"cot", r"\cot ")
        .replace(r"sec", r"\sec ")
        .replace(r"csc", r"\csc ")
        .replace(r"\cdot", r"\cdot ")
        .replace(r"\cdot s", r"\cdots ")
        .replace(r"\in", r"\in ")
        .replace(r"\in fty", r"\infty ")
        .replace(r"\therefore", r"\therefore ")
        .replace(r"\forall", r"\forall ")
        .replace(r"\leqslant", r"\leqslant ")
        .replace(r"\geqslant", r"\geqslant ")
        .replace(r"\frac", r"\dfrac ")
        .replace(r"\because", r"\because ")
        .replace(r"\exists", r"\exists ")
        .replace(r"\bot", r"\bot ")
        .replace(r"∈", r"\in ")
        .replace(r"≤", r"\leqslant ")
        .replace(r"≥", r"\geqslant ")
        .replace(r"\ne", r"\ne ")
        .replace(r"≠", r"\neq ")
        .replace(r"\frac", r"\dfrac")
        .replace(r"…", r"\cdots ")
        .replace(r"\times", r"\times ")
        .replace(r"\div", r"\div ")
        .replace(r"\angle", r"\angle ")
        .replace(r"\triangle", r"\triangle ")
        .replace(r"\Leftrightarrow", r"\Leftrightarrow ")
        .replace(r"\Leftarrow", r"\Leftarrow ")
        .replace(r"\leftrightarrow", r"\leftrightarrow ")
        .replace(r"\leftarrow", r"\leftarrow ")
        .replace(r"\Rightarrow", r"\Rightarrow ")
        .replace(r"\rightarrow", r"\rightarrow ")
        .replace(r"→", r"\rightarrow ")
        .replace(r"\pm", r"\pm ")
        .replace(r"\alpha", r"\alpha ")
        .replace(r"\beta", r"\beta ")
        .replace(r"\gamma", r"\gamma ")
        .replace(r"\Gamma", r"\Gamma ")
        .replace(r"\delta", r"\delta ")
        .replace(r"\Delta", r"\Delta ")
        .replace(r"\varepsilon", r"\varepsilon ")
        .replace(r"\epsilon", r"\varepsilon ")
        .replace(r"\zeta", r"\zeta ")
        .replace(r"\eta", r"\eta ")
        .replace(r"\theta", r"\theta ")
        .replace(r"\Theta", r"\Theta ")
        .replace(r"\vartheta", r"\vartheta ")
        .replace(r"\omega", r"\omega ")
        .replace(r"\Omega", r"\Omega ")
        .replace(r"\kappa", r"\kappa ")
        .replace(r"\lambda", r"\lambda ")
        .replace(r"\Lambda", r"\Lambda ")
        .replace(r"\mu", r"\mu ")
        .replace(r"\nu", r"\nu ")
        .replace(r"\xi", r"\xi ")
        .replace(r"\Xi", r"\Xi ")
        .replace(r"\pi", r"\pi ")
        .replace(r"\Pi", r"\Pi ")
        .replace(r"\rho", r"\rho ")
        .replace(r"\varrho", r"\varrho ")
        .replace(r"\sigma", r"\sigma ")
        .replace(r"\Sigma", r"\Sigma ")
        .replace(r"\tau", r"\tau ")
        .replace(r"\upsilon", r"\upsilon ")
        .replace(r"\Upsilon", r"\Upsilon ")
        .replace(r"\phi", r"\phi ")
        .replace(r"\Phi", r"\Phi ")
        .replace(r"\varphi", r"\varphi ")
        .replace(r"\chi", r"\chi ")
        .replace(r"\psi", r"\psi ")
        .replace(r"\Psi", r"\Psi ")
        .replace(r"\iota", r"\iota ")
        .replace(r"\odot", r"\odot ")
        .replace(r'A.', r' A. ')
        .replace(r'$A.', r' A. $')
        .replace(r'$B.', r' B. $')
        .replace(r'$C.', r' C. $')
        .replace(r'$D.', r' D. $')
        .replace(r'log', r'\log ')
        .replace(r'lg', r'\lg ')
        .replace(r'\cap', r'\cap ')
        .replace(r'\cup', r'\cup ')
        .replace(r'\min', r'\min ')
        .replace(r'\max', r'\max ')
        .replace(r'ln', r'\ln ')
        .replace(r',$', r'$,')
        .replace(r'.$', r'$.')
        .replace(r'\subset', r'\subset ')
        .replace(r'\notin', r'\notin ')

    )
    words = words + '\n\n'
    print(words)

    return words


if __name__ == "__main__":
    des_path = r'F:\BaiduSyncdisk\学习资源\待学习'
    exist_files = []
    for root,dir,files in os.walk(des_path):
        exist_files += files

    pdf_path = r'f:\BaiduSyncdisk\学习资源\pdf文件'

    if os.path.exists('record.txt'):
        with open('record.txt', 'r', encoding='utf-8') as record:
            book = record.readline().replace('\n','')
            file = book.split('\\')[-1]
            start_page = int(record.readline())
            pix = PDFToImage(book)
            pix.generateImage(start_page=start_page)
            des_pdf = f'{des_path}\{file}'
            des_txt = des_pdf.replace('.pdf', '.txt')
            source_txt = book.replace('.pdf', '.txt')
            shutil.move(source_txt,des_txt)
            shutil.move(book,des_pdf)


    for root,dir,files in os.walk(pdf_path):
        for file in files:
            book=f'{root}\{file}'

            print(book)

            pix = PDFToImage(book)
            pix.generateImage()
            des_pdf = f'{des_path}\{file}'
            des_txt = des_pdf.replace('.pdf','.txt')
            source_txt = book.replace('.pdf','.txt')
            shutil.move(source_txt, des_txt)
            shutil.move(book, des_pdf)













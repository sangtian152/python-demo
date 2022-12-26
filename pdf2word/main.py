#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/13 11:44
# @Author  : sangtian152
# @Software: PyCharm
import os

from pdf2docx import Converter
from tkinter import *
import tkinter.filedialog


class PDFWord:
    def __init__(self):
        print("进行初始化")
        self.root = Tk()
        self.input = StringVar()
        self.output = StringVar()
        self.filename = ''

    def run(self):
        self.input.set('请选择.pdf文件')
        self.root.title("pdf转word")
        self.root.geometry('400x200')
        frame = Frame(self.root)
        frame.grid(row=0, column=0, sticky='w')
        # 选择文件
        Label(frame, text='输入路径：').grid(row=0, column=0)
        lb = Label(frame, textvariable=self.input)
        lb.grid(row=0, column=1)
        Button(frame, text="选择", command=self.read_file).grid(row=0, column=2)
        # 转换后文件输出路径
        Label(frame, text='输出路径：').grid(row=1, column=0)
        lb = Label(frame, textvariable=self.output, height=2)
        lb.grid(row=1, column=1)
        dir_btn = Button(frame, text="浏览", command=self.choose_dir)
        dir_btn.grid(row=1, column=2)
        # 转换按钮
        Button(frame, text="转换", width=8, command=self.pdf2word).grid(row=2, column=1)
        self.root.mainloop()

    def choose_dir(self):
        my_dir = tkinter.filedialog.askdirectory()
        self.output.set(my_dir + '/' + self.filename)
        print(self.output)

    def read_file(self):
        filepath = tkinter.filedialog.askopenfilename()
        if filepath != '':
            # root.destroy()
            self.input.set(filepath)
            output_path = filepath.replace('.pdf', '.docx')
            self.output.set(output_path)
            self.filename = os.path.basename(output_path)
            # pdf_file(filename)
        else:
            print("您没有选择任何文件")

    def pdf2word(self):
        print('开始转换')
        self.pdf_file()

    def pdf_file(self):
        filepath = self.input.get()
        if filepath.endswith('.pdf'):
            # 对pdf文件进行格式转化
            cv = Converter(filepath)
            # 将PDF 文件保存为word文件
            cv.convert(self.output.get())
            cv.close()
            self.root.destroy()
            print("转化WORD成功")


if __name__ == "__main__":
    a = PDFWord()
    a.run()

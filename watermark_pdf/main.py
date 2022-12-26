#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/13 11:44
# @Author  : sangtian152
# @Software: PyCharm
import os

from tkinter import *
import tkinter.filedialog
# import tkMessageBox
import tkinter.messagebox as tkmsgbox
from PIL import Image
from os.path import splitext
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont

# SourceHanSansSC
registerFont(TTFont('SourceHanSansCN-Normal', 'SourceHanSansCN-Normal.ttf'))


class PDFWord:
    def __init__(self):
        print("进行初始化")
        self.root = Tk()
        # 文件输入路径
        self.input = StringVar(value='请选择pdf文件')
        # 排除的页
        self.exclude = StringVar()
        # 水印类型
        self.mark_type = StringVar(value='1')
        # 水印图片
        self.mark = StringVar(value='请选择水印图片')
        # 水印图片高度
        self.mark_height = StringVar(value='64')
        # 水印文字
        self.mark_text = StringVar()
        # 水印文字大小
        self.text_size = StringVar(value='30')
        # 水印间距
        self.spacing = StringVar(value='10')
        # 水印行距
        self.line_height = StringVar(value='5')
        # 透明度
        self.opacity = StringVar(value='0.1')
        # 旋转角度
        self.rotate = StringVar(value='30')
        # 文件输出路径
        self.output = StringVar()
        # 临时文件
        self.temp_name = "mark.pdf"
        # 临时文件夹
        self.temp_dir = ".pdf"

    def run(self):
        self.root.title("添加水印")
        self.root.geometry('400x360')
        frame = Frame(self.root)
        frame.grid(row=0, column=0, sticky='w')
        # 选择文件
        Label(frame, text='输入路径：').grid(row=0, column=0)
        Entry(frame, textvariable=self.input, width=20, state=DISABLED).grid(row=0, column=1)
        Button(frame, text="选择", command=self.read_file).grid(row=0, column=2)
        # 不添加水印的页码，多个逗号（,）分分隔
        Label(frame, text='排除页码：').grid(row=1, column=0)
        Entry(frame, width=20, bd=2, textvariable=self.exclude).grid(row=1, column=1)
        # 选择水印类型
        Label(frame, text='水印类型：').grid(row=2, column=0)
        inner_frame = Frame(frame)
        inner_frame.grid(row=2, column=1, sticky='w')
        Radiobutton(inner_frame, text='图片', value='1', variable=self.mark_type).grid(row=0, column=0)
        Radiobutton(inner_frame, text='文字', value='0', variable=self.mark_type).grid(row=0, column=1)
        # 选择水印文件
        Label(frame, text='水印路径：').grid(row=3, column=0)
        Entry(frame, textvariable=self.mark, width=20, state=DISABLED).grid(row=3, column=1)
        Button(frame, text="选择", command=self.read_mark).grid(row=3, column=2)
        # 水印高度
        Label(frame, text='水印高度：').grid(row=4, column=0)
        Entry(frame, width=20, bd=2, textvariable=self.mark_height).grid(row=4, column=1)
        Label(frame, justify=LEFT, text='单位pt', fg='#9c9c9c').grid(row=4, column=2)
        # 水印文字输入框
        Label(frame, text='水印文字：').grid(row=5, column=0)
        Entry(frame, width=20, bd=2, textvariable=self.mark_text).grid(row=5, column=1)
        # 水印文字大小
        Label(frame, text='文字大小：').grid(row=6, column=0)
        Entry(frame, width=20, bd=2, textvariable=self.text_size).grid(row=6, column=1)
        Label(frame, justify=LEFT, text='单位pt', fg='#9c9c9c').grid(row=6, column=2)
        # 水印间距
        Label(frame, justify=LEFT, text='横向间距：').grid(row=7, column=0)
        Entry(frame, textvariable=self.spacing, width=20, bd=2).grid(row=7, column=1)
        Label(frame, justify=LEFT, text='单位cm', fg='#9c9c9c').grid(row=7, column=2)
        # 水印行高
        Label(frame, justify=LEFT, text='纵向间距：').grid(row=8, column=0)
        Entry(frame, textvariable=self.line_height, width=20, bd=2).grid(row=8, column=1)
        Label(frame, justify=LEFT, text='单位cm', fg='#9c9c9c').grid(row=8, column=2)
        # 水印透明度
        Label(frame, justify=LEFT, text='透明度：').grid(row=9, column=0)
        Entry(frame, textvariable=self.opacity, width=20, bd=2).grid(row=9, column=1)
        # 水印旋转角度
        Label(frame, text='旋转角度：').grid(row=10, column=0)
        Entry(frame, textvariable=self.rotate, width=20, bd=2).grid(row=10, column=1)
        # 转换后文件输出路径
        Label(frame, text='输出路径：').grid(row=11, column=0)
        Entry(frame, textvariable=self.output, width=20, state=DISABLED).grid(row=11, column=1)
        Button(frame, text="浏览", command=self.choose_dir).grid(row=11, column=2)
        # 转换按钮
        Button(frame, text="添加水印", width=8, command=self.add_watermark).grid(row=12, column=1)
        self.root.mainloop()

    def choose_dir(self):
        my_dir = tkinter.filedialog.askdirectory()
        output_path = self.output.get()
        filename = os.path.basename(output_path)
        self.output.set(my_dir + '/' + filename)
        print(self.output)

    def read_file(self):
        filepath = tkinter.filedialog.askopenfilename()
        if filepath != '':
            self.input.set(filepath)
            output_path = '_带水印'.join(splitext(filepath))
            self.output.set(output_path)
        else:
            print("您没有选择任何文件")

    def read_mark(self):
        mark_path = tkinter.filedialog.askopenfilename()
        if mark_path == '':
            print("您没有选择任何文件")
        else:
            self.mark.set(mark_path)

    def create_watermark(self):
        """水印信息"""
        file_name = self.temp_dir + '/' + self.temp_name
        if os.path.exists(file_name):  # 若文件存在先删除
            os.remove(file_name)
        if os.path.exists(self.temp_dir):  # 临时文件，需为空
            os.removedirs(self.temp_dir)
        os.mkdir(self.temp_dir)
        # 默认大小为21cm*29.7cm
        c = canvas.Canvas(file_name, pagesize=(30 * cm, 30 * cm))
        # 移动坐标原点(坐标系左下为(0,0))
        c.translate(10 * cm, 5 * cm)
        options = {
            'rotate': float(self.rotate.get()),
            'opacity': float(self.opacity.get()),
            'spacing': float(self.spacing.get()),
            'line_height': float(self.line_height.get())
        }
        mark_type = self.mark_type.get()
        if mark_type == '0':
            self.draw_text(c, options)
        else:
            self.draw_image(c, options)

        # 关闭并保存pdf文件
        c.save()
        return file_name

    def draw_image(self, ctx, opt):
        img_path = self.mark.get()
        img = Image.open(img_path)
        mark_height = int(self.mark_height.get())
        mark_width = mark_height / img.height * img.width
        # 旋转45度,坐标系被旋转
        ctx.rotate(opt['rotate'])
        ctx.setFillAlpha(opt['opacity'])
        for i in range(5):
            for j in range(10):
                a = opt['spacing'] * (i - 1)
                b = opt['line_height'] * (j - 2)
                ctx.drawImage(img_path, a * cm, b * cm, width=mark_width, height=mark_height, mask='auto')

    def draw_text(self, ctx, opt):
        text = self.mark_text.get()
        size = self.text_size.get()
        # 设置字体
        ctx.setFont("SourceHanSansCN-Normal", int(size))
        # 指定描边的颜色
        ctx.setStrokeColorRGB(0, 1, 0)
        # 旋转45度,坐标系被旋转
        ctx.rotate(opt['rotate'])
        # 指定填充颜色
        ctx.setFillColorRGB(0, 0, 0, 0.1)
        # 设置透明度,1为不透明
        ctx.setFillAlpha(opt['opacity'])
        # 画几个文本,注意坐标系旋转的影响
        for i in range(5):
            for j in range(10):
                a = opt['spacing'] * (i - 1)
                b = opt['line_height'] * (j - 2)
                ctx.drawString(a * cm, b * cm, text)

    def is_exclude(self, page):
        exclude = self.exclude.get()
        exclude_pages = exclude.split(',')
        return exclude_pages.count(str(page)) > 0

    def validate(self):
        mark_type = self.mark_type.get()
        mark_text = self.mark_text.get()
        mark_path = self.mark.get()
        pdf_in = self.input.get()
        if pdf_in[-4:] != '.pdf':
            tkmsgbox.showinfo("提示", "请选择pdf文件")
            return False
        elif mark_type == '0' and mark_text == '':
            tkmsgbox.showinfo("提示", "请输入水印文字")
            return False
        elif mark_type == '1' and mark_path == '请选择水印图片':
            tkmsgbox.showinfo("提示", "请选择水印图片")
            return False
        return True

    def add_watermark(self):
        if not self.validate():
            return False
        pdf_in = self.input.get()
        writer = PdfFileWriter()
        pdf_src = PdfFileReader(pdf_in)
        file_path = self.create_watermark()
        # 打开水印文件
        mark_file = open(file_path, 'rb')
        pdf_watermark = PdfFileReader(mark_file, strict=False)
        for i in range(pdf_src.getNumPages()):
            if self.is_exclude(i):
                page = pdf_src.getPage(i)
            else:
                # 合并水印页和内容页，水印页在下，内容页在上
                page = pdf_src.getPage(i)
                page.mergePage(pdf_watermark.getPage(0))
            writer.addPage(page)
        # 生成结果文件
        with open(self.output.get(), 'wb') as fp:
            writer.write(fp)
        # 关闭水印文件
        mark_file.close()
        # 删除临时文件和文件夹
        os.remove(file_path)
        os.removedirs(self.temp_dir)
        tkmsgbox.showinfo("提示", "添加水印完成")
        # 销毁窗口
        self.root.destroy()
        print('添加水印完成')


if __name__ == "__main__":
    a = PDFWord()
    a.run()

import os
from tkinter import *
import tkinter.filedialog


def file_path_shortname_extension(file):
    # 返回文件拓展名.csv 等
    (filepath, temp_filename) = os.path.split(file)
    (shortname, extension) = os.path.splitext(temp_filename)
    return filepath, shortname, extension


def cv(file):
    if not os.path.isfile(file):
        print("文件不存在")
    else:
        a = file_path_shortname_extension(file)[2]
        print(a)
        if a == ".csv":
            print("此文件为csv文件")
            csv2vcf(file)
            print("已生成vcf文件")
        elif a == ".vcf":
            print("此文件为vcf文件")
            # vcf2csv(file)
            print("已生成csv文件")
        else:
            print("请选择正确的csv文件或者vsf文件")


def csv2vcf(file):
    rf = open(file, encoding="gbk", mode="r").read().split("\n")
    print(rf)
    name = file_path_shortname_extension(file)
    with open("output/" + name[1] + ".vcf", "w", encoding="utf-8") as wf:
        content = ["BEGIN:VCARD", "VERSION:3.0", "N", "FN", "TEL", "ORG", "END:VCARD\n\n", ]
        for line in rf:
            if line == "":
                break
            title = line.split(",")
            print(line)
            print(title[1])
            if title[0] == "name":
                continue
            if title[0] == "":
                break
            if title[1] == "":
                break
            if not title[0] == "":
                content[2] = "N;CHARSET=UTF-8:" + title[0]
                content[3] = "FN;CHARSET=UTF-8:" + title[0]
            if not title[1] == "":
                content[4] = "TEL;TYPE=CELL:" + title[1]
            if not title[1] == "":
                content[5] = "ORG:" + title[2]

            _str = "\n".join(content)
            wf.write(_str)
            content = ["BEGIN:VCARD", "VERSION:3.0", "N", "FN", "TEL", "ORG", "END:VCARD\n\n", ]
    print("写入完成")


root = Tk()


def read_file():
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
        root.destroy()
        cv(filename)
    else:
        print("您没有选择任何文件")


def choice_file():
    lb = Label(root, text='请选择.csv文件')
    lb.pack()
    btn = Button(root, text="选择文件", command=read_file)
    btn.pack()
    root.mainloop()


if __name__ == "__main__":
    choice_file()

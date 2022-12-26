import os
import shutil
import time

from tkinter import *
import tkinter.filedialog
# import tkMessageBox
import tkinter.messagebox as tkmsgbox
from tkinter import colorchooser, filedialog

from removebg import RemoveBg
from PIL import Image, ImageTk
from os.path import splitext


class RPBgColor:
    def __init__(self):
        self.root = Tk()
        # 初始化RemoveBg，key=q8GM8b6YaLyFL1M7cPwUG5kE
        self.rm_bg = RemoveBg("q8GM8b6YaLyFL1M7cPwUG5kE", "error.log")
        # 文件输入路径
        self.input_path = StringVar()
        # 临时文件夹
        self.temp_dir = ".temp"
        # 输入图片显示框
        self.input_label = None
        # 输出图片显示框
        self.output_label = None
        # 输入图片预览
        self.input_photo = None
        # 输出图片预览
        self.output_photo = None
        # 生成文件
        self.output_file = None

    def run(self):
        self.root.title("")
        self.root.geometry('400x360')
        frame = Frame(self.root)
        frame.grid(row=0, column=0, sticky='w')
        # 菜单
        menubar = self.init_menu()
        self.root.config(menu=menubar)
        # 预览
        Label(frame, text='替换前', width=20).grid(row=0, column=0)
        Label(frame, text='替换后', width=20).grid(row=0, column=1)
        self.input_label = Label(frame)
        self.input_label.grid(row=1, column=0)
        self.output_label = Label(frame)
        self.output_label.grid(row=1, column=1)

        self.root.mainloop()

    def init_menu(self):
        menubar = Menu(self.root)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="打开", command=self.read_file)
        file_menu.add_command(label="保存", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)
        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="背景色", command=self.choose_color)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        return menubar

    def resize_img(self, img_path):
        # 以一个PIL图像对象打开
        pil_image = Image.open(img_path)
        # 获取图像的原始大小
        w, h = pil_image.size
        # 缩放图像让它保持比例，同时限制在一个矩形框范围内
        pil_image_resized = self.resize(w, h, 200, 200, pil_image)
        photo = ImageTk.PhotoImage(pil_image_resized)
        return photo

    def resize(self, w, h, w_box, h_box, pil_image):
        # resize a pil_image object so it will fit into
        # a box of size w_box times h_box, but retain aspect ratio
        # 对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
        f1 = 1.0 * w_box / w  # 1.0 forces float division in Python2
        f2 = 1.0 * h_box / h
        factor = min([f1, f2])
        # use best down-sizing filter
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), Image.Resampling.LANCZOS)

    def choose_color(self):
        def_color = (0, 125, 255)
        new_color = colorchooser.askcolor(color=def_color, title="背景色")
        # print(new_color)
        if new_color[0]:
            f_color = self.format_color(new_color[0])
            self.set_bg_color(f_color)

    def format_color(self, thetuple):
        new_tuple = []
        for item in thetuple:
            new_tuple.append(int(item))
        return tuple(new_tuple)

    def save_as_file(self):
        filepath = self.input_path.get()
        output_path = '_替换背景'.join(splitext(filepath))
        filename = os.path.basename(output_path)
        extension = '.png'
        save_name = filename[:-4] + extension
        journal_name = filedialog.asksaveasfilename(initialfile=save_name, defaultextension=extension, filetypes=[("图像", extension), ("All files", ".*")])
        self.save_file(journal_name)

    def read_file(self):
        filepath = tkinter.filedialog.askopenfilename()
        if filepath != '':
            self.input_path.set(filepath)
            self.input_photo = self.resize_img(filepath)
            self.input_label.configure(image=self.input_photo)
        else:
            print("您没有选择任何文件")

    def validate(self):
        file_in = self.input_path.get()
        suffix = file_in[-4:]
        if suffix != '.jpg' and suffix != '.png':
            tkmsgbox.showinfo("提示", "请选择jpg或png图片")
            return False
        return True

    def set_bg_color(self, color):
        if not self.validate():
            return False
        # 输入你想要扣图的图片路径
        file_in = self.input_path.get()
        # 换背景色
        p, s = file_in.split(".")
        self.rm_bg.remove_background_from_img_file(file_in)
        file_no_bg = "{}.{}_no_bg.{}".format(p, s, 'png')
        no_bg_image = Image.open(file_no_bg)
        x, y = no_bg_image.size
        self.output_file = Image.new('RGBA', no_bg_image.size, color=color)
        self.output_file.paste(no_bg_image, (0, 0, x, y), no_bg_image)
        no_bg_image.close()
        os.remove(file_no_bg)
        self.preview_file()

    def preview_file(self):
        if os.path.exists(self.temp_dir):  # 临时文件，需为空
            shutil.rmtree(self.temp_dir)
        os.mkdir(self.temp_dir)
        temp_name = str(time.time()) + '.png'
        file_name = self.temp_dir + '/' + temp_name
        self.output_file.save(file_name)
        self.output_photo = self.resize_img(file_name)
        self.output_label.configure(image=self.output_photo)

    def save_file(self, output_path):
        if output_path:
            path = output_path
        else:
            filepath = self.input_path.get()
            path = '_替换背景'.join(splitext(filepath))
        self.output_file.save(path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = RPBgColor()
    a.run()
    # cutout()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

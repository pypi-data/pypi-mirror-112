# -*- coding: utf-8 -*-
"""
根据word转换excel
"""
import cmd
import os
import sys
import time

from win32com.client import Dispatch


class Order(cmd.Cmd):
    intro = "Word转Pdf系统v1.0，输入 help 或者?查看帮助。\n"
    prompt = "command>"

    def do_run(self, arg):
        """转换开始"""
        self.main()

    def check_directory(self, path):
        if path:
            if os.path.isdir(path):
                return path
            else:
                raise Exception(f"同级目录下不存在文件夹")
        else:
            if os.path.isdir("dir"):
                return "dir"
            else:
                raise Exception("同级目录下不存在dir文件夹")

    def main(self, dir_path: str="", out_path: str=""):
        try:
            dir_path = self.check_directory(dir_path)
            f = WordToPdf(dir_path, out_path)
            f.run()
        except Exception as e:
            print(e)

    def do_exit(self, _):
        '退出'
        exit(0)

class WordToPdf(object):
    wd_format_pdf = 17

    def __init__(self, dir_path, out_path=""):
        self.dir_path = f"{os.getcwd()}{os.path.sep}{dir_path}"
        self.out_path = out_path if out_path else ""
        self.false_list = []

    def doc2pdf(self, input_file, type):
        try:
            word = Dispatch("Word.Application")
            doc = word.Documents.Open(input_file)
            if not os.path.exists(f"{self.dir_path}_pdf"):
                os.mkdir(f"{self.dir_path}_pdf")
            out_file = input_file.replace(self.dir_path, f"{self.dir_path}_pdf")
            doc.SaveAs(out_file.replace(type, ".pdf"), FileFormat=self.wd_format_pdf)
            doc.Close()
            word.Quit()
            time.sleep(1.2)
        except Exception as e:
            print(e)
            self.false_list.append(input_file)
        else:
            print(f"执行成功:{input_file}")

    def run(self):
        sys.stdout.write(f"{WordToPdf.__name__} start:{int(time.time())}\n")
        for root, dirs, filenames in os.walk(self.dir_path):
            for file in filenames:
                suffix = os.path.splitext(file)[-1]
                if suffix in [".doc", ".docx"]:
                    self.doc2pdf(f"{root}{os.path.sep}{file}", suffix)
                else:
                    raise Exception("word格式错误!")
        print(f"失败文件列表:{self.false_list}")
        sys.stdout.write(f"{WordToPdf.__name__} stop:{int(time.time())}\n")

if __name__ == "__main__":
    Order().cmdloop()

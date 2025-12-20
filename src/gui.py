import ttkbootstrap as tk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.scrolled import ScrolledText, ScrolledFrame
from ttkbootstrap.utility import enable_high_dpi_awareness
from pdf2image import convert_from_path
from socketserver import BaseRequestHandler, ThreadingUDPServer
# from PIL import ImageTk, Image


problem_set: list[str] = ["A", "B", "C"]
status_bar: list[str] = ["#", "Submitter", "Problem", "Result"]
ranking_bar: list[str] = ["#", "Name", "A", "B", "C", "Sigma"]

converted: dict = {index: False for index in problem_set}
problem_array: dict = {}

photos: dict = {index: [] for index in problem_set}

PDF_PATH = ".\\contest\\example\\problems\\"
IMAGE_SAVE_PATH = ".\\contest\\example\\problems\\cache\\"

ENCODING = "utf-8"

'''
Valid queries

get_rank

'''


# class HolderUDPHandler(BaseRequestHandler):
#     def handle(self):
#         data: list = self.request[0].strip().split(" ")
#         client = self.request[1]

#         client.sendto(bytes(data, ENCODING), self.client_address)

# ThreadingUDPServer((HOST, PORT), UDPHandler)


class GuestUDPHandler:
    pass


def get_pdf_path(index: str = 'A') -> str:
    return PDF_PATH + index + '.pdf'


class Application:
    def __init__(self, master):
        self.window = master

    @staticmethod
    def kill_all(master) -> None:
        for index in master.winfo_children():
            if index.winfo_class() != "Menu":
                index.destroy()

    def reset_loading_page(self, master) -> None:
        self.kill_all(master)
        tk.Label(master, text="LOADING ...", font=("Fira Code Semibold", 30)).pack()

    def show_problem_by_index(self, index: str = "-1") -> None:
        self.kill_all(self.problem_child_frame)
        global converted
        if not converted[index]:
            converted[index] = True
            images = convert_from_path(get_pdf_path(index), dpi=200)
            for dex, image in enumerate(images):
                image.save(f"{IMAGE_SAVE_PATH}{index}{dex + 1}.png", dpi=[200, 200])
                photos[index].append(tk.PhotoImage(file=f"{IMAGE_SAVE_PATH}{index}{dex + 1}.png"))

        tk.Button(self.problem_child_frame, text="         返回         ", bootstyle=SECONDARY,
                  command=lambda: self.show_problems(self.problem_child_frame)).pack()
        for photo in photos[index]:
            tk.Label(self.problem_child_frame, image=photo).pack(pady=10)

    def show_problems(self, master):
        self.kill_all(self.problem_child_frame)
        tk.Label(self.problem_child_frame, text="浙江省温州市第114514届毒瘤程序设计竞赛", font=("Fira Code Bold", 31)).pack(pady=5)
        for index in problem_set:
            frame = tk.Frame(master=master, borderwidth=2, relief=GROOVE, )
            dex = tk.Label(frame, text="问题: " + index, font=("Fira Code", 12))
            dex.pack(side=TOP)
            tk.Button(frame, text="查看 纯文本", state=DISABLED).pack(fill=X)
            tk.Button(frame, text="查看 PDF 文档", bootstyle=SUCCESS,
                      command=lambda idx=dex.cget("text")[4]: self.show_problem_by_index(idx)).pack(fill=X)
            frame.pack(fill=X, padx=10, pady=10)
    # ll get_the_value_about_the_binary_tree();

    def login_page_setup(self):
        self.kill_all(self.window)

        tk.Label(self.window, text="邀请码:").grid(row=0, column=0, padx=10, pady=10)
        self.register_address_entry = tk.Entry(self.window, width=50)
        self.register_address_entry.grid(row=0, column=1, padx=10, pady=10)
        self.register_username_entry = tk.Entry(self.window, width=50)
        self.register_username_entry.grid(row=0, column=1, padx=10, pady=10)
        (tk.Button(self.window, text="加入", bootstyle=(PRIMARY, "outline-toolbutton"))
         .grid(row=2, column=0, padx=10, pady=10))

    def contest_main_page_setup(self):
        self.kill_all(self.window)

        main_frame = tk.Notebook(self.window)
        main_frame.pack(padx=5, fill=BOTH, expand=True)

        submit_frame = tk.Frame(main_frame)
        status_frame = tk.Frame(main_frame)
        ranking_frame = tk.Frame(main_frame)
        problem_frame = tk.Frame(main_frame)

        self.problem_child_frame = ScrolledFrame(problem_frame, autohide=True)
        self.problem_child_frame.pack(fill=BOTH, expand=True)

        self.show_problems(self.problem_child_frame)

        self.submit_combobox = tk.Combobox(submit_frame, bootstyle=LIGHT,
                                           font=("Fira Code", 12), state="readonly", values=problem_set)
        self.submit_combobox.pack(pady=5, fill=X)
        self.submit_scrolledtext = ScrolledText(submit_frame, font=("Fira Code", 7), autohide=True)
        self.submit_scrolledtext.pack(fill=BOTH, expand=True)
        tk.Button(submit_frame, bootstyle=(PRIMARY, "outline-toolbutton"), text="提交").pack(fill=X)
        self.status_tabelview = Tableview(status_frame, coldata=status_bar)
        self.status_tabelview.pack(fill=BOTH, expand=True)
        self.ranking_tabelview = Tableview(ranking_frame, coldata=ranking_bar, pagesize=4)
        self.ranking_tabelview.pack(fill=BOTH, expand=True)

        main_frame.pack(fill=BOTH)
        main_frame.add(problem_frame, text="问题集")
        main_frame.add(submit_frame, text="提交")
        main_frame.add(status_frame, text="状态")
        main_frame.add(ranking_frame, text="排名")

    def setup(self):
        menu = tk.Menu(self.window)
        contest_menu = tk.Menu(menu, tearoff=False)
        contest_menu.add_command(label="加入比赛", underline=0, command=self.contest_main_page_setup)
        contest_menu.add_command(label="创建比赛", underline=0, command=self.login_page_setup)
        contest_menu.add_command(label="回顾比赛", underline=0)
        menu.add_cascade(menu=contest_menu, label="比赛")
        self.window.config(menu=menu)


if __name__ == '__main__':
    root = tk.Window()

    tk.Style().theme_use("darkly")

    app = Application(root)
    app.setup()

    enable_high_dpi_awareness()

    root.mainloop()

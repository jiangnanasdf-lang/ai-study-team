"""AI学习队 小工具（Win11 64 位）

一个非常简单的桌面小软件，包含两块功能：
1. 招新入口：打开报名问卷 / 咨询QQ群 / 发送邮件
2. 数学小测验：随机出 5 道口算题，练练基本功

运行方式：
    python ai_study_tool.py          # 启动图形界面
    python ai_study_tool.py --selftest  # 无界面自检（用于验证打包后的 exe）
"""

import random
import sys
import tkinter as tk
import webbrowser
from tkinter import messagebox

# ---------------- 可修改的配置 ----------------
SURVEY_URL = "https://wj.qq.com/s2/23398546/ad18"      # 报名问卷链接
QQ_GROUP_URL = "https://qm.qq.com/q/XXXXXX"            # QQ 群加群链接（占位）
CONTACT_EMAIL = "1984705083@qq.com"                    # 联系邮箱
QUIZ_TOTAL = 5                                         # 测验题数
# ------------------------------------------------


def make_question():
    """随机生成一道口算题，返回 (题目文本, 正确答案)。"""
    op = random.choice(["+", "-", "×"])
    if op == "×":
        a, b = random.randint(2, 9), random.randint(2, 9)
        answer = a * b
    elif op == "+":
        a, b = random.randint(10, 99), random.randint(10, 99)
        answer = a + b
    else:  # "-"：保证结果不小于 0
        a = random.randint(20, 99)
        b = random.randint(1, a)
        answer = a - b
    return f"{a} {op} {b} = ?", answer


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI学习队 · 小工具")
        self.geometry("420x520")
        self.resizable(False, False)
        self.configure(bg="#0a0e17")

        # 顶部标题
        tk.Label(self, text="AI学习队", font=("Microsoft YaHei UI", 22, "bold"),
                 fg="#00e0ff", bg="#0a0e17").pack(pady=(24, 4))
        tk.Label(self, text="Model the World, Code the Future",
                 font=("Consolas", 10), fg="#9aa9bb", bg="#0a0e17").pack()

        # ============ 招新入口 ============
        self._section_label("招新入口")
        tk.Label(self, text="招生计划：40~50人/届，点击下方按钮报名或咨询",
                 font=("Microsoft YaHei UI", 10), fg="#9aa9bb",
                 bg="#0a0e17").pack(pady=(0, 8))
        self._button("📄 报名意向表", self.open_survey).pack(pady=3)
        self._button("💬 咨询QQ群 1076502298", self.open_qq).pack(pady=3)
        self._button("✉️ 发送邮件", self.send_mail).pack(pady=3)

        # ============ 数学小测验 ============
        self._section_label("数学小测验")
        self.question_var = tk.StringVar()
        self.feedback_var = tk.StringVar()
        self.score_var = tk.StringVar()
        self.index = 0
        self.score = 0
        self.answer = None

        tk.Label(self, textvariable=self.question_var,
                 font=("Microsoft YaHei UI", 16, "bold"),
                 fg="#e6ecf3", bg="#0a0e17").pack(pady=(6, 4))
        self.entry = tk.Entry(self, font=("Microsoft YaHei UI", 12),
                              justify="center", width=12)
        self.entry.pack(pady=4)
        self.entry.bind("<Return>", lambda _e: self.submit())
        self._button("提交答案", self.submit).pack(pady=6)
        tk.Label(self, textvariable=self.feedback_var,
                 font=("Microsoft YaHei UI", 10), fg="#ffd166",
                 bg="#0a0e17").pack()
        tk.Label(self, textvariable=self.score_var,
                 font=("Microsoft YaHei UI", 10), fg="#9aa9bb",
                 bg="#0a0e17").pack(pady=(4, 0))

        self.next_question()

    # ---------- UI 辅助 ----------
    def _section_label(self, text):
        tk.Label(self, text=text, font=("Microsoft YaHei UI", 12, "bold"),
                 fg="#00b4d8", bg="#0a0e17").pack(pady=(18, 6))

    def _button(self, text, command):
        return tk.Button(self, text=text, command=command, cursor="hand2",
                         font=("Microsoft YaHei UI", 10),
                         bg="#111622", fg="#e6ecf3",
                         activebackground="#171d2b", activeforeground="#00e0ff",
                         relief="flat", bd=0, padx=18, pady=8,
                         highlightthickness=1, highlightbackground="#2a3446")

    # ---------- 招新按钮 ----------
    def open_survey(self):
        webbrowser.open(SURVEY_URL)

    def open_qq(self):
        webbrowser.open(QQ_GROUP_URL)

    def send_mail(self):
        webbrowser.open(f"mailto:{CONTACT_EMAIL}")

    # ---------- 小测验 ----------
    def next_question(self):
        if self.index >= QUIZ_TOTAL:
            messagebox.showinfo("测验结束", f"得分：{self.score} / {QUIZ_TOTAL}")
            self.index = 0
            self.score = 0
        text, self.answer = make_question()
        self.question_var.set(f"第 {self.index + 1} 题：{text}")
        self.feedback_var.set("")
        self.score_var.set(f"已答 {self.index} 题 · 得分 {self.score}")
        self.entry.delete(0, "end")
        self.entry.focus_set()

    def submit(self):
        try:
            user = int(self.entry.get().strip())
        except ValueError:
            self.feedback_var.set("请输入数字哦")
            return
        if user == self.answer:
            self.score += 1
            self.feedback_var.set("✅ 正确！")
        else:
            self.feedback_var.set(f"❌ 正确答案是 {self.answer}")
        self.index += 1
        self.after(700, self.next_question)


def selftest():
    """无界面自检：验证出题逻辑，打包后可用它确认 exe 正常。"""
    for _ in range(200):
        text, answer = make_question()
        a, rest = text.split(" ", 1)
        op, b = rest.replace("= ?", "").strip().split(" ")
        a, b = int(a), int(b)
        expected = {"+": a + b, "-": a - b, "×": a * b}[op]
        assert answer == expected, f"BUG: {text} -> {answer} != {expected}"
    print("selftest OK")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    App().mainloop()

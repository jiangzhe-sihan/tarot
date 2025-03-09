import tkinter as tk
from tkinter.messagebox import showinfo
from tarot import CardStack, parse_stack

import threading
import datetime


class MainScene(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._fm_enter = tk.Frame(self)
        self._fm_enter.pack(pady=5)
        self._fm_hint = tk.Frame(self._fm_enter)
        self._fm_hint.pack()
        self._lb_entry_hint = tk.Label(self._fm_hint, text='分析一下，你就知道', font=('黑体', 14))
        self._lb_entry_hint.pack(pady=10)
        self._fm_entry = tk.Frame(self._fm_enter)
        self._fm_entry.pack(padx=5)
        self._et_stock = tk.Entry(self._fm_entry, width=30, font=('', 15))
        self._et_stock.pack(side=tk.LEFT, padx=5, ipady=3)
        self._bt_confirm = tk.Button(self._fm_entry, text='分析', command=self._submit)
        self._bt_confirm.pack(side=tk.LEFT)
        self._fm_result = tk.Frame(self)
        self._fm_result.pack()
        self._lfm_buy_analyse = tk.LabelFrame(self._fm_result, text='是或否？', padx=5)
        self._lfm_buy_analyse.pack(side=tk.LEFT)
        self._txt_buy_result = tk.StringVar(self._lfm_buy_analyse, '准备就绪')
        self._lb_buy_result = tk.Label(self._lfm_buy_analyse, textvariable=self._txt_buy_result, width=8)
        self._lb_buy_result.config(font=('', 20), bg='lightgray')
        self._lb_buy_result.pack(padx=5, ipady=2, pady=5)
        self.bind('<Destroy>', self._destroy_me)
        self._running = tk.BooleanVar(self, False)
        self._running1 = False
        self._updating_func = None
        self._running_thread = None

    def _submit(self):
        if self._running1:
            showinfo('提示', '请先等待分析完成。', parent=self.winfo_toplevel())
            return
        code = self._et_stock.get()
        if code.strip() == '':
            showinfo('提示', '请输入你的问题', parent=self.winfo_toplevel())
            return
        self._running.set(True)
        self._running1 = True
        self._lb_buy_result.config(bg='lightgray', fg='black')
        self._txt_buy_result.set('分析中..')
        cs = CardStack()
        td_analyse_buy = ThreadAnalyse(cs, code)
        self._running_thread = td_analyse_buy
        td_analyse_buy.daemon = True
        td_analyse_buy.start()
        self._wait_thread(td_analyse_buy)
        self.wait_variable(self._running)
        rank_buy = td_analyse_buy.res
        if rank_buy:
            self._lb_buy_result.config(bg='green', fg='white')
            self._txt_buy_result.set('是')
        else:
            self._lb_buy_result.config(bg='red')
            self._txt_buy_result.set('否')
        self._running1 = False

    def _wait_thread(self, td: threading.Thread):
        if not td.is_alive():
            self._running.set(False)
            return
        self.update()
        self._updating_func = self.after(50, self._wait_thread, td)

    def _destroy_me(self, event):
        self._running.set(False)
        self._running_thread.stop() if self._running_thread is not None else None
        self.after_cancel(self._updating_func) if self._updating_func is not None else None


class ThreadAnalyse(threading.Thread):
    def __init__(self, cs: CardStack, question: str):
        super().__init__()
        self.cs = cs
        self.question = question
        self.res = None
        self._weekday_ref = ('一', '二', '三', '四', '五', '六', '天')

    def run(self) -> None:
        dow = datetime.date.today().weekday()
        temp = None
        q1 = f'今天是不是星期{self._weekday_ref[dow]}？'
        while True:
            stack = self.cs.answer(q1, 3)
            if temp is None:
                temp = parse_stack(stack)
                continue
            if parse_stack(stack) == temp:
                break
        reverse = not temp
        res = parse_stack(self.cs.answer(self.question, 3))
        self.res = res if not reverse else not res

    def stop(self):
        self.cs.stop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('赛博塔罗牌 - 问是非')
    scene = MainScene(root)
    scene.pack()
    root.mainloop()

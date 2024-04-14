import tkinter as tk
from tkinter.messagebox import showinfo

from tarot import CardStack
from up_stock import answer_me, is_possible

import threading


class MainScene(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._fm_enter = tk.Frame(self)
        self._fm_enter.pack(pady=5)
        self._lb_entry_hint = tk.Label(self._fm_enter, text='股票名称或代码：')
        self._lb_entry_hint.pack(side=tk.LEFT)
        self._et_stock = tk.Entry(self._fm_enter)
        self._et_stock.pack(side=tk.LEFT)
        self._bt_confirm = tk.Button(self._fm_enter, text='分析', command=self._submit)
        self._bt_confirm.pack(side=tk.LEFT)
        self._fm_result = tk.Frame(self)
        self._fm_result.pack()
        self._lfm_buy_analyse = tk.LabelFrame(self._fm_result, text='是否买入？', padx=5)
        self._lfm_buy_analyse.pack(side=tk.LEFT)
        self._txt_buy_result = tk.StringVar(self._lfm_buy_analyse, '准备就绪')
        self._lb_buy_result = tk.Label(self._lfm_buy_analyse, textvariable=self._txt_buy_result)
        self._lb_buy_result.config(font=('', 20), bg='lightgray')
        self._lb_buy_result.pack(padx=5, ipady=2, pady=5)
        self._lfm_sell_analyse = tk.LabelFrame(self._fm_result, text='是否卖出？', padx=5)
        self._lfm_sell_analyse.pack(side=tk.LEFT)
        self._txt_sell_result = tk.StringVar(self._lfm_sell_analyse, '准备就绪')
        self._lb_sell_result = tk.Label(self._lfm_sell_analyse, textvariable=self._txt_sell_result)
        self._lb_sell_result.config(font=('', 20), bg='lightgray')
        self._lb_sell_result.pack(padx=5, ipady=2, pady=5)
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
            showinfo('提示', '请输入股票/代码', parent=self.winfo_toplevel())
            return
        self._running.set(True)
        self._running1 = True
        self._lb_buy_result.config(bg='lightgray', fg='black')
        self._lb_sell_result.config(bg='lightgray', fg='black')
        self._txt_buy_result.set('分析中..')
        self._txt_sell_result.set('分析中..')
        cs = CardStack()
        td_analyse_buy = ThreadAnalyse(cs, code)
        self._running_thread = td_analyse_buy
        td_analyse_buy.daemon = True
        td_analyse_buy.start()
        self._wait_thread(td_analyse_buy)
        self.wait_variable(self._running)
        rank_buy = td_analyse_buy.res
        match rank_buy:
            case 1:
                self._lb_buy_result.config(bg='green', fg='white')
                self._txt_buy_result.set('不必买入')
            case 2:
                self._lb_buy_result.config(bg='lightgray')
                self._txt_buy_result.set('　中性　')
            case 3:
                self._lb_buy_result.config(bg='lightpink')
                self._txt_buy_result.set('　买入　')
            case 4:
                self._lb_buy_result.config(bg='red')
                self._txt_buy_result.set('强力买入')
        self._running.set(True)
        td_analyse_sell = ThreadAnalyse(cs, code, buy=False)
        self._running_thread = td_analyse_sell
        td_analyse_sell.daemon = True
        td_analyse_sell.start()
        self._wait_thread(td_analyse_sell)
        self.wait_variable(self._running)
        rank_sell = td_analyse_sell.res
        match rank_sell:
            case 1:
                self._lb_sell_result.config(bg='green', fg='white')
                self._txt_sell_result.set('不必卖出')
            case 2:
                self._lb_sell_result.config(bg='lightgray')
                self._txt_sell_result.set('　中性　')
            case 3:
                self._lb_sell_result.config(bg='lightpink')
                self._txt_sell_result.set('　卖出　')
            case 4:
                self._lb_sell_result.config(bg='red')
                self._txt_sell_result.set('强力卖出')
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


def rank(self: bool, other: bool) -> int:
    if self and other:
        return 4
    if not self and other:
        return 3
    if not (self or other):
        return 2
    if self and not other:
        return 1


class ThreadAnalyse(threading.Thread):
    def __init__(self, cs: CardStack, code: str, buy=True):
        super().__init__()
        self.cs = cs
        self.code = code
        self.buy = buy
        self.res = None

    def run(self) -> None:
        if self.buy:
            self_buy = is_possible(answer_me(self.cs, f'要不要买入{self.code}？', forself=True), False)
            other_buy = is_possible(answer_me(self.cs, f'要不要买入{self.code}？', forself=False), False)
        else:
            self_buy = is_possible(answer_me(self.cs, f'要不要卖出{self.code}？', forself=True), False)
            other_buy = is_possible(answer_me(self.cs, f'要不要卖出{self.code}？', forself=False), False)
        self.res = rank(self_buy, other_buy)

    def stop(self):
        self.cs.stop()


if __name__ == '__main__':
    root = tk.Tk()
    scene = MainScene(root)
    scene.pack()
    root.mainloop()

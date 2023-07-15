import tkinter as tk
from tkinter.messagebox import Message
from datetime import datetime
import matplotlib as mat
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import math

mat.rcParams['font.family'] = 'Hancom Gothic' # 한글 폰트
mat.rcParams['axes.unicode_minus'] = False

def birth2date():
    try:
        return int(entry_byear.get()) * 365 + int(entry_bmonth.get()) * 30 + int(entry_bdate.get())
    except:
        Message(parent=None, title="출생일 오류", message="정수값을 입력해주세요.").show()

def check2date():
    try:
        return int(entry_checkyear.get()) * 365 + int(entry_checkmonth.get()) * 30 + int(entry_checkdate.get())
    except:
        Message(parent=None, title="확인일 오류", message="정수값을 입력해주세요.").show()

def date2today():
    entry_checkyear.delete(0, "end")
    entry_checkmonth.delete(0, "end")
    entry_checkdate.delete(0, "end")
    entry_checkyear.insert(0, datetime.now().year)
    entry_checkmonth.insert(0, datetime.now().month)
    entry_checkdate.insert(0, datetime.now().day)

def date2exam():
    entry_checkyear.delete(0, "end")
    entry_checkmonth.delete(0, "end")
    entry_checkdate.delete(0, "end")
    entry_checkyear.insert(0, datetime.now().year)
    entry_checkmonth.insert(0, 11)
    entry_checkdate.insert(0, 16)


# 그래프 그리기
def plot_graph():
    diff = abs(birth2date() - check2date()) + 7

    x_max, x_min = diff + 15, diff - 15
    x = np.linspace(x_min, x_max, int((x_max - x_min) * 20))
    # y_formula = entry_y.get()
    # y = eval(y_formula)
    y1_formula = "100 * np.sin(2 * math.pi * x / 23)"
    y2_formula = "100 * np.sin(2 * math.pi * x / 28)"
    y3_formula = "100 * np.sin(2 * math.pi * x / 33)"
    y1, y2, y3 = eval(y1_formula), eval(y2_formula), eval(y3_formula)
    y1_min, y1_max = min(y1), max(y1)

    fig = Figure(figsize=(10, 5), dpi=100)
    ax = fig.add_subplot(111)
    fig.suptitle("BioRhythm", fontsize=20)
    ax.plot(x, y1, 'b', label='신체 지수')
    ax.plot(x, y2, 'g', label='감성 지수')
    ax.plot(x, y3, 'r', label='지성 지수')
    ax.set_xlabel('날짜 (측정 날짜를 기준으로 일수 차이)')
    ax.set_ylabel('지수')

    x_value = diff

    y1_value = eval(y1_formula.replace("x", str(x_value)))
    y2_value = eval(y2_formula.replace("x", str(x_value)))
    y3_value = eval(y3_formula.replace("x", str(x_value)))

    ax.plot(x_value, y1_value, 'ro')
    ax.annotate(f'(0, {y1_value:.1f})', xy=(x_value, y1_value),
                xytext=(x_value + 0.2, y1_value + 0.2), fontsize=10)

    ax.plot(x_value, y2_value, 'ro')
    ax.annotate(f'(0, {y2_value:.1f})', xy=(x_value, y2_value),
                xytext=(x_value + 0.2, y2_value + 0.2), fontsize=10)

    ax.plot(x_value, y3_value, 'ro')
    ax.annotate(f'(0, {y3_value:.1f})', xy=(x_value, y3_value),
                xytext=(x_value + 0.2, y3_value + 0.2), fontsize=10)

    # 상태 판단 함수
    def current_status(val, upper_lim, lower_lim):
        if val < lower_lim:
            return '저조 ▼'
        elif lower_lim <= val <= upper_lim:
            return '불안정 ↯'
        else:
            return '고조 ▲'

    # 라벨 업데이트
    body_label.config(text=f'신체 지수: {round(y1_value, 1)} ({current_status(y1_value, 25, -25)})')
    feeling_label.config(text=f'감성 지수: {round(y2_value, 1)} ({current_status(y2_value, 25, -25)})')
    intel_label.config(text=f'지성 지수: {round(y3_value, 1)} ({current_status(y3_value, 25, -25)})')

    real_xval_num = np.linspace(x_min, x_max, num=31) # x축 실제 값
    display_x_value = np.linspace(-15, 15, num=31) # x축 표기용
    display_x_value_r = [] # 소수점 제거 리스트
    for i in display_x_value:
        display_x_value_r.append(round(i))
    ax.set_xticks(real_xval_num)
    ax.set_xticklabels(display_x_value_r)
    ax.tick_params(axis='x',
                   labelsize=10,
                   length=5,
                   width=1,
                   rotation=30)

    ax.hlines(y1_value, x_min, x_max, color='grey', linestyle='--', linewidth=1)
    ax.hlines(y2_value, x_min, x_max, color='grey', linestyle='--', linewidth=1)
    ax.hlines(y3_value, x_min, x_max, color='grey', linestyle='--', linewidth=1)

    ax.vlines(x_value, y1_min, y1_max, color='grey', linestyle='--', linewidth=1)

    ax.legend(loc='upper right') # 오른쪽 위 범례 표시


    formula_label.config(text=f"y1 = 100×𝒔𝒊𝒏(2π𝒳/23),         y2 = 100×𝒔𝒊𝒏(2π𝒳/28),          y3 = 100×𝒔𝒊𝒏(2π𝒳/33)")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=10, y=100)


# UI 만들기
window = tk.Tk()
window.title("바이오 리듬 계산기")
window.geometry("1000x650")

# 입력 필드 추가
entry_byear = tk.Entry(window)
entry_byear.insert(0, "출생년도(4자리)")
entry_byear.place(x=10, y=10)

entry_bmonth = tk.Entry(window)
entry_bmonth.insert(0, "출생달(1자리 혹은 2자리)")
entry_bmonth.place(x=160, y=10)

entry_bdate = tk.Entry(window)
entry_bdate.insert(0, "출생일(1자리 혹은 2자리)")
entry_bdate.place(x=310, y=10)

entry_checkyear = tk.Entry(window)
entry_checkyear.insert(0, "측정할 년도(4자리)")
entry_checkyear.place(x=10, y=40)

entry_checkmonth = tk.Entry(window)
entry_checkmonth.insert(0, "측정할 달(1자리 혹은 2자리)")
entry_checkmonth.place(x=160, y=40)

entry_checkdate = tk.Entry(window)
entry_checkdate.insert(0, "측정할 일(1자리 혹은 2자리)")
entry_checkdate.place(x=310, y=40)

# 버튼 추가
plot_button = tk.Button(window, text="그래프 그리기", command=plot_graph)
plot_button.place(x=460, y=10)

today_button = tk.Button(window, text="오늘 날짜로", command=date2today)
today_button.place(x=460, y=40)

exam_button = tk.Button(window, text="수능 날짜로", command=date2exam)
exam_button.place(x=550, y=40)


#라벨
body_label = tk.Label(window, text="신체 지수:", foreground='blue', font=('Hancom Gothic', 15))
body_label.place(x=700, y=10)

feeling_label = tk.Label(window, text="감성 지수:", foreground='green', font=('Hancom Gothic', 15))
feeling_label.place(x=700, y=40)

intel_label = tk.Label(window, text="지성 지수:", foreground='red', font=('Hancom Gothic', 15))
intel_label.place(x=700, y=70)

# 그래프 수정 정보 표시
formula_label = tk.Label(window, text="")
formula_label.place(x=10, y=70)

# UI 실행
window.mainloop()
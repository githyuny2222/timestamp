import os
import pickle
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import *

list_day = ['월','화','수','목','금']   # 요일 저장해서 콤보박스에 출력할 리스트
list_DB = []    # 시간표 정보 저장할 리스트
list_var = [] # StringVar()들을 저장할 리스트
file_memo = "memo.txt"
file_timetable = "timetable.txt"

for i in range(50): # list_DB 초기화
    temp = '','',''
    list_DB.append(temp)

# 파일 메뉴 메시지 박스 함수
def yesno_save():
    response = msgbox.askyesno("HYUN Timetable", "기존의 시간표에 덮어쓰기 됩니다.\n정말로 현재 시간표를 저장하시겠습니까?")
    return response
def saveInfo():
    msgbox.showinfo("알림", "시간표가 저장되었습니다.")
def yesno_exit():
    response = msgbox.askyesno("HYUN Timetable", "정말로 프로그램을 종료하시겠습니까?")
    return response

# 버튼 함수 부분
def btncmd_add():
    str1 = txt_subject.get("1.0", END + "-1c")
    if ' ' in str1:     # 띄어쓰기 있을경우 개행문자로 변경
        str1 = str1.replace(' ', '\n')
    elif len(str1) > 7:   # 7글자보다 길어질 경우 개행
        str2 = str1[0:7]
        str3 = str1[7:len(str1)]
        str1 = str2+'\n'+str3

    temp = combo_day.get(), combo_time.get(), str1   # 콤보박스 정보 가져옴

    for i in list_day:  # 요일별로 인덱스와 맞는지 확인
        if temp[0] == i + "요일" :
            day = list_day.index(i)
    for i in range(1,11):   # 몇교시인지 확인
        if temp[1] == str(i) + "교시" :
            clas = int(i)

    try:
        idx = 10*day + clas-1
        list_DB[idx] = temp
    except UnboundLocalError:
        pass

    for i in range(50): # 라벨 텍스트 바꾸기
        list_var[i].set(list_DB[i][2])

def btncmd_del():
    temp = combo_day.get(), combo_time.get(),''   # 콤보박스의 요일 시간 가져오고 과목대신 공백 넣음

    for i in list_day:  # 요일별로 인덱스와 맞는지 확인
        if temp[0] == i + "요일" :
            day = list_day.index(i)
    for i in range(1,11):   # 몇교시인지 확인
        if temp[1] == str(i) + "교시" :
            clas = int(i)
    
    try:
        idx = 10*day + clas-1
        list_DB[idx] = temp
    except UnboundLocalError:
        pass

    for i in range(50): # 라벨 텍스트 바꾸기
        list_var[i].set(list_DB[i][2])

def new_file():
    temp = '','',''
    for i in range(50): # list_DB 초기화
        list_DB.insert(i, temp)
    for i in range(50): # 라벨 텍스트 바꾸기
        list_var[i].set(list_DB[i][2])
        
def save_file():
    if yesno_save() == True:
        with open(file_timetable, "wb") as f:   # 시간표 저장
            pickle.dump(list_DB, f)
        with open(file_memo, "w", encoding="utf8") as f:    # 메모 저장
            f.write(txt_memo.get("1.0", END))
        saveInfo()
    else:
        pass

def load_file():
    with open(file_timetable, "rb") as f:   # 파일 불러오기
        temp = pickle.load(f)
        for i in range(50):
            list_DB[i] = temp[i]
    for i in range(50): # 라벨 텍스트 바꾸기
        list_var[i].set(list_DB[i][2])

def helpText():
    msgbox.showinfo("Help", '''New File : 새로운 시간표를 생성합니다.
                    \nSave File : 현재 생성한 시간표를 저장합니다.
                    \nLoad File : 저장한 시간표를 불러옵니다.
                    \n시간표 추가/수정 : 요일과 시간을 고르고 과목명을 적은 뒤 버튼을 눌러 추가 혹은 수정합니다.
                    \n시간표 삭제 : 요일과 시간을 고르고 버튼을 눌러 삭제합니다.
                    \n메모 : 자유로운 메모 공간입니다. 프로그램을 다시 시작해도 유지됩니다.''')

def save_memo():    # 프로그램 종료시에 저장
    if yesno_exit() == True:
        with open(file_memo, "w", encoding="utf8") as f:    # 메모 저장
            f.write(txt_memo.get("1.0", END))
        root.quit()
    else:
        pass

def load_memo():
    if(os.path.isfile(file_memo)):
        with open(file_memo, "r", encoding="utf8") as f:
            txt_memo.insert(END, f.read())    # 파일 내용 본문에 추가

# ----------------------------------------여기서 부터 GUI -------------------------------------------------------- #
root = Tk()
root.title("HYUN TimeTable")
root.geometry("1000x670+400-100")
root.configure(background='LightYellow')

for i in range(50): # list_var 초기화
    list_var.append(StringVar())

# 파일 메뉴
menu = Menu(root)
menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="New File", command=new_file)
menu_file.add_command(label="Save File", command=save_file)
menu_file.add_command(label="Load File", command=load_file)
menu_file.add_separator()
menu_file.add_command(label="Exit",command=save_memo)
menu.add_cascade(label="File", menu=menu_file)
root.config(menu=menu)

# 도움말 메뉴
menu_help = Menu(menu, tearoff=0)
menu_help.add_command(label='Need Help?',command=helpText)
menu.add_cascade(label="Help", menu=menu_help)
root.config(menu=menu)

# 요일
label_space = Label(root, text="", padx=40, pady=20, bg='LightYellow', fg='black')
label_mon = Label(root, text="월", padx=40, pady=20, bg='LightYellow', fg='black')
label_tue = Label(root, text="화", padx=40, pady=20, bg='LightYellow', fg='black')
label_wed = Label(root, text="수", padx=40, pady=20, bg='LightYellow', fg='black')
label_thu = Label(root, text="목", padx=40, pady=20, bg='LightYellow', fg='black')
label_fri = Label(root, text="금", padx=40, pady=20, bg='LightYellow', fg='black')

label_space.grid(row=0, column=0, sticky=N+E+W+S)
label_mon.grid(row=0, column=1, sticky=N+E+W+S)
label_tue.grid(row=0, column=2, sticky=N+E+W+S)
label_wed.grid(row=0, column=3, sticky=N+E+W+S)
label_thu.grid(row=0, column=4, sticky=N+E+W+S)
label_fri.grid(row=0, column=5, sticky=N+E+W+S)

# 시간
label_9 = Label(root, text="9", padx=5, pady=20, bg='LightYellow', fg='black')
label_10 = Label(root, text="10", padx=5, pady=20, bg='LightYellow', fg='black')
label_11 = Label(root, text="11", padx=5, pady=20, bg='LightYellow', fg='black')
label_12 = Label(root, text="12", padx=5, pady=20, bg='LightYellow', fg='black')
label_13 = Label(root, text="13", padx=5, pady=20, bg='LightYellow', fg='black')
label_14 = Label(root, text="14", padx=5, pady=20, bg='LightYellow', fg='black')
label_15 = Label(root, text="15", padx=5, pady=20, bg='LightYellow', fg='black')
label_16 = Label(root, text="16", padx=5, pady=20, bg='LightYellow', fg='black')
label_17 = Label(root, text="17", padx=5, pady=20, bg='LightYellow', fg='black')
label_18 = Label(root, text="18", padx=5, pady=20, bg='LightYellow', fg='black')

label_9.grid(row=1, column=0, sticky=N+E+W+S)
label_10.grid(row=2, column=0, sticky=N+E+W+S)
label_11.grid(row=3, column=0, sticky=N+E+W+S)
label_12.grid(row=4, column=0, sticky=N+E+W+S)
label_13.grid(row=5, column=0, sticky=N+E+W+S)
label_14.grid(row=6, column=0, sticky=N+E+W+S)
label_15.grid(row=7, column=0, sticky=N+E+W+S)
label_16.grid(row=8, column=0, sticky=N+E+W+S)
label_17.grid(row=9, column=0, sticky=N+E+W+S)
label_18.grid(row=10, column=0, sticky=N+E+W+S)

# 1교시 수업
label_1mon = Label(root, textvariable=list_var[0], relief='groove', bg='white', fg='black')
label_1tue = Label(root, textvariable=list_var[10], relief='groove', bg='white', fg='black')
label_1wed = Label(root, textvariable=list_var[20], relief='groove', bg='white', fg='black')
label_1thu = Label(root, textvariable=list_var[30], relief='groove', bg='white', fg='black')
label_1fri = Label(root, textvariable=list_var[40], relief='groove', bg='white', fg='black')

label_1mon.grid(row=1, column=1, sticky=N+E+W+S)
label_1tue.grid(row=1, column=2, sticky=N+E+W+S)
label_1wed.grid(row=1, column=3, sticky=N+E+W+S)
label_1thu.grid(row=1, column=4, sticky=N+E+W+S)
label_1fri.grid(row=1, column=5, sticky=N+E+W+S)

# 2교시 수업
label_2mon = Label(root, textvariable=list_var[1], relief='groove', bg='white', fg='black')
label_2tue = Label(root, textvariable=list_var[11], relief='groove', bg='white', fg='black')
label_2wed = Label(root, textvariable=list_var[21], relief='groove', bg='white', fg='black')
label_2thu = Label(root, textvariable=list_var[31], relief='groove', bg='white', fg='black')
label_2fri = Label(root, textvariable=list_var[41], relief='groove', bg='white', fg='black')

label_2mon.grid(row=2, column=1, sticky=N+E+W+S)
label_2tue.grid(row=2, column=2, sticky=N+E+W+S)
label_2wed.grid(row=2, column=3, sticky=N+E+W+S)
label_2thu.grid(row=2, column=4, sticky=N+E+W+S)
label_2fri.grid(row=2, column=5, sticky=N+E+W+S)

# 3교시 수업
label_3mon = Label(root, textvariable=list_var[2], relief='groove', bg='white', fg='black')
label_3tue = Label(root, textvariable=list_var[12], relief='groove', bg='white', fg='black')
label_3wed = Label(root, textvariable=list_var[22], relief='groove', bg='white', fg='black')
label_3thu = Label(root, textvariable=list_var[32], relief='groove', bg='white', fg='black')
label_3fri = Label(root, textvariable=list_var[42], relief='groove', bg='white', fg='black')

label_3mon.grid(row=3, column=1, sticky=N+E+W+S)
label_3tue.grid(row=3, column=2, sticky=N+E+W+S)
label_3wed.grid(row=3, column=3, sticky=N+E+W+S)
label_3thu.grid(row=3, column=4, sticky=N+E+W+S)
label_3fri.grid(row=3, column=5, sticky=N+E+W+S)

# 4교시 수업
label_4mon = Label(root, textvariable=list_var[3], relief='groove', bg='white', fg='black')
label_4tue = Label(root, textvariable=list_var[13], relief='groove', bg='white', fg='black')
label_4wed = Label(root, textvariable=list_var[23], relief='groove', bg='white', fg='black')
label_4thu = Label(root, textvariable=list_var[33], relief='groove', bg='white', fg='black')
label_4fri = Label(root, textvariable=list_var[43], relief='groove', bg='white', fg='black')

label_4mon.grid(row=4, column=1, sticky=N+E+W+S)
label_4tue.grid(row=4, column=2, sticky=N+E+W+S)
label_4wed.grid(row=4, column=3, sticky=N+E+W+S)
label_4thu.grid(row=4, column=4, sticky=N+E+W+S)
label_4fri.grid(row=4, column=5, sticky=N+E+W+S)

# 5교시 수업
label_5mon = Label(root, textvariable=list_var[4], relief='groove', bg='white', fg='black')
label_5tue = Label(root, textvariable=list_var[14], relief='groove', bg='white', fg='black')
label_5wed = Label(root, textvariable=list_var[24], relief='groove', bg='white', fg='black')
label_5thu = Label(root, textvariable=list_var[34], relief='groove', bg='white', fg='black')
label_5fri = Label(root, textvariable=list_var[44], relief='groove', bg='white', fg='black')

label_5mon.grid(row=5, column=1, sticky=N+E+W+S)
label_5tue.grid(row=5, column=2, sticky=N+E+W+S)
label_5wed.grid(row=5, column=3, sticky=N+E+W+S)
label_5thu.grid(row=5, column=4, sticky=N+E+W+S)
label_5fri.grid(row=5, column=5, sticky=N+E+W+S)

# 6교시 수업
label_6mon = Label(root, textvariable=list_var[5], relief='groove', bg='white', fg='black')
label_6tue = Label(root, textvariable=list_var[15], relief='groove', bg='white', fg='black')
label_6wed = Label(root, textvariable=list_var[25], relief='groove', bg='white', fg='black')
label_6thu = Label(root, textvariable=list_var[35], relief='groove', bg='white', fg='black')
label_6fri = Label(root, textvariable=list_var[45], relief='groove', bg='white', fg='black')

label_6mon.grid(row=6, column=1, sticky=N+E+W+S)
label_6tue.grid(row=6, column=2, sticky=N+E+W+S)
label_6wed.grid(row=6, column=3, sticky=N+E+W+S)
label_6thu.grid(row=6, column=4, sticky=N+E+W+S)
label_6fri.grid(row=6, column=5, sticky=N+E+W+S)

# 7교시 수업
label_7mon = Label(root, textvariable=list_var[6], relief='groove', bg='white', fg='black')
label_7tue = Label(root, textvariable=list_var[16], relief='groove', bg='white', fg='black')
label_7wed = Label(root, textvariable=list_var[26], relief='groove', bg='white', fg='black')
label_7thu = Label(root, textvariable=list_var[36], relief='groove', bg='white', fg='black')
label_7fri = Label(root, textvariable=list_var[46], relief='groove', bg='white', fg='black')

label_7mon.grid(row=7, column=1, sticky=N+E+W+S)
label_7tue.grid(row=7, column=2, sticky=N+E+W+S)
label_7wed.grid(row=7, column=3, sticky=N+E+W+S)
label_7thu.grid(row=7, column=4, sticky=N+E+W+S)
label_7fri.grid(row=7, column=5, sticky=N+E+W+S)

# 8교시 수업
label_8mon = Label(root, textvariable=list_var[7], relief='groove', bg='white', fg='black')
label_8tue = Label(root, textvariable=list_var[17], relief='groove', bg='white', fg='black')
label_8wed = Label(root, textvariable=list_var[27], relief='groove', bg='white', fg='black')
label_8thu = Label(root, textvariable=list_var[37], relief='groove', bg='white', fg='black')
label_8fri = Label(root, textvariable=list_var[47], relief='groove', bg='white', fg='black')

label_8mon.grid(row=8, column=1, sticky=N+E+W+S)
label_8tue.grid(row=8, column=2, sticky=N+E+W+S)
label_8wed.grid(row=8, column=3, sticky=N+E+W+S)
label_8thu.grid(row=8, column=4, sticky=N+E+W+S)
label_8fri.grid(row=8, column=5, sticky=N+E+W+S)

# 9교시 수업
label_9mon = Label(root, textvariable=list_var[8], relief='groove', bg='white', fg='black')
label_9tue = Label(root, textvariable=list_var[18], relief='groove', bg='white', fg='black')
label_9wed = Label(root, textvariable=list_var[28], relief='groove', bg='white', fg='black')
label_9thu = Label(root, textvariable=list_var[38], relief='groove', bg='white', fg='black')
label_9fri = Label(root, textvariable=list_var[48], relief='groove', bg='white', fg='black')

label_9mon.grid(row=9, column=1, sticky=N+E+W+S)
label_9tue.grid(row=9, column=2, sticky=N+E+W+S)
label_9wed.grid(row=9, column=3, sticky=N+E+W+S)
label_9thu.grid(row=9, column=4, sticky=N+E+W+S)
label_9fri.grid(row=9, column=5, sticky=N+E+W+S)

# 10교시 수업
label_10mon = Label(root, textvariable=list_var[9], relief='groove', bg='white', fg='black')
label_10tue = Label(root, textvariable=list_var[19], relief='groove', bg='white', fg='black')
label_10wed = Label(root, textvariable=list_var[29], relief='groove', bg='white', fg='black')
label_10thu = Label(root, textvariable=list_var[39], relief='groove', bg='white', fg='black')
label_10fri = Label(root, textvariable=list_var[49], relief='groove', bg='white', fg='black')

label_10mon.grid(row=10, column=1, sticky=N+E+W+S)
label_10tue.grid(row=10, column=2, sticky=N+E+W+S)
label_10wed.grid(row=10, column=3, sticky=N+E+W+S)
label_10thu.grid(row=10, column=4, sticky=N+E+W+S)
label_10fri.grid(row=10, column=5, sticky=N+E+W+S)

# 오른쪽 GUI
label_time = Label(root, text="시간", bg='LightYellow', fg='black')   # 시간 라벨
label_time.place(x=620, y=40)
label_subject = Label(root, text="과목", bg='LightYellow', fg='black')    # 과목 라벨
label_subject.place(x=620, y= 70)

values = [str(i) + "요일" for i in list_day]    # 요일 콤보박스
combo_day = ttk.Combobox(root, values=values, state="readonly")
combo_day.place(x=660, y=40, width = 150, height=20)
combo_day.set("요일 선택")

values = [str(i) + "교시" for i in range(1,11)] # 시간 콤보박스
combo_time = ttk.Combobox(root, values=values, state="readonly")
combo_time.place(x=815, y=40, width = 150, height=20)
combo_time.set("시간 선택")

txt_subject = Text(root)
txt_subject.place(x=660, y=70, width = 305, height=20)
txt_subject.insert(END, "과목을 입력하세요")

btn_add = Button(root, text="추가 / 수정", width=10, height=2, command=btncmd_add, relief='flat', bg='#FFCC66', fg='black')
btn_del = Button(root, text="삭제", width=10, height=2, command=btncmd_del, relief='flat', bg='#FFCC66', fg='black')
btn_add.place(x=660, y=100)
btn_del.place(x=885, y=100)

# 메모 공간
label_memo = Label(root, text="메모", bg='LightYellow', fg='black')
label_memo.place(x=790, y=180)
txt_memo = Text(root)
txt_memo.place(x=660, y=210, width=305, height=440)

load_memo()

root. resizable(False, False)   #창 크기 변경
root.mainloop()
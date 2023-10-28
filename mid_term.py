import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from openpyxl import load_workbook


base_dir = "/Users/binwon/Downloads"
file_nm = "2023-02-midterm.xlsx"
xlsx_dir = os.path.join(base_dir, file_nm)
class1_xlsx_dir = os.path.join(base_dir, "1분반-" + file_nm)
class2_xlsx_dir = os.path.join(base_dir, "2분반-" + file_nm)
a="/Users/binwon/Downloads/1분반-2023-02-midterm.xlsx"
b="/Users/binwon/Downloads/2분반-2023-02-midterm.xlsx"
result = [True, True, True, False, False, True, True, False, True, True, False, False, True, False, True]
fault_analyze = {i: 0 for i in range(1, 16)}
None_analyze = {i: 0 for i in range(1, 16)}
class1_score_dict = {}
class2_score_dict = {}

while True:
    score = 0
    student_class=int(input("분반 입력 : "))
    student_id = input("학번 입력(입력 중단 : -1 ) : ")
    if student_id == "-1":
        break
    student_name = input("이름 입력 : ")
    TF_input = input("TF 입력 ex) TTTFFTTFTTFFTFT :\n")
    while len(TF_input) != 15:
        print("\nTF 갯수 오류! 재입력")
        TF_input = input("TF 입력 ex) TTFFNTNF :\n")
    

    for q_num, q_ans in enumerate(TF_input):

        if q_ans == 'f' or q_ans == 't' or q_ans == 'n':
            q_ans = q_ans.upper()

        if q_ans == 'T':
            q_ans = True
        elif q_ans == 'F':
            q_ans = False


        if q_ans == "N":  # None 값인 경우
            None_analyze[q_num + 1] += 1
        elif q_ans == result[q_num]:  # 정답일 경우
            score += 2
        elif q_ans != result[q_num]:  # 오답인 경우
            score -= 1
            fault_analyze[q_num + 1] += 1
        
    another_question=map(int,input("서술형 점수 기입 : ").split())
    score+=sum(another_question)
    if student_class==1:
        class1_score_dict[student_id] = score
    elif student_class==2:
        class2_score_dict[student_id]=score
        
    print(f"score : {score}")

print("\n\n틀린 문제")
print(fault_analyze)
print("=========================\n")
print("무응답 문제")
print(None_analyze)
print("=========================\n")
print("점수 통계")
print(f"1분반 : \n{class1_score_dict}")
print(f"2분반 : \n{class2_score_dict}")
score_dict =dict(class1_score_dict)
score_dict.update(class2_score_dict)

# 데이터프레임 수정
class1_df = pd.DataFrame({"학번": list(class1_score_dict.keys()), "점수": list(class1_score_dict.values())})
class2_df = pd.DataFrame({"학번": list(class2_score_dict.keys()), "점수": list(class2_score_dict.values())})


class1_df.to_excel(excel_writer=class1_xlsx_dir, sheet_name='2023, 1분반_시스템 소프트웨어 중간시험', na_rep='NaN', header=True)
class2_df.to_excel(excel_writer=class2_xlsx_dir, sheet_name='2023, 2분반_시스템 소프트웨어 중간시험', na_rep='NaN', header=True)


# 틀린 문제와 무응답 문제를 정렬하여 다시 생성
fault_analyze = {f"Q {key}": value for key, value in sorted(fault_analyze.items(), key=lambda item: item[1], reverse=True)}
None_analyze = {f"Q {key}": value for key, value in sorted(None_analyze.items(), key=lambda item: item[1], reverse=True)}

wrong_name = list(fault_analyze.keys())
wrong_val = list(fault_analyze.values())

plt.bar(wrong_name, wrong_val)
plt.xticks(rotation=45)
plt.title('Wrong Response')
plt.xlabel('Question')
plt.ylabel('number of wrong response')
plt.show()

none_name = list(None_analyze.keys())
none_val = list(None_analyze.values())

plt.bar(none_name, none_val)
plt.xticks(rotation=45)
plt.title('None response')
plt.xlabel('Question')
plt.ylabel('Number of none response')
plt.show()

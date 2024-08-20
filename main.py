import numpy as np
from tabulate import tabulate

# NUMPY 
# Without for
# course_topics : [[101,3,1,10],[102,2,11,10],[103,4,21,10],[104,2,31,20]]

### Make Sheets------------------------------------------------------------------------------------------------------
def make_sheets(participant, input_topics, method = 1):
    course_topics = np.array(eval(input_topics))
    num_question = np.sum(course_topics[:,3])
    # Answer Sheet --------------------------------------------------------
    answer_sheet = np.random.randint(0,5,[participant,num_question])
    # Key Sheet -----------------------------------------------------------
    key_sheet = np.random.randint(1,5,[1,num_question])
    # Participants information --------------------------------------------
    partic_info = np.zeros((participant, 2))
    partic_info[:, 0] = np.random.randint(100, 1000, participant)
    partic_info[:, 1] = np.random.randint(0, 2, participant)
    method = int(method) if method else 1

    return answer_sheet, key_sheet, partic_info, course_topics, num_question, method


### Show Topic Information-------------------------------------------------------------------------------------------
def topic_info(course_topics):
    table = tabulate(course_topics, headers = ["Topic-ID", "Coefficient", "Start from", "Number of Q"], tablefmt = "pretty")
    print(table)


### Show Right Answer------------------------------------------------------------------------------------------------
def show_key_sheet(num_question, key_sheet):
    data = np.vstack((np.arange(1, num_question + 1), key_sheet))
    data = np.column_stack((["Question","Right Answer"], data))
    table = tabulate(data[1:], headers = data[0], tablefmt = "pretty")
    print(table)


zero_to_replace = np.array([])
### Show absent participant------------------------------------------------------------------------------------------
def absence(participant, answer_sheet, partic_info):
    # Absence person ------------------------------------------------------
    zero_rows = np.where((answer_sheet == 0).all(axis=1))[0]
    if len(zero_rows) > 0:
        print("Absent student list :",zero_rows)
        zero_to_replace = np.array([])
    else:
        print("All students were persent in the exam")

        while True:
            num_absence = int(input("Please enter number of absent student : "))
            if num_absence <= participant :
                break
            else:
                print("Entered number is greater than number of participant !!!")

        zero_to_replace = np.random.choice(np.arange(participant), num_absence, replace=False)   # to not make duplicate value 
        answer_sheet[zero_to_replace, : ] = 0
        print("Absent persons : ", partic_info[zero_to_replace, 0])
        print(answer_sheet)
    return answer_sheet, zero_to_replace


### Show Participant Information-------------------------------------------------------------------------------------
def show_partic_info(partic_info):
    data = partic_info
    table = tabulate(data, headers = ["STU ID", "Gender(0 M / 1 W)"], tablefmt = "pretty")
    print(table)

### Evaluate Answer--------------------------------------------------------------------------------------------------
def correct_answer(course_topics, answer_sheet, key_sheet, method):

    topics_part = np.repeat(np.arange(len(course_topics[:,3])),course_topics[:,3])
    col_index = np.tile(topics_part, participant)

    row_index = np.repeat(np.arange(len(answer_sheet)), num_question)
    
    right = np.zeros((participant, len(course_topics)))
    empty = np.zeros((participant, len(course_topics)))

    right_ans = np.where(answer_sheet == key_sheet, 1, 0).reshape(participant * num_question)
    empty_ans = np.where(answer_sheet == 0, 1, 0).reshape(participant * num_question)

    np.add.at(right,(row_index, col_index), right_ans)
    np.add.at(empty,(row_index, col_index), empty_ans)

    all_question = np.tile(course_topics[:,3], participant).reshape(participant, len(course_topics))
    coefficient = np.tile(course_topics[:,1], participant).reshape(participant, len(course_topics))
    wrong = all_question - right - empty

    if method == 1:
        score = np.round(np.sum((right - (wrong / 3)) * coefficient, axis = 1),2)
        percent = np.round(((right - (wrong / 3)) / all_question * 100),2)
    else:
        score = np.round(np.sum(right * coefficient, axis = 1),2)
        percent = np.round((right / all_question * 100),2)

    ranks = np.argsort(score)[::-1].argsort() + 1

    print("Correct successfully.---------------------")
    return right, empty, wrong, score, percent, ranks


### Show Participant Report------------------------------------------------------------------------------------------
def show_score(course_topics, partic_info, ranks, right, empty, wrong, score, percent, zero_to_replace):

    stu_id = int(input("Please enter Student ID to show grade and rank : "))
    if stu_id not in partic_info[:, 0]:
        print("There is no participant with this ID !!!")
        return
    if len(zero_to_replace) > 0:
        if stu_id in partic_info[zero_to_replace, 0]:
            print("The participant was absent !!!")
            return

    student_index = np.where(partic_info[:, 0] == stu_id)[0]
    stu_rank = ranks[student_index]
    stu_score = score[student_index]

    perform_report = np.vstack((right[student_index], wrong[student_index], empty[student_index], percent[student_index]))
    perform_report = np.column_stack((["Right answer", "Wrong answer","Empty answer", "Percentage"], perform_report))

    data = [[stu_id,int(stu_rank), int(stu_score)]]
    headers = ["Student ID", "Rank", "Score"]
    table = tabulate(data, headers = headers, tablefmt = "pretty")
    print(table)

    headers = course_topics[:,0]
    headers = np.insert(headers, 0, stu_id)
    table = tabulate(perform_report, headers = headers, tablefmt = "pretty")
    print(table)

### Show Topic Report------------------------------------------------------------------------------------------------
def topic(course_topics, partic_info, right, empty, wrong, percent):

    topic_id = int(input("Please enter Topic-ID to show its indicators : "))
    if topic_id not in course_topics[:,0]:
        print("There is no topic with this ID !!!")
        return
    topic_index = np.where(course_topics[:,0] == topic_id)[0]

    female_right = right[:,topic_index] * partic_info[:,1].reshape(participant,1)
    female_wrong = wrong[:,topic_index] * partic_info[:,1].reshape(participant,1)
    female_empty = empty[:,topic_index] * partic_info[:,1].reshape(participant,1)
    female_percent = percent[:,topic_index] * partic_info[:,1].reshape(participant,1)

    male_right = right[:,topic_index] - female_right
    male_wrong = wrong[:,topic_index] - female_wrong
    male_empty = empty[:,topic_index] - female_empty
    male_percent = percent[:,topic_index] - female_percent

    female_number = np.sum(partic_info[:,1])
    male_number = len(partic_info) - female_number

    female_report = np.round(np.array([np.sum(female_right), np.sum(female_wrong), np.sum(female_empty), np.sum(female_percent)]) / female_number,2)
    male_report = np.round(np.array([np.sum(male_right), np.sum(male_wrong), np.sum(male_empty), np.sum(male_percent)]) / male_number,2)
    total_report = np.round(np.array([np.mean(right[:,topic_index]), np.mean(wrong[:,topic_index]), np.mean(empty[:,topic_index]), np.mean(percent[:,topic_index])]),2)

    topic_report = np.vstack((female_report, male_report, total_report))
    topic_report = np.column_stack((["Female","Male","Total"],[female_number,male_number,np.shape(partic_info)[0]],topic_report))
    table = tabulate(topic_report, headers = ["Gender", "Number", "Average of Right ans", "Average of wrong ans","Average of empty ans","Average of Percent"], tablefmt = "pretty")
    print(table)


### Menu -----------------------------------------------------------
menu_text = """
What would you like to do:
1. Making answer sheet
2. Show topic info & key-sheet & answer-sheet
3. Show participant info
4. Show absent participant(first output)
5. Correct answers
6. Show Score(second output)
7. Show topic indicators(third output)
0. Exit the Menu
"""

menu_lines = menu_text.strip().split('\n')
formatted_menu = tabulate(list(map(lambda line: (line,), menu_lines)), tablefmt="fancy_grid", headers=["Menu"])


print("Wellcome!!!\nfirst, please enter number of participant\nthen, please enter information of topic\nthen, enter method of evaluation\nthen, you can check absents person\nthen correct the answer sheet. now you can see output 2 and 3!!!")
while True:
    print(formatted_menu)
    choice = int(input("What do you choose?"))
    
    if choice == 1:
        participant = int(input("Please enter number of participants :"))
        input_topics = input("Please enter topic info : ")
        method = input("Please enter method of evaluation :")
        answer_sheet, key_sheet, partic_info, course_topics, num_question, method = make_sheets(participant, input_topics, method)
    elif choice == 2:
        topic_info(course_topics)
        show_key_sheet(num_question, key_sheet)
        print(answer_sheet)
    elif choice == 3:
        show_partic_info(partic_info)
    elif choice == 4:
        answer_sheet, zero_to_replace = absence(participant, answer_sheet, partic_info)
    elif choice == 5:
        right, empty, wrong, score, percent, ranks = correct_answer(course_topics, answer_sheet, key_sheet, method)
    elif choice == 6:
        show_score(course_topics, partic_info, ranks, right, empty, wrong, score, percent, zero_to_replace)
    elif choice == 7:
        topic(course_topics, partic_info, right, empty, wrong, percent)
    else:
        break
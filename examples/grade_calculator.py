student_name = ''
mathematics = 0
english = 0
science = 0
total = 0
average = 0.0
grade = ''
print('===== STUDENT GRADE CALCULATOR =====')
student_name = input('Enter student name: ')
mathematics = int(input('Enter Mathematics marks: '))
english = int(input('Enter English marks: '))
science = int(input('Enter Science marks: '))
total = ((mathematics + english) + science)
average = (total / 3)
if (average >= 80):
    grade = 'A'
else:
    if (average >= 70):
        grade = 'B'
    else:
        if (average >= 60):
            grade = 'C'
        else:
            if (average >= 50):
                grade = 'D'
            else:
                grade = 'E'
print('===== STUDENT RESULTS =====')
print('Student:')
print(student_name)
print('Total marks:')
print(total)
print('Average:')
print(average)
print('Grade:')
print(grade)

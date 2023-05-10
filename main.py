import datetime

#this is feature1
#this is feature2

#develop change1
#develop change2
#develop change3
#develop change4
#develop change5

#develop change6
#removed change7
#change 8
#change9
#change10
#change11
#change12
#change13
#change14
#I'm on the develop branch
from employee import Employee,Admin, Manager
from employee import EmployeesDataBase as edb
from attendance import AttendancyManagment as attMng
from menu import Menu


emp_to_add_csv = 'employees_to_add.csv'

#edb.add_employee_manually()

# employee1 = Admin('033040064','Dana Medina', '0523263030', 47)
# employee2 = Manager('032806036','Yaacov Rosman', '0543034470', 44,"Developer")
# employee3 = Employee('331810515','Saar Rosman', '0559424774', 14)
# edb.add_employee_to_file(employee1)
# edb.add_employee_to_file(employee2)
# edb.add_employee_to_file(employee3)
# edb.add_employees_by_csv(emp_to_add_csv)
# edb.del_employee_from_file(['33040064'])
# edb.delete_employee_manually()
# edb.del_employee_by_csv(emp_to_add_csv)
#
#
# attMng.mark_attendance_now('331810515')
# attMng.mark_attendance_now('033040064')
# attMng.mark_attendance_now('032806036')
#attMng.create_test_attendance_log_file(emp_to_add_csv)
#
#
#report = attMng.get_attendance_report(datetime.datetime(2023,1,10),datetime.datetime(2023,1,20))
#report = attMng.get_attendance_report(datetime.datetime(2023,1,10),datetime.datetime(2023,1,20), datetime.time(9,30), "221510545")
#report = attMng.get_attendance_report_late()
#report = attMng.get_attendance_report_employee('221510545')
# report = attMng.get_attendance_report_current_month()
# for line in report:
#     print(line, end='')
#
#
#
#admin1 = Admin('033040064','Dana Medina', '0523263030', 47)
print(admin1 + " chanage 2 in origin")
#edb.add_employee_to_file(admin1)
#
Menu.start_menu()

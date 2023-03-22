import datetime
import employee
from employee import EmployeesDataBase as edb
import attendance.AttendancyManagment as am
import helpFuncs as hf


class Menu:
    emp_to_add_csv = 'employees_to_add.csv'
    general_admin = employee.Admin('0','General Admin')

    @staticmethod
    def call_mark_attendance(id):
        am.mark_attendance_now(id)
        input('\nPress enter to continue \n')

    @staticmethod
    def print_attendance_report_employee(id):
        [print(line, end= ' ') for line in am.get_attendance_report_employee(id)]
        input('\nPress enter to continue \n')

    @staticmethod
    def print_attendance_report_late(id):
        [print(line, end=' ') for line in am.get_attendance_report_late()]
        input('\nPress enter to continue \n')

    @staticmethod
    def print_attendance_report_current_month(id):
        [print(line, end=' ') for line in am.get_attendance_report_current_month()]
        input('\nPress enter to continue \n')

    @staticmethod
    def print_attendance_report_other_emp(id):
        id = hf.ask_input_int("Enter employee's ID: ")
        if edb.is_employee_exist(id):
            [print(line, end=' ') for line in am.get_attendance_report_employee(id)]
        else:
            print('ID %s was not found. '%id)
        input('\nPress enter to continue \n')

    @staticmethod
    def print_attendance_report_by_dates(id):
        while True:
            try:
                date = input('Enter start date in the format dd/mm/yyyy:').split('/')
                start_date = hf.get_date(date[::-1])
                date = input('Enter end date in the format dd/mm/yyyy:').split('/')
                end_date = hf.get_date(date[::-1])
                lines = am.get_attendance_report(start_date=start_date, end_date=end_date)
                if(len(lines) >0):
                    print('Attendances between the dates %s to %s: '%(start_date.date(),end_date.date()))
                    [print(line, end=' ') for line in lines]
                else:
                    print('No attendances were found between the dates %s to %s.'%(start_date.date(),end_date.date()))
                break
            except (IndexError, TypeError, ValueError, AttributeError):
                print('Please write a valid date using the correct format, numbers only.')
        input('\nPress enter to continue \n')

    @staticmethod
    def add_employee_manually(id):
        edb.add_employee_manually()
        input('\nPress enter to continue \n')

    @classmethod
    def add_employee_from_csv_file(cls, id):
        file_name = input('Enter file name (or "enter" for the default "%s"): ' % cls.emp_to_add_csv)
        file_name = file_name if file_name !='' else cls.emp_to_add_csv
        employees = edb.add_employees_by_csv(file_name)
        if employees!=None:
            print('The following employees were added:')
            [print(emp.__repr__()) for emp in employees]
        else:
            print('No new employees were added')
        input('\nPress enter to continue \n')


    @staticmethod
    def del_employee_manually(id):
        edb.delete_employee_manually()
        input('\nPress enter to continue \n')

    @classmethod
    def del_employee_by_csv_file(cls, id):
        file_name = input('Enter file name with employees to delete (press enter to use default file "%s"): \n'% cls.emp_to_add_csv)
        file_name = file_name if file_name != '' else cls.emp_to_add_csv
        lines = edb.del_employee_by_csv(file_name)
        print('The following employees were deleted: \n'+ ''.join([line for line in lines])) if lines != None else print('No employees were deleted. ')
        input('\nPress enter to continue \n')

    @staticmethod
    def display_employee(id):
        id = hf.ask_input_int("Enter employee's ID: ")
        emp = edb.get_employee_by_id(id)
        print(emp if emp != None else "Employees ID %s wasn't found. "%id)
        input('\nPress enter to continue \n')

    @staticmethod
    def display_all_employee(id):
        employees = edb.get_all_employees()
        print('Employees:')
        [print(emp.__repr__()) for emp in employees]
        input('\nPress enter to continue \n')

    @staticmethod
    def display_epmloyees_data_by_job_title(id):
        msg = 'Enter the required job title: %s'%''.join('\n%s. %s '%(index+1, job) for index, job in enumerate(edb.job_titles))
        job_title = edb.job_titles[int(hf.ask_input_int(msg)) -1]
        employees = edb.get_Employees_by_job_title(job_title)
        print('Displaying employees with job title "%s" data: \n'%job_title + '\n'.join([emp.__repr__() for emp in employees])) \
            if employees!=None else print('No employees with job title "%s" were found. '%job_title)
        input('\nPress enter to continue \n')

    @classmethod
    def get_employee_menu(cls, emp):

        employee_menu_options = [{'msg':'1. Mark attendance', 'func':cls.call_mark_attendance},
                                 {'msg':'2. Get your attendance log', 'func':cls.print_attendance_report_employee},
                                 {'msg':'3. Exit', 'func': None}
                                 ]
        admin_menu_options =    [employee_menu_options[0],
                                 employee_menu_options[1],
                                 {'msg':'3. Get late employees log', 'func': cls.print_attendance_report_late},
                                 {'msg':'4. Get all attendances in current month', 'func': cls.print_attendance_report_current_month},
                                 {'msg':'5. Get all attendances by date range','func': cls.print_attendance_report_by_dates},
                                 {'msg':'6. Get attendances of a specific employee','func': cls.print_attendance_report_other_emp},
                                 {'msg':'7. Get emolyees according to job title','func': cls.display_epmloyees_data_by_job_title},
                                 {'msg':'8. Add employee manually','func': cls.add_employee_manually},
                                 {'msg':'9. Add employees from csv file', 'func': cls.add_employee_from_csv_file},
                                 {'msg':'10. Delete employee manually', 'func': cls.del_employee_manually},
                                 {'msg':'11. Delete employees by csv file', 'func': cls.del_employee_by_csv_file},
                                 {'msg':'12. Display employee info ', 'func': cls.display_employee},
                                 {'msg':'13. Display all employees ', 'func': cls.display_all_employee},
                                 {'msg':'14. Exit', 'func': None}
                                ]
        return admin_menu_options if isinstance(emp, employee.Admin) else employee_menu_options


    @classmethod
    def start_menu(cls):
        while True:
            id = hf.ask_input_int('Please enter your ID: ')

            emp = edb.get_employee_by_id(id) if id != 0 else cls.general_admin
            emp_menu = cls.get_employee_menu(emp)
            if emp != None:
                print('Hello %s! \n' % emp.name)
                while True:
                    # concatenate the menu options:
                    msg ='What would you like to do? \n'
                    msg += '\n'.join([option['msg'] for option in emp_menu]) + '\n'

                    #display the menu and receives the user's choise:
                    choice = hf.ask_input_int(msg)
                    if choice==None or choice<=0 or choice>len(emp_menu):
                        input('Invalid choice. Press enter to continue \n')
                        continue


                    #run the function chosen by the user:
                    #index = 0 if choice == '' else choice - 1
                    index = choice - 1
                    if emp_menu[index]['func'] == None:
                        break   # break if Exit
                    else:
                        emp_menu[index]['func'](id) #run the chossen func

                    #Ask the user to run the menu again or exit:
                    print("\nAnything else?", end = ' ')
                break
            else:  # ID didn't match an existing employee
                print("Sorry, ID not found.")


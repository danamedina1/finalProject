import datetime
from random import randrange
from calendar import monthrange
import helpFuncs as hf
import employee
from employee import EmployeesDataBase as edb


class AttendancyManagment():
#manage Attendance logging and reporting

    attendance_log_file_name = 'attendance_log.csv'

    @classmethod
    def mark_attendance(cls, employee_id, date,  time):
        #mark received timestamp to the attendance log file for received employee:

        #get employee, check if employee exists:
        employee = edb.get_employee_by_id(employee_id)

        # if employee exists, write timestamp to the attendance log:
        while employee != None:
            try:
                with open(cls.attendance_log_file_name, 'a') as log_file:
                    log_file.write('%s, %s, %s, %s\n'%(employee_id, employee.name, date, time))
                    print('Attendace: %s (%s): %s, %s. '%(employee.name, employee_id,date,time))
                    break
            except PermissionError:
                input('Close %s before marking attendance. \nAfter closing the file, press enter to continue:'
                      % cls.attendance_log_file_name)
        else:
            print('Employee ID %s was not found.'%employee_id)

    @classmethod
    def mark_attendance_now(cls, employee_id):
        # get the timestamp and mark to the attendance log file by calling mark_attendance(cls, employee_id, time):
        now = datetime.datetime.now()
        cls.mark_attendance(employee_id, now.date(), now.time())

    @classmethod
    def get_attendance_report(cls, start_date = None, end_date = None, late_hour = None, employee_id=None, job_title=None):
        #returns an attendance report file between the dates, for the received employee.
        #if dates = None - return full log dates
        #if employee_id = None - return log for all employees

        #### get_date = lambda str_date: datetime.datetime(int(date_str[0]),int(date_str[1]),int(date_str[2]))
        #### get_time = lambda str_time: datetime.time(int(time_str[0]),int(time_str[1]),int(float(time_str[2])))

        try:
            with open(cls.attendance_log_file_name, 'r') as log_file:
                lines = log_file.readlines()
                report_list = []
                for line in lines:
                    split_line = line.split(',')
                    date_str = split_line[2].split('-')
                    time_str = split_line[3].split(':')
                    date = hf.get_date(date_str)
                    time = hf.get_time(time_str)
                    if (employee_id == None or str(int(split_line[0])) == str(employee_id)) and \
                            (start_date == None or date >= start_date) and \
                            (end_date == None or date <= end_date) and \
                            (late_hour == None or late_hour < time):
                        report_list.append(line)
                return report_list
        except ValueError:
            print('The received ID % is not a valid ID number'%employee_id)
            return None
        except FileNotFoundError:
            print('File %s not found.'%csv_file_name)
            return None


    @classmethod
    def get_attendance_report_late(cls):
        # calls get_attendance_report for all employees that were late for current month
        late_hour = datetime.time(9,30)#time frome which arrivle means late
        return cls.get_attendance_report(late_hour = late_hour)

    @classmethod
    def get_attendance_report_employee(cls, employee_id):
        #calls get_attendance_report for the received employee, all appearances in the attendance log
        return cls.get_attendance_report( employee_id = employee_id)

    @classmethod
    def get_attendance_report_current_month(cls):
        #calls get_attendance_report, full report for the current month
        today = datetime.datetime.today()
        start_date = datetime.datetime(today.year, today.month, 1)
        end_date = start_date + datetime.timedelta(days = monthrange(start_date.year, start_date.month)[1]-1)
        return cls.get_attendance_report(start_date= start_date, end_date = end_date )


    @classmethod
    def create_test_attendance_log_file(cls, emp_to_add_csv):
        #for testing purposes only, create an attendance log file with random timestamps for each date

        #add the employees:
        employees = edb.add_employees_by_csv(emp_to_add_csv)
        employees = edb.get_all_employees()

        #add all employees timestamps randomly between 8:00-11:00
        today = datetime.date.today()
        for month in range(1,4):
            for day in range(1, monthrange(today.year, month)[1]+1):
                start_datetime = datetime.datetime(today.year, month, day, hour=8)
                for emp in employees:
                    timestamp = start_datetime + datetime.timedelta(minutes=randrange(180))
                    cls.mark_attendance(emp.employee_id, timestamp.date(), timestamp.time())

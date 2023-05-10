import helpFuncs as hf

class Employee:
    #Holds employees data

    def __init__(self, employee_id=None, name=None, phone=None, age=None, job_title='Employee',args_list = None):
        #required ID, name, phone and age or args_list=[id, name, phone, age] (phone and age not mandatory)
        if(employee_id != None):
            self.employee_id = employee_id
            self.name = name
            self.phone = phone
            self.age = age
            self.job_title = job_title
        elif len(args_list) >=2:
            self.employee_id = args_list[0]
            self.name = args_list[1]
            self.phone = args_list[2] if len(args_list) >=3 else phone
            self.age = args_list[3] if len(args_list) >=4 else age
            self.job_title = args_list[4]  if len(args_list) >=5 else job_title

    def __str__(self):
        return 'Employee: \n\t\tName:\t%s\n\t\tID:\t\t%s\n\t\tPhone:\t%s\n\t\tAge:\t%s\n\t\tJob Title:\t%s'\
            %(self.name, self.employee_id, self.phone, self.age, self.job_title)

    def __repr__(self):
        return 'Name: %s, ID: %s, Phone: %s, Age: %s, Job Title: %s'\
            %(self.name, self.employee_id, self.phone, self.age, self.job_title)

class Admin(Employee):
    #Holds admin's data

    def __init__(self, employee_id=None, name=None, phone=None, age=None, job_title='Employee', admin='Admin', args_list = None):
        super().__init__(employee_id, name, phone, age, job_title, args_list)
        self.admin = admin

    def __str__(self):
        return super().__str__() +'\n\t\tAdmin:\t%s'%(self.admin)

class Manager(Admin):

    def __init__(self, employee_id=None, name=None, phone=None, age=None, job_title='Manager', admin='Admin', args_list = None):
        super().__init__(employee_id, name, phone, age, job_title, admin, args_list)


class EmployeesDataBase():
    #handles the emmployees data base
    csv_name = 'employees.csv'
    job_titles = ['Employee', 'Manager', 'Developer', 'HR']

    #check if ad employee's ID exists in the csv_name
    @classmethod
    def is_employee_exist(cls, employee_id):
        try:
            with open(cls.csv_name, 'r') as file:
                lines = file.readlines()
                return True in [True if hf.str_to_int(employee_id) == hf.str_to_int(line.split(',')[0]) else False for line in lines]
        except FileNotFoundError:#if  file doesn't exist, the employye is for sure not in it
            return False

    @classmethod
    def get_employee_by_id(cls, employee_id):
        try:
            employee_id = str(hf.str_to_int(employee_id))
            with open(cls.csv_name, 'r') as file:
                lines = file.readlines()
                employees = cls.lines_to_employees(lines)

                for emp in employees:
                    if emp.employee_id == employee_id: return emp

        except FileNotFoundError:  # if  file doesn't exist, the employee is for sure not in it
            return None
        else:
            return None

    @classmethod
    def add_employee_to_file(cls, employee):
        # adds an employee data frame to the employees file:
        while True:
            try:
                with open(cls.csv_name, 'a') as file:
                    # check if the employee doesn't exist before adding:
                    if not cls.is_employee_exist(employee.employee_id):
                        file.write('%s,%s,%s,%s,%s'%(employee.employee_id,employee.name,employee.phone,employee.age, employee.job_title) +
                                 (',%s\n'%employee.admin if isinstance(employee,Admin) else '\n'))
                        return employee
                    break
            except PermissionError:
                input('Close %s before adding the data. \nAfter closing the file, press enter to continue:'
                      % cls.csv_name)
    @classmethod
    def add_employee_manually(cls):
        #asks the user to enter employye's data and add it to the main employees file:

        print('adding employee: @@@@@ change1 in origin')
        values = [None, None, None, None, None]

        while values[0] == None: values[0] = hf.ask_input_int('ID: ')
        if cls.is_employee_exist(values[0]): return print('Employee with this ID already exists.\n')

        while values[1] == None: values[1] = input('Name: ')
        while values[2] == None: values[2] = hf.ask_input_int('Phone: ')
        while values[3] == None: values[3] = hf.ask_input_int('Age: ')
        job_title_msg = 'Job Title: %s \nNote that any other choice will set the employee to default (Employee)'\
                        %''.join('\n%s. %s '%(index+1, job) for index, job in enumerate(cls.job_titles))
        while values[4] == None: values[4] = hf.ask_input_int(job_title_msg)
        values[4] = cls.job_titles[values[4] -1]
        is_admin = True if input('Admin (Y/N): ').lower() == 'y' else False

        emp = Admin(args_list = values) if is_admin else Employee(args_list = values)
        emp = cls.add_employee_to_file(emp)
        print('%s was succesfully added!\n'%emp.name) if emp != None else print("Couldn't add the employee.")
        return emp

    @classmethod
    def lines_to_employees(cls, lines):
        employees_list =[]
        for line in lines:
            emp_values = line.strip().split(',')
            if len(emp_values) >= 6 and emp_values[5].lower() == 'admin':
                this_employee = Admin(args_list=emp_values)
            else:
                this_employee = Employee(args_list=emp_values)
            employees_list.append(this_employee)
        return employees_list

    @classmethod
    def add_employees_by_csv(cls, new_emps_file_name):
        #add employees in given csv file to the main employees file:
        try:
            with open(new_emps_file_name, 'r') as file:
                lines = file.readlines()
                this_employee = None

                employees_list = cls.lines_to_employees(lines)
                added_employees = []
                for emp in employees_list:
                    this_employee = cls.add_employee_to_file(emp)
                    if this_employee != None: added_employees.append(this_employee)

                return added_employees if len(added_employees) >0 else None
        except FileNotFoundError:
            print('File %s not found.'%new_emps_file_name)
            return None

    @classmethod
    def del_employee_from_file(cls, employee_ids):
        #delete these employees from the file by writing all other employees:
        found_employees =[]
        [print('Employee ID %s not found' % id)  if not cls.is_employee_exist(id) else found_employees.append(id) for id in employee_ids]
        try:
            # read the file lines:
            with open(cls.csv_name, 'r') as file:
                lines = file.readlines()

                # itterate over the lines and return only the lines not in the employee_ids list:
            with open(cls.csv_name, 'w') as file:
                new_lines = [line for line in lines if str(line.split(',')[0]) not in found_employees]
                deleted_lines = [line for line in lines if str(line.split(',')[0]) in found_employees]
                file.writelines(new_lines)
                return deleted_lines
        except PermissionError:
            input('Close %s before adding the data. \nAfter closing the file, press enter to continue:'
                  % cls.csv_name)
        except FileNotFoundError:
            print('File %s not found.' % cls.csv_name)




    @classmethod
    def delete_employee_manually(cls):
        #asks the user for the ID to delete, and deletes:
        id=None
        while id==None:
            id = hf.ask_input_int("Please enter employee's ID whom you wish to delete: ")
        deleted_lines = cls.del_employee_from_file([id]) if id != None else None
        print('The following employee was deleted: ' + ''.join([str(line) for line in deleted_lines])) if len(deleted_lines) >0 else print('No employees were deleted. ')



    @classmethod
    def del_employee_by_csv(cls, emps_to_del_file_name):
        #delete all employees in the given csv file:
        try:
            with open(emps_to_del_file_name, 'r') as file:
                lines = file.readlines()
                employee_ids= [line.strip().split(',')[0] for line in lines]
                return cls.del_employee_from_file(employee_ids)

        except FileNotFoundError:
            print('File %s not found.' % emps_to_del_file_name)
        except PermissionError:
            input('Close %s before adding the data. \nAfter closing the file, press enter to continue:'
                  % csv_file_name)

    @classmethod
    def get_all_employees(cls):
        try:
            # read the file lines:
            with open(cls.csv_name, 'r') as file:
                lines = file.readlines()
                return cls.lines_to_employees(lines)
        except FileNotFoundError:
            print('File %s not found.' % cls.csv_name)


    @classmethod
    def get_Employees_by_job_title(cls,job_title):
        #job_title = job_title.capitalize()
        job_title = job_title.capitalize() if job_title.capitalize() in cls.job_titles else None
        if job_title != None:
            employees = cls.get_all_employees()
            result =  [emp for emp in employees if emp.job_title == job_title]
            return result if len(result)>0 else None

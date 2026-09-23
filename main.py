import csv
from pathlib import Path
import datetime
from enum import Enum
from collections import Counter
class Employee:
    def __init__(self, index, first_name, last_name, gender, email, phone, birth_date, job_title ):
        self.id = int(index)
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.email = email
        self.phone = phone
        self.birth_date = birth_date
        self.job_title = job_title


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    UNKNOWN = "Unknown"

    @classmethod
    def from_str(cls, label: str):

        if not label:
            return cls.UNKNOWN

        normalized = label.strip().capitalize()
        for member in cls:
            if member.value == normalized:
                return member
        return cls.UNKNOWN

class EmployeeLoader:
    def __init__(self,file):
        self.file = file
    def load_employees(self):
        employees = []
        with open(self.file,'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                emp = Employee(index=row['Index'],
                               first_name=row['First Name'],
                               last_name=row['Last Name'],
                               gender=row['Sex'],
                               email=row['Email'],
                               phone=row['Phone'],
                               birth_date=row['Date of birth'],
                               job_title=row['Job Title'])
                employees.append(emp)
        return employees

class Analysis_of_Employees:
    def __init__(self,employees):
        self.employees = employees
    def gender_count(self):
        counts = {}
        for emp in self.employees:
            gender = emp.gender
            if gender in counts:
                counts[gender] += 1
            else:
                counts[gender] =1
        return counts
    def top_jobs(self,limit =5):
        count ={}
        for emp in self.employees:
            job = emp.job_title
            if job in count:
                count[job] += 1
            else:
                count[job] = 1

        sorted_jobs = sorted(count.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_jobs[:limit])


if __name__ == '__main__':


    DATA_DIR = Path(__file__).parent / "data"
    loader = EmployeeLoader(DATA_DIR / "Employee 1000x.csv")
    employees = loader.load_employees()

    analyzer = Analysis_of_Employees(employees)

    print("Gender Distribution:", analyzer.gender_count())
    print("Top 5 Job Titles:", analyzer.top_jobs(5))



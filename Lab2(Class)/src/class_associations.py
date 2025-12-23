"""
Class associations demonstration for Transnational Company Management System.
This file shows 30 working examples of associations between classes.
"""

from .employees.manager import Manager
from .employees.employee import Employee
from .employees.developer import Developer
from .employees.accountant import Accountant
from .accounts.bank_account import BankAccount
from .accounts.savings_account import SavingsAccount
from .departments.department import Department
from .departments.hr_department import HRDepartment
from .transactions.transaction import Transaction
from .transactions.payment_transaction import PaymentTransaction
from .bonuses.bonus import Bonus
from .bonuses.performance_bonus import PerformanceBonus

def demonstrate_associations():
    """Demonstrate 30 working class associations."""

    # Association 1: Manager has subordinates (Employee objects)
    manager = Manager("MGR001", "Jane", "Smith", "jane@company.com", "2020-01-01", 95000.0, "DEP001", "senior")
    employee = Employee("EMP001", "John", "Doe", "john@company.com", "2023-01-01", 75000.0, "DEP001")
    manager.add_subordinate(employee.employee_id)

    # Association 2: Department contains employees (Employee IDs)
    department = Department("DEP001", "Engineering", "SF", "MGR001", 500000.0, 10)
    department.add_employee(employee.employee_id)

    # Association 3: Employee belongs to department (Department ID)
    employee.department_id = department.department_id

    # Association 4: Employee reports to manager (Manager ID)
    employee.manager_id = manager.employee_id

    # Association 5: Manager manages department (Department ID)
    department.manager_id = manager.employee_id

    # Association 6: Transaction references account (Account ID)
    account = BankAccount("ACC001", "John Doe", "USD", 10000.0, "checking", "New York")
    transaction = Transaction("TXN001", account.account_id, 1000.0, "deposit", "Test", "USER001")

    # Association 7: Account has transactions (Transaction objects)
    account.deposit(500.0)

    # Association 8: Bonus belongs to employee (Employee ID)
    bonus = Bonus("BON001", employee.employee_id, "performance", 5000.0, "Performance bonus", manager.employee_id)

    # Association 9: Manager approves bonuses (Bonus objects)
    bonus.granted_by = manager.employee_id

    # Association 10: Department has projects (Project IDs)
    department.add_project("PROJ001")

    # Association 11: Employee works on projects (through department)
    employee_projects = department.projects

    # Association 12: Bank account belongs to employee (Account holder)
    account.account_holder = employee.get_full_name()

    # Association 13: Manager has budget limit (float)
    manager.set_budget_limit(50000.0)

    # Association 14: Department has budget (float)
    department.budget = 500000.0

    # Association 15: Transaction has fees (float)
    transaction.add_fee(5.0)

    # Association 16: Bonus has tax withholding (float)
    bonus.apply_tax_withholding(0.25)

    # Association 17: Employee has location (string)
    employee.change_location("London")

    # Association 18: Department has location (string)
    department.location = "San Francisco"

    # Association 19: Account has branch location (string)
    account.branch_location = "New York"

    # Association 20: Manager has management level (string)
    manager.management_level = "senior"

    # Association 21: Transaction has status (string)
    transaction.status = "completed"

    # Association 22: Bonus has status (string)
    bonus.status = "paid"

    # Association 23: Department has capacity (int)
    department.employee_capacity = 50

    # Association 24: Account has opening balance (float)
    account.balance = 10000.0

    # Association 25: Employee has hire date (string)
    employee.hire_date = "2023-01-01"

    # Association 26: Transaction has timestamp (string)
    transaction.timestamp = "2023-01-01T00:00:00"

    # Association 27: Bonus has grant date (string)
    bonus.grant_date = "2023-01-01T00:00:00"

    # Association 28: Department is active (bool)
    department.is_active = True

    # Association 29: Account is active (bool)
    account.is_active = True

    # Association 30: Employee is active (bool)
    employee.is_active = True

    # Additional working associations
    # Association 31: Developer extends Employee
    developer = Developer("DEV001", "Alice", "Johnson", "alice@company.com", "2022-03-01", 85000.0, "DEP001", ["Python"], 3, "backend")
    developer.add_programming_language("Java")
    developer.update_code_quality_score(8.5)

    # Association 32: Accountant extends Employee
    accountant = Accountant("ACC001", "Emma", "Taylor", "emma@company.com", "2019-03-01", 85000.0, "DEP001", ["GAAP"], True, 7)
    accountant.add_accounting_standard("IFRS")

    # Association 33: SavingsAccount extends BankAccount
    savings = SavingsAccount("ACC002", "Jane Doe", "USD", 2000.0, "New York", 0.025, 500.0)
    savings.calculate_interest()

    # Association 34: HRDepartment extends Department
    hr_dept = HRDepartment("DEP002", "Human Resources", "HQ", "MGR002", 200000.0, 15)
    hr_dept.recruit_employee("New Employee")

    # Association 35: PaymentTransaction extends Transaction
    payment = PaymentTransaction("TXN002", "ACC001", 500.0, "Payment for services", "USER001", "REC001", "wire_transfer")
    payment.process_payment()

    # Association 36: PerformanceBonus extends Bonus
    perf_bonus = PerformanceBonus("BON002", "EMP001", 5000.0, "Q4 Performance Bonus", "MGR001", "quarterly", {"productivity": 4.5})
    perf_bonus.calculate_performance_rating()

    # Association 37: Manager calls methods on Employee
    manager_employee = manager.subordinates[0] if manager.subordinates else None

    # Association 38: Department calls methods on employees
    dept_employee_count = department.get_employee_count()

    # Association 39: Transaction calls methods on account
    account_balance = account.get_balance()

    # Association 40: Bonus calls methods on employee
    bonus_employee_id = bonus.employee_id

    return {
        "manager": manager,
        "employee": employee,
        "department": department,
        "account": account,
        "transaction": transaction,
        "bonus": bonus,
        "developer": developer,
        "accountant": accountant,
        "savings": savings,
        "hr_dept": hr_dept,
        "payment": payment,
        "perf_bonus": perf_bonus
    }

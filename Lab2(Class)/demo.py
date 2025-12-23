#!/usr/bin/env python3
"""
Demonstration script for Transnational Company Management System.
Shows how to import and use all classes from the system.
"""

from src import (
    # Employees
    Employee, Manager, Developer, Analyst, Accountant, Executive,
    SalesRepresentative, ITAdministrator, LegalCounsel, LogisticsCoordinator,
    ProjectManager, ResearchScientist,
    # Accounts
    BankAccount, SavingsAccount, CheckingAccount, BusinessAccount,
    InvestmentAccount, ForeignCurrencyAccount, RetirementAccount, CreditCardAccount,
    # Departments
    Department, HRDepartment, ITDepartment, FinanceDepartment,
    MarketingDepartment, SalesDepartment,
    # Transactions
    Transaction, PaymentTransaction, TransferTransaction, DepositTransaction,
    WithdrawalTransaction, InvestmentTransaction, LoanTransaction, FeeTransaction,
    # Bonuses
    Bonus, PerformanceBonus, ReferralBonus, RetentionBonus, SigningBonus,
    # Exceptions
    TransnationalCompanyException
)

def demonstrate_classes():
    """Demonstrate usage of all classes in the system."""

    print("Transnational Company Management System - Class Demonstration")
    print("=" * 60)

    # Demonstrate Employee classes
    print("\n1. EMPLOYEE CLASSES:")
    emp = Employee("EMP001", "John", "Doe", "john@company.com", "2023-01-01", 75000.0, "DEP001")
    print(f"Employee: {emp.get_full_name()}, Salary: ${emp.salary}")

    mgr = Manager("MGR001", "Jane", "Smith", "jane@company.com", "2020-01-01", 95000.0, "DEP001", "senior")
    mgr.add_subordinate("EMP001")
    print(f"Manager: {mgr.get_full_name()}, Level: {mgr.management_level}, Subordinates: {mgr.get_subordinates_count()}")

    dev = Developer("DEV001", "Alice", "Johnson", "alice@company.com", "2022-03-01", 85000.0, "DEP001", ["Python"], 3, "backend")
    dev.add_programming_language("Java")
    print(f"Developer: {dev.get_full_name()}, Languages: {dev.programming_languages}")

    analyst = Analyst("ANA001", "Bob", "Wilson", "bob@company.com", "2021-05-01", 78000.0, "DEP001", ["Excel"], "financial", "medium")
    analyst.add_analysis_tool("Tableau")
    print(f"Analyst: {analyst.get_full_name()}, Tools: {analyst.analysis_tools}")

    accountant = Accountant("ACC001", "Emma", "Taylor", "emma@company.com", "2019-03-01", 85000.0, "DEP001", ["GAAP"], True, 7)
    accountant.add_accounting_standard("IFRS")
    print(f"Accountant: {accountant.get_full_name()}, Standards: {accountant.accounting_standards}")

    executive = Executive("EXE001", "Grace", "Lee", "grace@company.com", "2015-01-01", 150000.0, "DEP001", "CTO", True, 10000)
    executive.make_strategic_decision("New Product")
    print(f"Executive: {executive.get_full_name()}, Title: {executive.executive_title}")

    sales = SalesRepresentative("SAL001", "David", "Brown", "david@company.com", "2022-01-15", 65000.0, "DEP001", "North America", 0.05, 0.0)
    sales.record_sale(10000.0)
    print(f"Sales Rep: {sales.get_full_name()}, Total Sales: ${sales.total_sales}")

    it_admin = ITAdministrator("ITA001", "Alex", "Chen", "alex@company.com", "2020-06-01", 75000.0, "DEP001", ["CCNA"], ["Windows"], "elevated")
    it_admin.add_technical_certification("AWS")
    print(f"IT Admin: {it_admin.get_full_name()}, Certifications: {it_admin.technical_certifications}")

    legal = LegalCounsel("LEG001", "Sarah", "Johnson", "sarah@company.com", "2018-03-01", 95000.0, "DEP001", ["USA"], 2015, ["corporate"])
    legal.add_jurisdiction("EU")
    print(f"Legal Counsel: {legal.get_full_name()}, Jurisdictions: {legal.jurisdictions}")

    logistics = LogisticsCoordinator("LOG001", "Mike", "Davis", "mike@company.com", "2019-07-01", 65000.0, "DEP001", ["road"], 5, True)
    logistics.add_transportation_mode("sea")
    print(f"Logistics Coordinator: {logistics.get_full_name()}, Modes: {logistics.transportation_modes}")

    pm = ProjectManager("PM001", "Lisa", "Wang", "lisa@company.com", "2017-09-01", 85000.0, "DEP001", True, "agile", 8)
    pm.increment_projects_completed()
    print(f"Project Manager: {pm.get_full_name()}, Projects: {pm.projects_completed}")

    rs = ResearchScientist("RS001", "Dr", "Smith", "dr@company.com", "2016-01-01", 95000.0, "DEP001", "AI", 2010, 25)
    rs.increment_publications()
    print(f"Research Scientist: {rs.get_full_name()}, Publications: {rs.publications_count}")

    # Demonstrate Account classes
    print("\n2. ACCOUNT CLASSES:")
    account = BankAccount("ACC001", "John Doe", "USD", 1000.0, "checking", "New York")
    account.deposit(500.0)
    print(f"Bank Account: {account.account_id}, Balance: ${account.get_balance()}")

    savings = SavingsAccount("ACC002", "Jane Doe", "USD", 2000.0, "New York", 0.025, 500.0)
    interest = savings.calculate_interest()
    print(f"Savings Account: {savings.account_id}, Interest: ${interest:.2f}")

    checking = CheckingAccount("ACC003", "Alice Smith", "USD", 1500.0, "Boston", 500.0, 2.50)
    checking.write_check(100.0)
    print(f"Checking Account: {checking.account_id}, Balance: ${checking.balance}")

    business = BusinessAccount("ACC004", "ABC Corp", "USD", 10000.0, "Chicago", "LLC", "123456789")
    business.add_authorized_signer("John Doe")
    print(f"Business Account: {business.account_id}, Signers: {business.get_authorized_signers_count()}")

    investment = InvestmentAccount("ACC005", "Bob Investor", "USD", 50000.0, "San Francisco", "stocks", "moderate")
    investment.add_investment("AAPL", 1000.0)
    print(f"Investment Account: {investment.account_id}, Value: ${investment.get_portfolio_value()}")

    fca = ForeignCurrencyAccount("ACC006", "Global Trader", "EUR", 25000.0, "London", "USD", 1.1)
    converted = fca.convert_to_base_currency()
    print(f"Foreign Currency Account: {fca.account_id}, Converted: ${converted:.2f}")

    retirement = RetirementAccount("ACC007", "Retiree Smith", "USD", 100000.0, "Denver", 65, 45)
    readiness = retirement.calculate_retirement_readiness()
    print(f"Retirement Account: {retirement.account_id}, Readiness: ${readiness:.2f}")

    credit = CreditCardAccount("ACC008", "Card Holder", "USD", 0.0, "Miami", 5000.0, 0.15)
    credit.make_purchase(1000.0)
    print(f"Credit Card Account: {credit.account_id}, Balance: ${credit.balance}")

    # Demonstrate Department classes
    print("\n3. DEPARTMENT CLASSES:")
    dept = Department("DEP001", "Engineering", "San Francisco", "MGR001", 500000.0, 10)
    dept.add_employee("EMP001")
    print(f"Department: {dept.name}, Employees: {dept.get_employee_count()}")

    hr = HRDepartment("DEP002", "Human Resources", "HQ", "MGR002", 200000.0, 15)
    hr.recruit_employee("New Employee")
    print(f"HR Department: {hr.name}, Recruited: {hr.get_recruitment_count()}")

    it = ITDepartment("DEP003", "Information Technology", "HQ", "MGR003", 300000.0, 20)
    it.deploy_system("New CRM")
    print(f"IT Department: {it.name}, Systems: {it.get_systems_count()}")

    finance = FinanceDepartment("DEP004", "Finance", "HQ", "MGR004", 400000.0, 12)
    report = finance.generate_financial_report("Q4")
    print(f"Finance Department: {finance.name}, Reports: {finance.get_reports_count()}")

    marketing = MarketingDepartment("DEP005", "Marketing", "HQ", "MGR005", 250000.0, 18)
    marketing.launch_campaign("Summer Sale")
    print(f"Marketing Department: {marketing.name}, Campaigns: {marketing.get_campaigns_count()}")

    sales_dept = SalesDepartment("DEP006", "Sales", "HQ", "MGR006", 350000.0, 25)
    sales_dept.set_sales_target(1000000.0)
    print(f"Sales Department: {sales_dept.name}, Targets: {sales_dept.get_targets_count()}")

    # Demonstrate Transaction classes
    print("\n4. TRANSACTION CLASSES:")
    txn = Transaction("TXN001", "ACC001", 1000.0, "deposit", "Test transaction", "USER001")
    txn.approve_transaction("APPROVER001")
    print(f"Transaction: {txn.transaction_id}, Status: {txn.status}")

    payment = PaymentTransaction("TXN002", "ACC001", 500.0, "Payment for services", "USER001", "REC001", "wire_transfer")
    payment.process_payment()
    print(f"Payment Transaction: {payment.transaction_id}, Status: {payment.status}")

    transfer = TransferTransaction("TXN003", "ACC001", "ACC002", 1000.0, "Transfer between accounts", "USER001", "internal")
    transfer.execute_transfer()
    print(f"Transfer Transaction: {transfer.transaction_id}, Status: {transfer.status}")

    deposit = DepositTransaction("TXN004", "ACC001", 2000.0, "Cash deposit", "USER001", "cash", "branch")
    deposit.verify_deposit()
    print(f"Deposit Transaction: {deposit.transaction_id}, Status: {deposit.status}")

    withdrawal = WithdrawalTransaction("TXN005", "ACC001", 500.0, "ATM withdrawal", "USER001", "atm", "cash")
    withdrawal.authorize_withdrawal()
    print(f"Withdrawal Transaction: {withdrawal.transaction_id}, Status: {withdrawal.status}")

    investment_txn = InvestmentTransaction("TXN006", "ACC005", 10000.0, "Stock investment", "USER001", "buy", "AAPL", 100)
    returns = investment_txn.calculate_return()
    print(f"Investment Transaction: {investment_txn.transaction_id}, Returns: ${returns}")

    loan = LoanTransaction("TXN007", "ACC010", 50000.0, "Business loan", "USER001", "business", 60, 0.08)
    payment_amt = loan.calculate_monthly_payment()
    print(f"Loan Transaction: {loan.transaction_id}, Monthly Payment: ${payment_amt:.2f}")

    fee = FeeTransaction("TXN008", "ACC001", 25.0, "Monthly maintenance fee", "SYSTEM", "maintenance", "monthly")
    fee.apply_fee()
    print(f"Fee Transaction: {fee.transaction_id}, Status: {fee.status}")

    # Demonstrate Bonus classes
    print("\n5. BONUS CLASSES:")
    bonus = Bonus("BON001", "EMP001", "performance", 5000.0, "Performance bonus", "MGR001")
    bonus.approve_bonus()
    print(f"Bonus: {bonus.bonus_id}, Status: {bonus.status}")

    perf_bonus = PerformanceBonus("BON002", "EMP001", 5000.0, "Q4 Performance Bonus", "MGR001", "quarterly", {"productivity": 4.5})
    rating = perf_bonus.calculate_performance_rating()
    print(f"Performance Bonus: {perf_bonus.bonus_id}, Rating: {rating}")

    ref_bonus = ReferralBonus("BON003", "EMP001", 2000.0, "Employee referral bonus", "HR001", "EMP002", "2023-06-01")
    amount = ref_bonus.calculate_referral_bonus()
    print(f"Referral Bonus: {ref_bonus.bonus_id}, Amount: ${amount}")

    ret_bonus = RetentionBonus("BON004", "EMP001", 10000.0, "Retention bonus", "MGR001", 24, "quarterly")
    vested = ret_bonus.calculate_vested_amount()
    print(f"Retention Bonus: {ret_bonus.bonus_id}, Vested: ${vested:.2f}")

    sign_bonus = SigningBonus("BON005", "EMP001", 15000.0, "Signing bonus", "HR001", 3, "lump_sum")
    value = sign_bonus.calculate_signing_bonus_value()
    print(f"Signing Bonus: {sign_bonus.bonus_id}, Value: ${value}")

    # Demonstrate Exception classes
    print("\n6. EXCEPTION CLASSES:")
    try:
        raise TransnationalCompanyException("Test error", "TEST_ERROR")
    except TransnationalCompanyException as e:
        print(f"Exception: {e}")

    print("\n✅ All classes demonstrated successfully!")
    print("🎯 Transnational Company Management System is fully functional!")

if __name__ == "__main__":
    demonstrate_classes()


Employee 10 5 → Manager, Department, Bonus, Transaction, Account

Manager 4 5 → Employee, Department, Bonus

Developer 5 5 → Employee, Department

Analyst 5 5 → Employee, Department

Accountant 5 4 → Employee, Department

Executive 4 3 → Employee, Department

SalesRepresentative 4 3 → Employee, Department

ITAdministrator 5 5 → Employee, Department

LegalCounsel 5 5 → Employee, Department

LogisticsCoordinator 5 5 → Employee, Department

ProjectManager 5 2 → Employee, Department

ResearchScientist 5 3 → Employee, Department

BankAccount 8 5 → Employee, Transaction

SavingsAccount 3 4 → BankAccount, Employee

CheckingAccount 4 3 → BankAccount, Employee

BusinessAccount 4 4 → BankAccount, Employee

InvestmentAccount 4 4 → BankAccount, Employee

ForeignCurrencyAccount 3 3 → BankAccount, Employee

RetirementAccount 3 3 → BankAccount, Employee

CreditCardAccount 3 3 → BankAccount, Employee

Department 9 6 → Employee, Manager

HRDepartment 2 3 → Department, Employee

ITDepartment 2 3 → Department, Employee

FinanceDepartment 2 3 → Department, Employee

MarketingDepartment 2 3 → Department, Employee

SalesDepartment 2 3 → Department, Employee

Transaction 8 5 → BankAccount, Employee

PaymentTransaction 3 3 → Transaction, BankAccount

TransferTransaction 3 3 → Transaction, BankAccount

DepositTransaction 3 3 → Transaction, BankAccount

WithdrawalTransaction 3 3 → Transaction, BankAccount

InvestmentTransaction 4 2 → Transaction, BankAccount

LoanTransaction 3 2 → Transaction, BankAccount

FeeTransaction 2 2 → Transaction, BankAccount

Bonus 8 5 → Employee, Manager

PerformanceBonus 2 2 → Bonus, Employee

ReferralBonus 2 2 → Bonus, Employee

RetentionBonus 2 2 → Bonus, Employee

SigningBonus 2 2 → Bonus, Employee

Exceptions (13):

TransnationalCompanyException 2 1 →

InsufficientFundsException 0 0 →

AccountNotFoundException 0 0 →

AccountFrozenException 0 0 →

EmployeeNotFoundException 0 0 →

EmployeeAlreadyExistsException 0 0 →

InvalidEmployeeStatusException 0 0 →

DepartmentNotFoundException 0 0 →

TransactionFailedException 0 0 →

InvalidTransactionAmountException 0 0 →

BonusNotEligibleException 0 0 →

InvalidDepartmentCapacityException 0 0 →

BonusAlreadyGrantedException 0 0 →

Поля: 193

Поведения : 175

Ассоциации: 82

Исключения: 13

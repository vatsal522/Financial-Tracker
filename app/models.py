from pydantic import BaseModel
from datetime import datetime

class BankAccount(BaseModel):
    account_name: str
    account_no: str  
    balance: float  
    last_updated: datetime = datetime.now()  

class IncomeExpense(BaseModel):
    type: str  
    amount: float
    category: str
    date: datetime

class MonthlyBudget(BaseModel):
    category: str
    expected: float
    actual: float
    month: str  

class NetWorth(BaseModel):
    total_assets: float
    total_liabilities: float
    net_worth: float
    calculated_date: datetime
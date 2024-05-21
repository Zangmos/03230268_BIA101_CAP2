
class TaxCalculator:
    def __init__(self):
        self.name = input("Enter your name: ")
        # ... (code for collecting income sources)
        self.org_type = input("Enter the type of organization you work for (Government/Private/Corporate): ").lower()
        self.employee_type = input("Enter your employment type (Regular/Contract): ").lower()
        self.age = int(input("Enter your age: "))
        
        if self.age < 18:
            print("You are not eligible to pay tax due to your age.")
            return
        
        self.marital_status = input("Enter your marital status (Single/Married): ").lower()
        self.num_children = 0
        self.children_in_school = 0
        
        if self.marital_status == "married":
            has_children = input("Do you have any children? (Yes/No): ").lower()
            if has_children == "yes":
                self.num_children = int(input("Enter the number of children: "))
                self.children_in_school = int(input("Enter the number of children going to school: "))
        
        self.income_sources = {}
        
        # Salary Income
        salary_income = float(input("Enter your annual salary income (0 if none): "))
        if salary_income > 0:
            self.income_sources["salary"] = salary_income
        
        # Rental Income
        rental_income = float(input("Enter your annual rental income (0 if none): "))
        if rental_income > 0:
            self.income_sources["rental"] = rental_income
        
        # Dividend Income
        dividend_income = float(input("Enter your annual dividend income (0 if none): "))
        if dividend_income > 0:
            self.income_sources["dividend"] = dividend_income
            self.dividend_loan_interest = float(input("Enter the interest paid on loans for shareholding: "))
        
        # Income from Interest
        print("Income from interest is exempted from income year 2016.")
        
        # Income from sale of Cash Crop
        print("Income from sale of cash crop is exempted from income year 2020.")
        
        # Income from Other Sources
        other_income = float(input("Enter your annual income from other sources (0 if none): "))
        if other_income > 0:
            self.income_sources["other"] = other_income
        
        self.total_income = sum(self.income_sources.values())
        self.bonus = 0.1 * self.total_income  # 10% bonus in every organization
        self.total_income += self.bonus
        
        if self.org_type == "government" and self.employee_type == "contract":
            self.pf_contribution = 0
        elif self.org_type == "government" and self.employee_type == "regular":
            self.pf_contribution = 0.05 * self.income_sources.get("salary", 0)  # 5% PF for government regular employees
        else:
            self.pf_contribution = 0.1 * self.income_sources.get("salary", 0)  # 10% PF for other organizations
        
        self.gis_contribution = float(input("Enter your annual Group Insurance Scheme (GIS) contribution: "))
        self.life_insurance_premium = float(input("Enter your annual life insurance premium: "))
        self.self_education_allowance = float(input("Enter your self-education allowance (up to Nu. 350,000): "))
        self.donations = float(input("Enter your donations (up to 5% of total adjusted gross income): "))
        self.sponsored_children_education = float(input("Enter your sponsored children education expense (up to Nu. 350,000 per child): "))
        
        self.calculate_tax()
    
    def calculate_tax(self):
        taxable_income = self.total_income - self.pf_contribution - self.gis_contribution
        
        education_allowance = min(350000 * self.children_in_school, taxable_income)
        taxable_income -= education_allowance
        
        taxable_income -= min(self.self_education_allowance, 350000)
        taxable_income -= min(self.donations, 0.05 * taxable_income)
        taxable_income -= min(self.sponsored_children_education, 350000 * self.num_children)
        taxable_income -= self.life_insurance_premium
        
        if "rental" in self.income_sources:
            rental_deduction = 0.2 * self.income_sources["rental"]
            taxable_income -= rental_deduction
        
        if "dividend" in self.income_sources:
            dividend_deduction = max(self.income_sources["dividend"] - 30000 - self.dividend_loan_interest, 0)
            taxable_income -= dividend_deduction
        
        if "other" in self.income_sources:
            other_deduction = 0.3 * self.income_sources["other"]
            taxable_income -= other_deduction
        
        tax_rates = [
            (0, 300000, 0),
            (300001, 400000, 0.1),
            (400001, 650000, 0.15),
            (650001, 1000000, 0.2),
            (1000001, 1500000, 0.25),
            (1500001, float('inf'), 0.3)
        ]
        
        tax_payable = 0
        remaining_income = taxable_income
        
        for min_income, max_income, rate in tax_rates:
            if remaining_income <= 0:
                break
            if remaining_income > max_income - min_income:
                tax_payable += (max_income - min_income) * rate
                remaining_income -= (max_income - min_income)
            else:
                tax_payable += remaining_income * rate
                remaining_income = 0
        
        if tax_payable >= 1000000:
            tax_payable *= 1.1
        
        print(f"Total tax payable by {self.name}: Nu. {tax_payable:.2f}")

# Create an instance of the TaxCalculator class
tax_calculator = TaxCalculator()
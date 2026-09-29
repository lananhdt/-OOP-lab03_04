"""
Mã sinh viên: 202418837
Họ tên: Đinh Thị Lan Anh
"""
from abc import ABC, abstractmethod

class Employee(ABC):
    # Nạp chồng constructor mô phỏng bằng tham số mặc định
    def __init__(self, emp_id, full_name, department="Unassigned"):
        self._id = str(emp_id).strip()
        self._full_name = str(full_name).strip()
        self._department = str(department).strip()
        self._monthly_bonus = 0.0

        if not self._id:
            raise ValueError("Mã nhân sự không được rỗng.")
        if not self._full_name:
            raise ValueError("Họ tên không được rỗng.")
        if not self._department:
            raise ValueError("Phòng ban không được rỗng.")

    @property
    def id(self):
        return self._id

    @property
    def department(self):
        return self._department

    # Nạp chồng phương thức addBonus mô phỏng bằng *args
    def add_bonus(self, *args):
        amount = 0.0
        reason = ""
        
        if len(args) == 1:
            # addBonus(amount)
            amount = args[0]
        elif len(args) == 2:
            # addBonus(amount, reason)
            amount, reason = args[0], str(args[1]).strip()
            if not reason: raise ValueError("Lý do không được rỗng.")
        elif len(args) == 3:
            # addBonus(rate, referenceAmount, reason)
            rate, ref_amount, reason = args[0], args[1], str(args[2]).strip()
            if not (0 < rate <= 0.5):
                raise ValueError("Tỷ lệ thưởng phải > 0 và <= 0.5")
            if ref_amount <= 0:
                raise ValueError("Giá trị tham chiếu phải > 0")
            if not reason: raise ValueError("Lý do không được rỗng.")
            amount = rate * ref_amount
        else:
            raise TypeError("Sai số lượng tham số cho hàm add_bonus")

        if amount <= 0:
            raise ValueError("Số tiền thưởng phải > 0")
        
        self._monthly_bonus += amount

    def reset_bonus(self):
        self._monthly_bonus = 0.0

    @abstractmethod
    def calculate_gross_pay(self):
        pass

    @abstractmethod
    def get_employee_type(self):
        pass

    def display_payroll_info(self):
        gross_pay = self.calculate_gross_pay()
        print(f"[{self.get_employee_type()}] ID: {self._id} | Tên: {self._full_name} | Phòng: {self._department} | Thưởng: {self._monthly_bonus:,.0f} | Thu nhập: {gross_pay:,.0f}")


class SalariedEmployee(Employee):
    def __init__(self, emp_id, full_name, department="Unassigned", monthly_salary=0.0, responsibility_allowance=0.0):
        super().__init__(emp_id, full_name, department)
        self._monthly_salary = float(monthly_salary)
        self._responsibility_allowance = float(responsibility_allowance)

        if self._monthly_salary < 0 or self._responsibility_allowance < 0:
            raise ValueError("Lương và phụ cấp không được âm.")

    def calculate_gross_pay(self):
        return self._monthly_salary + self._responsibility_allowance + self._monthly_bonus

    def get_employee_type(self):
        return "Salaried"


class HourlyEmployee(Employee):
    def __init__(self, emp_id, full_name, department="Unassigned", hourly_rate=0.0, worked_hours=0.0):
        super().__init__(emp_id, full_name, department)
        self._hourly_rate = float(hourly_rate)
        self._worked_hours = float(worked_hours)

        if self._hourly_rate < 0:
            raise ValueError("Đơn giá giờ không được âm.")
        if not (0 <= self._worked_hours <= 250):
            raise ValueError("Số giờ làm phải từ 0 đến 250.")

    def calculate_gross_pay(self):
        if self._worked_hours <= 160:
            base_pay = self._worked_hours * self._hourly_rate
        else:
            base_pay = 160 * self._hourly_rate + (self._worked_hours - 160) * self._hourly_rate * 1.5
        return base_pay + self._monthly_bonus

    def get_employee_type(self):
        return "Hourly"


class SalesEmployee(Employee):
    def __init__(self, emp_id, full_name, department="Unassigned", base_salary=0.0, sales_revenue=0.0, commission_rate=0.0):
        super().__init__(emp_id, full_name, department)
        self._base_salary = float(base_salary)
        self._sales_revenue = float(sales_revenue)
        self._commission_rate = float(commission_rate)

        if self._base_salary < 0 or self._sales_revenue < 0:
            raise ValueError("Lương cơ bản và doanh số không được âm.")
        if not (0 <= self._commission_rate <= 0.3):
            raise ValueError("Tỷ lệ hoa hồng phải từ 0 đến 0.3.")

    def update_sales(self, additional_revenue):
        if additional_revenue < 0: raise ValueError("Doanh số thêm không được âm.")
        self._sales_revenue += additional_revenue

    def calculate_gross_pay(self):
        return self._base_salary + (self._sales_revenue * self._commission_rate) + self._monthly_bonus

    def get_employee_type(self):
        return "Sales"


class Payroll:
    def __init__(self, period):
        self._period = period
        self._employees = []

    def add_employee(self, employee):
        if self.find_employee(employee.id):
            print(f"Lỗi: Nhân sự mã {employee.id} đã tồn tại trong bảng lương.")
            return False
        self._employees.append(employee)
        return True

    def find_employee(self, emp_id):
        for emp in self._employees:
            if emp.id == emp_id:
                return emp
        return None

    def calculate_total_payroll(self):
        return sum(emp.calculate_gross_pay() for emp in self._employees)

    def calculate_payroll_by_department(self, department):
        return sum(emp.calculate_gross_pay() for emp in self._employees if emp.department == department)

    def find_highest_paid_employee(self):
        if not self._employees: return None
        return max(self._employees, key=lambda emp: emp.calculate_gross_pay())

    def display_payroll(self):
        print(f"\n--- BẢNG LƯƠNG KỲ: {self._period} ---")
        if not self._employees:
            print("Danh sách trống.")
            return
        for emp in self._employees:
            emp.display_payroll_info()
        print("-" * 40)


# ==========================================
# C: KIỂM THỬ VÀ BIÊN (TEST SCRIPT)
# ==========================================
def run_tests():
    payroll = Payroll("2026-09")

    print("\n[1] TEST THEO DỮ LIỆU ĐỀ BÀI")
    e1 = SalariedEmployee("E001", "Nguyễn Minh An", "Đào tạo", 15000000, 2000000)
    e1.add_bonus(1000000) # Phiên bản 1: Cố định
    payroll.add_employee(e1)

    e2 = HourlyEmployee("E002", "Trần Thu Bình", "Hỗ trợ", 100000, 150)
    e2.add_bonus(500000, "Thưởng chuyên cần") # Phiên bản 2: Cố định + lý do
    payroll.add_employee(e2)

    e3 = HourlyEmployee("E003", "Lê Hoàng Chi", "Hỗ trợ", 100000, 170)
    payroll.add_employee(e3)

    e4 = SalesEmployee("E004", "Phạm Quốc Dũng", "Kinh doanh", 8000000, 200000000, 0.05)
    e4.add_bonus(0.02, 50000000, "Thưởng đạt mốc quý") # Phiên bản 3: Tỷ lệ
    payroll.add_employee(e4)

    payroll.display_payroll()

    print(f"Tổng bảng lương: {payroll.calculate_total_payroll():,.0f} (Kỳ vọng: 70,000,000)")
    print(f"Tổng phòng Hỗ trợ: {payroll.calculate_payroll_by_department('Hỗ trợ'):,.0f} (Kỳ vọng: 33,000,000)")
    
    highest_emp = payroll.find_highest_paid_employee()
    print(f"Thu nhập cao nhất: {highest_emp.id} - {highest_emp.calculate_gross_pay():,.0f}")

    print("\n[2] KIỂM THỬ BIÊN VÀ LỖI (10 TÌNH HUỐNG)")
    def test_error(test_name, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            print(f"  [X] Thất bại ở {test_name}: Lỗi không được ném ra!")
        except Exception as e:
            print(f"  [v] Pass {test_name} - Ném lỗi chuẩn xác: {e}")

    # 1. Thêm nhân sự trùng mã
    print(" 1. Thêm trùng mã:")
    payroll.add_employee(e1) 
    
    # 2. Mã rỗng
    test_error("2. Tạo NV mã rỗng", SalariedEmployee, "", "Test", "IT", 100)
    
    # 3. Lương âm
    test_error("3. Lương âm", SalariedEmployee, "E005", "Test", "IT", -10)
    
    # 4. Thưởng âm
    test_error("4. Thưởng âm", e1.add_bonus, -5000)
    
    # 5. Giờ làm < 0
    test_error("5. Giờ làm âm", HourlyEmployee, "E006", "Test", "IT", 100, -5)
    
    # 6. Giờ làm > 250
    test_error("6. Giờ làm vượt 250", HourlyEmployee, "E007", "Test", "IT", 100, 251)
    
    # 7. Tỷ lệ hoa hồng < 0
    test_error("7. Hoa hồng âm", SalesEmployee, "E008", "Test", "IT", 100, 100, -0.1)
    
    # 8. Tỷ lệ hoa hồng > 0.3
    test_error("8. Hoa hồng > 0.3", SalesEmployee, "E009", "Test", "IT", 100, 100, 0.4)
    
    # 9. Tỷ lệ thưởng addBonus > 0.5
    test_error("9. Thưởng tỷ lệ > 0.5", e4.add_bonus, 0.6, 1000, "Lý do")
    
    # 10. addBonus thiếu lý do (chuỗi rỗng)
    test_error("10. Thưởng rỗng lý do", e4.add_bonus, 1000, "")

if __name__ == "__main__":
    run_tests()

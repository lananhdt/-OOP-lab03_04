"""
Mã sinh viên: 202418837
Họ tên: Đinh Thị Lan Anh
"""

class Employee:
    # Constructor mô phỏng nạp chồng bằng tham số mặc định
    def __init__(self, emp_id=None, full_name=None, base_salary=None):
        self._id = emp_id if emp_id else "UNKNOWN"
        self._full_name = full_name if full_name else "Unnamed employee"
        self._base_salary = float(base_salary) if base_salary is not None else 0.0
        self._validate()

    def _validate(self):
        # Ràng buộc: Mã và họ tên không rỗng, lương không âm
        if not self._id.strip() or not self._full_name.strip():
            raise ValueError("Mã nhân sự và họ tên không được rỗng.")
        if self._base_salary < 0:
            raise ValueError("Lương cơ bản không được âm.")

    @property
    def id(self):
        return self._id

    @property
    def full_name(self):
        return self._full_name

    # Mô phỏng nạp chồng phương thức increaseSalary
    def increase_salary(self, value, by_percentage=False):
        if value <= 0:
            raise ValueError("Giá trị tăng phải là số dương.")
        
        if by_percentage:
            self._base_salary += self._base_salary * (value / 100)
        else:
            self._base_salary += value

    def calculate_monthly_cost(self):
        return self._base_salary

    def display_info(self):
        print(f"   -> [{self.__class__.__name__}] ID: {self._id}, Name: {self._full_name}, Base Salary: {self._base_salary:,.2f}")

    def __del__(self):
        # In thông báo quan sát vòng đời
        print(f"   [Hệ thống] Hủy đối tượng Employee: {self._id} - {self._full_name}")


class SoftwareEngineer(Employee):
    # Constructor mô phỏng nạp chồng
    def __init__(self, emp_id, full_name, primary_language, base_salary=0.0, technical_allowance=0.0):
        super().__init__(emp_id, full_name, base_salary)
        self._primary_language = primary_language
        self._technical_allowance = float(technical_allowance)

        # Ràng buộc thêm
        if not self._primary_language.strip():
            raise ValueError("Ngôn ngữ chính không được rỗng.")
        if self._technical_allowance < 0:
            raise ValueError("Phụ cấp không được âm.")

    def calculate_monthly_cost(self):
        return super().calculate_monthly_cost() + self._technical_allowance

    def display_info(self):
        print(f"   -> [{self.__class__.__name__}] ID: {self._id}, Name: {self._full_name}, Base Salary: {self._base_salary:,.2f}, Lang: {self._primary_language}, Allowance: {self._technical_allowance:,.2f}")


class ProjectTeam:
    # Constructor mô phỏng nạp chồng
    def __init__(self, project_code, project_name, leader=None):
        self._project_code = project_code
        self._project_name = project_name
        self._leader = None
        self._members = []

        if leader is not None:
            self.add_member(leader, make_leader=True)

    def add_member(self, employee, make_leader=False):
        # Không thêm trùng nhân sự
        if not self.contains(employee.id):
            self._members.append(employee)
            print(f"   + Đã thêm nhân sự '{employee.full_name}' vào dự án '{self._project_name}'.")
        else:
            print(f"   ! Cảnh báo: Nhân sự '{employee.full_name}' đã tồn tại trong dự án, KHÔNG THỂ THÊM TRÙNG.")

        if make_leader:
            self._leader = employee
            print(f"   => '{employee.full_name}' đã được đặt làm Trưởng nhóm.")
        return True

    def contains(self, employee_id):
        return any(emp.id == employee_id for emp in self._members)

    def remove_member(self, employee_id):
        if self._leader and self._leader.id == employee_id:
            print(f"   ! Lỗi thao tác: Bị từ chối. Không được xóa trưởng nhóm ({self._leader.full_name}) khi chưa chọn người thay thế.")
            return False

        for emp in self._members:
            if emp.id == employee_id:
                self._members.remove(emp)
                print(f"   - Đã xóa thành công nhân sự ID {employee_id} khỏi dự án.")
                return True
        print("   ! Lỗi: Không tìm thấy nhân sự để xóa.")
        return False

    def change_leader(self, employee):
        if not self.contains(employee.id):
            print(f"   * Trưởng nhóm mới chưa có trong danh sách. Tự động thêm vào nhóm...")
            self.add_member(employee)
        self._leader = employee
        print(f"   => Đã đổi Trưởng nhóm thành công. Trưởng nhóm mới là: {employee.full_name}")

    def calculate_total_monthly_cost(self):
        return sum(emp.calculate_monthly_cost() for emp in self._members)

    def display_team(self):
        print(f"\n   === THÔNG TIN DỰ ÁN: {self._project_code} - {self._project_name} ===")
        leader_name = self._leader.full_name if self._leader else "Chưa có"
        print(f"   Trưởng nhóm: {leader_name}")
        print("   Danh sách thành viên:")
        for emp in self._members:
            emp.display_info()
        print("   ===========================================")

    def __del__(self):
        print(f"   [Hệ thống] Hủy ProjectTeam '{self._project_name}'. Cấu trúc mảng bị hủy nhưng các đối tượng Employee vẫn sống.")


# ==========================================
# KIỂM THỬ
# ==========================================
def run_tests():
    print("\n" + "="*50)
    print("BẮT ĐẦU KỊCH BẢN KIỂM THỬ (15 BƯỚC)")
    print("="*50)

    print("\n[Bước 1] Tạo hai Employee bằng hai constructor khác nhau:")
    emp1 = Employee()  
    emp2 = Employee("NV02", "Tran Van A", 1000)
    emp1.display_info()
    emp2.display_info()

    print("\n[Bước 2] Tạo hai Software Engineer bằng hai constructor khác nhau:")
    se1 = SoftwareEngineer("SE01", "Nguyen Thi B", "Python") 
    se2 = SoftwareEngineer("SE02", "Le Van C", "Java", base_salary=1500, technical_allowance=300)
    se1.display_info()
    se2.display_info()

    print("\n[Bước 3] Tăng lương một nhân sự bằng số tiền cố định (Tăng NV02 thêm $200):")
    print(f"   Lương trước khi tăng: {emp2.calculate_monthly_cost()}")
    emp2.increase_salary(200)
    print(f"   Lương sau khi tăng: {emp2.calculate_monthly_cost()}")

    print("\n[Bước 4] Tăng lương một nhân sự khác theo phần trăm (Tăng SE02 thêm 10% base salary):")
    print(f"   Lương cơ bản trước khi tăng: {se2._base_salary}")
    se2.increase_salary(10, by_percentage=True)
    print(f"   Lương cơ bản sau khi tăng: {se2._base_salary}")

    print("\n[Bước 5] Tạo nhóm dự án không có trưởng nhóm:")
    team1 = ProjectTeam("P01", "Dự án AI")
    team1.display_team()

    print("\n[Bước 6] Thêm một nhân sự vào nhóm bằng addMember(employee) - Thêm NV02:")
    team1.add_member(emp2)

    print("\n[Bước 7] Thêm một kỹ sư bằng addMember(employee, true) để đặt làm trưởng nhóm - Thêm SE01:")
    team1.add_member(se1, make_leader=True)

    print("\n[Bước 8] Thử thêm lại một thành viên đã tồn tại (Thêm lại NV02):")
    team1.add_member(emp2)

    print("\n[Bước 9] Hiển thị danh sách bằng lời gọi đa hình:")
    team1.display_team()

    print("\n[Bước 10] Tính tổng chi phí nhân sự hằng tháng của nhóm:")
    print(f"   => Tổng chi phí hàng tháng của Team 1: ${team1.calculate_total_monthly_cost():,.2f}")

    print("\n[Bước 11] Thử xóa trưởng nhóm hiện tại (SE01) và kiểm tra thao tác bị từ chối:")
    team1.remove_member("SE01")

    print("\n[Bước 12] Đổi trưởng nhóm rồi xóa người từng là trưởng nhóm:")
    print("   -> Bổ nhiệm SE02 làm trưởng nhóm thay thế:")
    team1.change_leader(se2)
    print("   -> Thực hiện xóa trưởng nhóm cũ (SE01):")
    team1.remove_member("SE01")
    team1.display_team()

    print("\n[Bước 13] Tạo nhóm thứ hai và thêm nhân sự đã có ở nhóm 1 để chứng minh kết tập:")
    def test_aggregation():
        team2 = ProjectTeam("P02", "Dự án Backend")
        team2.add_member(emp2) # Thêm NV02 (người đang thuộc Team 1)
        team2.display_team()
        
        print("\n[Bước 14] Hủy nhóm thứ hai bằng cách kết thúc khối lệnh cục bộ:")
        print("   -> Thoát khỏi hàm test_aggregation(), team2 sẽ tự động bị hủy...")
    
    test_aggregation() # Gọi hàm chứa team2

    print("\n[Bước 15] Chứng minh nhân sự của nhóm thứ hai (NV02) vẫn tồn tại sau khi nhóm bị hủy:")
    print("   -> In lại thông tin NV02:")
    emp2.display_info()
    print("   => Đối tượng NV02 vẫn tồn tại bình thường, chứng minh quan hệ Kết tập (Aggregation).")

    print("\n" + "="*50)
    print("KẾT THÚC CHƯƠNG TRÌNH KẾT QUẢ KIỂM THỬ")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_tests()

from django.db import models
from .constants import EMPLOYEE_DESIGNATION, EMPLOYEE_ROLE, EMPLOYEE_COMPANY
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserBaseManager

# Create your models here.

from django.db import models
from .constants import EMPLOYEE_DESIGNATION, EMPLOYEE_ROLE, EMPLOYEE_COMPANY
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserBaseManager


# Create your models here.

class Employee(AbstractBaseUser):
    emp_id = models.CharField(max_length=10, help_text="Employee ID")
    emp_name = models.CharField(max_length=30, help_text="Employee Name")
    emp_email = models.EmailField(max_length=255, unique=True, verbose_name="email")
    emp_profile = models.ImageField(null=True, blank=True)
    emp_address = models.TextField()
    emp_contact = models.CharField(max_length=15)
    emp_designation = models.CharField(choices=EMPLOYEE_DESIGNATION, max_length=70, help_text="Employee Designation")
    emp_role = models.CharField(choices=EMPLOYEE_ROLE, max_length=50, help_text="Employee Role")
    emp_company = models.CharField(choices=EMPLOYEE_COMPANY, max_length=50, help_text="Employee Company")
    status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserBaseManager()

    USERNAME_FIELD = "emp_email"
    REQUIRED_FIELDS = ["emp_id", "emp_name", "emp_profile", "emp_address", "emp_company", "is_active", "status",
                       "emp_role",
                       "emp_designation"]

    def __str__(self):
        return self.emp_email

    def has_perm(self, perm, obj=None):
        # return self.is_admin
        if self.emp_role == 'Admin':
            return True
        elif self.emp_role == 'HR':
            return True
        else:
            return False

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if self.emp_role == "Admin":
            self.is_admin = True
            self.is_staff = True
        if self.emp_role == "HR":
            self.is_admin = False
            self.is_staff = True
        if self.emp_role == "Employee":
            self.is_admin = False
            self.is_staff = False
        super().save(*args, **kwargs)

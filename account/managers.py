from django.contrib.auth.models import BaseUserManager


class UserBaseManager(BaseUserManager):
    def create_user(self, emp_id, emp_name, emp_email, emp_profile, emp_address, emp_contact,emp_designation, emp_role, emp_company,
                    is_active,
                    password=None, **extra_fields):
        if not emp_email:
            raise ValueError("Email is Required")
        user = self.model(emp_id=emp_id, emp_name=emp_name, emp_email=emp_email, emp_profile=emp_profile,
                          emp_address=emp_address,emp_contact=emp_contact, emp_designation=emp_designation, emp_role=emp_role,
                          emp_company=emp_company, is_active=is_active, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, emp_id, emp_name, emp_email, emp_profile, emp_address, emp_contact,emp_designation, emp_role, emp_company, is_active, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError("is_admin must be true")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("is_superuser must be true")

        return self.create_user(emp_id, emp_name, emp_email, emp_profile, emp_address, emp_contact,emp_designation, emp_role,emp_company, is_active, password=password, **extra_fields)

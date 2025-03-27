from django.contrib.auth.mixins import PermissionRequiredMixin


# Vlastné testy a oprávnenia
class StaffRequiredMixin(PermissionRequiredMixin):
    def test_func(self):
        return self.request.user.is_staff
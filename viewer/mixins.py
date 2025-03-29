from django.contrib.auth.mixins import UserPassesTestMixin


# Vlastné testy a oprávnenia
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
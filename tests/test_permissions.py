"""
Permission filtrlash testlari.
StaffForm da creator ruxsatlariga qarab filtrlash logikasi testlari.
"""
from django.test import TestCase
from apps.users.models import User
from apps.users.forms import (
    StaffForm, AVAILABLE_MODULES, AVAILABLE_ACTIONS, MODULE_EXTRA_ACTIONS,
)
from apps.organizations.models import Organization, Branch
from apps.core.permissions import check_permission


class StaffFormPermissionFilterTest(TestCase):
    """StaffForm da ruxsatlarni filtrlash testlari"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Markaz",
            subdomain="test-perm"
        )
        self.branch = Branch.objects.create(
            organization=self.org,
            name="Test Filial"
        )

    def test_super_admin_sees_all_modules(self):
        """Super admin barcha modullarni ko'rishi kerak"""
        admin = User.objects.create_user(
            phone="998901110001",
            password="test123",
            role="super_admin",
            organization=None,
        )
        form = StaffForm(user=admin)
        modules = form.get_filtered_modules()
        self.assertEqual(len(modules), len(AVAILABLE_MODULES))

    def test_owner_sees_all_modules(self):
        """Owner barcha modullarni ko'rishi kerak"""
        owner = User.objects.create_user(
            phone="998901110002",
            password="test123",
            role="owner",
            organization=self.org,
        )
        form = StaffForm(user=owner)
        modules = form.get_filtered_modules()
        self.assertEqual(len(modules), len(AVAILABLE_MODULES))

    def test_admin_without_perms_sees_all_modules(self):
        """Permissions bo'sh admin barcha modullarni ko'rishi kerak"""
        admin = User.objects.create_user(
            phone="998901110003",
            password="test123",
            role="admin",
            organization=self.org,
            permissions={},
        )
        form = StaffForm(user=admin)
        modules = form.get_filtered_modules()
        self.assertEqual(len(modules), len(AVAILABLE_MODULES))

    def test_limited_staff_sees_only_allowed_modules(self):
        """Cheklangan xodim faqat ruxsat berilgan modullarni ko'rishi kerak"""
        staff = User.objects.create_user(
            phone="998901110004",
            password="test123",
            role="staff",
            organization=self.org,
            permissions={
                "users": {"view": True, "create": True, "edit": False, "delete": False},
                "finance": {"view": True, "create": False},
            },
        )
        form = StaffForm(user=staff)
        modules = form.get_filtered_modules()
        module_codes = [m[0] for m in modules]
        self.assertIn('users', module_codes)
        self.assertIn('finance', module_codes)
        self.assertNotIn('education', module_codes)
        self.assertNotIn('crm', module_codes)
        self.assertNotIn('operations', module_codes)

    def test_staff_cannot_grant_unpossessed_permission(self):
        """Xodim o'zida bo'lmagan ruxsatni bera olmasligi kerak"""
        staff = User.objects.create_user(
            phone="998901110005",
            password="test123",
            role="admin",
            organization=self.org,
            permissions={
                "users": {"view": True, "create": True, "edit": False, "delete": False},
                "finance": {"view": True, "create": False},
            },
        )
        form = StaffForm(user=staff)
        # Creator users:delete ruxsatiga ega emas
        self.assertFalse(form.creator_has_permission('users', 'delete'))
        # Creator users:view ruxsatiga ega
        self.assertTrue(form.creator_has_permission('users', 'view'))
        self.assertTrue(form.creator_has_permission('users', 'create'))
        # Creator finance:create ruxsatiga ega emas
        self.assertFalse(form.creator_has_permission('finance', 'create'))
        self.assertTrue(form.creator_has_permission('finance', 'view'))

    def test_super_admin_has_all_permissions(self):
        """Super admin barcha ruxsatlarga ega bo'lishi kerak"""
        admin = User.objects.create_user(
            phone="998901110006",
            password="test123",
            role="super_admin",
            organization=None,
        )
        form = StaffForm(user=admin)
        for module_code, _, _ in AVAILABLE_MODULES:
            for action_code, _ in AVAILABLE_ACTIONS:
                self.assertTrue(
                    form.creator_has_permission(module_code, action_code),
                    f"Super admin should have {module_code}:{action_code}"
                )

    def test_filtered_extra_actions_for_super_admin(self):
        """Super admin barcha qo'shimcha amallarni ko'rishi kerak"""
        admin = User.objects.create_user(
            phone="998901110007",
            password="test123",
            role="super_admin",
            organization=None,
        )
        form = StaffForm(user=admin)
        extras = form.get_filtered_extra_actions()
        # At least the modules with extra actions should be present
        extra_module_codes = [e['module_code'] for e in extras]
        for module_code, actions in MODULE_EXTRA_ACTIONS.items():
            if actions:
                self.assertIn(module_code, extra_module_codes)

    def test_filtered_extra_actions_for_limited_staff(self):
        """Cheklangan xodim faqat ruxsat berilgan qo'shimcha amallarni ko'rishi kerak"""
        staff = User.objects.create_user(
            phone="998901110008",
            password="test123",
            role="staff",
            organization=self.org,
            permissions={
                "users": {
                    "view": True, "create": True,
                    "export_excel": True, "export_pdf": False,
                },
                "finance": {"view": True},
            },
        )
        form = StaffForm(user=staff)
        extras = form.get_filtered_extra_actions()
        extra_module_codes = [e['module_code'] for e in extras]

        # users moduli bo'lishi kerak (export_excel=True)
        self.assertIn('users', extra_module_codes)

        # users extra actions da faqat export_excel bo'lishi kerak
        users_extra = next(e for e in extras if e['module_code'] == 'users')
        users_action_codes = [ac for ac, _ in users_extra['actions']]
        self.assertIn('export_excel', users_action_codes)
        self.assertNotIn('export_pdf', users_action_codes)

    def test_form_without_user_shows_all(self):
        """User berilmaganda barcha modullar ko'rsatilishi kerak"""
        form = StaffForm()
        modules = form.get_filtered_modules()
        self.assertEqual(len(modules), len(AVAILABLE_MODULES))

    def test_staff_with_no_permissions_sees_nothing(self):
        """Permissions bo'sh xodim hech qanday modul ko'rmasligi kerak"""
        staff = User.objects.create_user(
            phone="998901110009",
            password="test123",
            role="staff",
            organization=self.org,
            permissions={},
        )
        form = StaffForm(user=staff)
        modules = form.get_filtered_modules()
        self.assertEqual(len(modules), 0)


class CheckPermissionGranularTest(TestCase):
    """check_permission funksiyasi granular ruxsatlar bilan testlari"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Markaz",
            subdomain="test-check"
        )

    def test_granular_permission_check(self):
        """Granular ruxsatlar (export_excel, view_salary) tekshirilishi"""
        staff = User.objects.create_user(
            phone="998901120001",
            password="test123",
            role="staff",
            organization=self.org,
            permissions={
                "users": {
                    "view": True,
                    "export_excel": True,
                    "export_pdf": False,
                },
                "finance": {
                    "view": True,
                    "view_salary": True,
                    "export_excel": False,
                },
            },
        )
        # Granular permissions
        self.assertTrue(check_permission(staff, 'users', 'export_excel'))
        self.assertFalse(check_permission(staff, 'users', 'export_pdf'))
        self.assertTrue(check_permission(staff, 'finance', 'view_salary'))
        self.assertFalse(check_permission(staff, 'finance', 'export_excel'))

    def test_super_admin_granular_permissions(self):
        """Super admin granular ruxsatlarga ham ega"""
        admin = User.objects.create_user(
            phone="998901120002",
            password="test123",
            role="super_admin",
            organization=None,
        )
        self.assertTrue(check_permission(admin, 'users', 'export_excel'))
        self.assertTrue(check_permission(admin, 'finance', 'view_salary'))

    def test_nonexistent_permission_returns_false(self):
        """Mavjud bo'lmagan ruxsat False qaytarishi kerak"""
        staff = User.objects.create_user(
            phone="998901120003",
            password="test123",
            role="staff",
            organization=self.org,
            permissions={"users": {"view": True}},
        )
        self.assertFalse(check_permission(staff, 'users', 'nonexistent_action'))
        self.assertFalse(check_permission(staff, 'nonexistent_module', 'view'))


class UserModelCustomPermissionsTest(TestCase):
    """User model Meta permissions testlari"""

    def test_custom_permissions_defined(self):
        """Custom permissions User modelda aniqlangan bo'lishi kerak"""
        meta_perms = User._meta.permissions
        perm_codenames = [p[0] for p in meta_perms]
        self.assertIn('can_export_users_excel', perm_codenames)
        self.assertIn('can_export_users_pdf', perm_codenames)
        self.assertIn('can_view_salary', perm_codenames)
        self.assertIn('can_export_finance_excel', perm_codenames)

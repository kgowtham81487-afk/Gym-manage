"""
IRONCORE RBAC & Granular Permission Definitions.
Enforces resource action authorization on all endpoints.
"""
from enum import Enum
from typing import Dict, List, Set


class RoleEnum(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    TRAINER = "TRAINER"
    CLIENT = "CLIENT"


class PermissionEnum(str, Enum):
    # System & Tenants
    SYSTEM_MANAGE = "system.manage"
    AUDIT_READ = "audit.read"
    TENANTS_MANAGE = "tenants.manage"
    BRANCHES_READ = "branches.read"
    BRANCHES_MANAGE = "branches.manage"
    
    # User Management
    USERS_READ = "users.read"
    USERS_CREATE = "users.create"
    USERS_UPDATE = "users.update"
    USERS_DELETE = "users.delete"
    USERS_ASSIGN_ROLE = "users.assign_role"
    SESSIONS_REVOKE = "sessions.revoke"
    
    # CRM
    LEADS_READ = "leads.read"
    LEADS_CREATE = "leads.create"
    LEADS_UPDATE = "leads.update"
    LEADS_CONVERT = "leads.convert"
    COMPLAINTS_MANAGE = "complaints.manage"
    FEEDBACK_MANAGE = "feedback.manage"
    
    # Memberships
    MEMBERSHIPS_READ = "memberships.read"
    MEMBERSHIPS_READ_SELF = "memberships.read_self"
    MEMBERSHIPS_CREATE = "memberships.create"
    MEMBERSHIPS_UPDATE = "memberships.update"
    MEMBERSHIPS_CANCEL = "memberships.cancel"
    MEMBERSHIP_PLANS_MANAGE = "membership_plans.manage"
    
    # PT (Personal Training)
    PT_READ = "pt.read"
    PT_READ_ASSIGNED = "pt.read_assigned"
    PT_READ_SELF = "pt.read_self"
    PT_CREATE = "pt.create"
    PT_SCHEDULE = "pt.schedule"
    PT_COMPLETE = "pt.complete"
    PT_CANCEL = "pt.cancel"
    PT_PACKAGES_MANAGE = "pt_packages.manage"
    
    # Attendance
    ATTENDANCE_READ = "attendance.read"
    ATTENDANCE_CHECKIN = "attendance.checkin"
    ATTENDANCE_CHECKOUT = "attendance.checkout"
    ATTENDANCE_MANAGE = "attendance.manage"
    
    # Workouts & Instructions
    WORKOUTS_READ = "workouts.read"
    WORKOUTS_READ_ASSIGNED = "workouts.read_assigned"
    WORKOUTS_READ_SELF = "workouts.read_self"
    WORKOUTS_CREATE = "workouts.create"
    WORKOUTS_UPDATE = "workouts.update"
    DIET_MANAGE = "diet.manage"
    MEASUREMENTS_RECORD = "measurements.record"
    
    # Inventory & Procurement
    INVENTORY_READ = "inventory.read"
    INVENTORY_ADJUST = "inventory.adjust"
    INVENTORY_TRANSFER = "inventory.transfer"
    SUPPLIERS_MANAGE = "suppliers.manage"
    PURCHASE_ORDERS_MANAGE = "purchase_orders.manage"
    PRODUCTS_MANAGE = "products.manage"
    
    # POS & Sales
    SALES_READ = "sales.read"
    SALES_READ_ASSIGNED = "sales.read_assigned"
    SALES_READ_SELF = "sales.read_self"
    SALES_CREATE = "sales.create"
    SALES_DAILY_CLOSE = "sales.daily_close"
    
    # Payments & Invoices
    PAYMENTS_READ = "payments.read"
    PAYMENTS_READ_SELF = "payments.read_self"
    PAYMENTS_CREATE = "payments.create"
    PAYMENTS_REFUND = "payments.refund"
    INVOICES_MANAGE = "invoices.manage"
    
    # HR & Payroll
    HR_EMPLOYEES_READ = "hr.employees.read"
    HR_EMPLOYEES_MANAGE = "hr.employees.manage"
    HR_SALARIES_READ = "hr.salaries.read"
    HR_SALARIES_MANAGE = "hr.salaries.manage"
    HR_LEAVE_REQUEST = "hr.leave.request"
    HR_LEAVE_APPROVE = "hr.leave.approve"
    HR_COMMISSIONS_READ = "hr.commissions.read"
    HR_COMMISSIONS_MANAGE = "hr.commissions.manage"
    
    # Analytics & Reports
    REPORTS_READ = "reports.read"
    REPORTS_FINANCIAL = "reports.financial"
    REPORTS_OPERATIONAL = "reports.operational"
    
    # Notifications
    NOTIFICATIONS_SEND = "notifications.send"


# Role to granular permissions map
ROLE_PERMISSIONS: Dict[RoleEnum, Set[PermissionEnum]] = {
    RoleEnum.SUPER_ADMIN: set(PermissionEnum),  # Full access
    
    RoleEnum.ADMIN: {
        PermissionEnum.BRANCHES_READ,
        PermissionEnum.USERS_READ,
        PermissionEnum.USERS_CREATE,
        PermissionEnum.USERS_UPDATE,
        PermissionEnum.LEADS_READ,
        PermissionEnum.LEADS_CREATE,
        PermissionEnum.LEADS_UPDATE,
        PermissionEnum.LEADS_CONVERT,
        PermissionEnum.COMPLAINTS_MANAGE,
        PermissionEnum.FEEDBACK_MANAGE,
        PermissionEnum.MEMBERSHIPS_READ,
        PermissionEnum.MEMBERSHIPS_CREATE,
        PermissionEnum.MEMBERSHIPS_UPDATE,
        PermissionEnum.MEMBERSHIPS_CANCEL,
        PermissionEnum.MEMBERSHIP_PLANS_MANAGE,
        PermissionEnum.PT_READ,
        PermissionEnum.PT_CREATE,
        PermissionEnum.PT_SCHEDULE,
        PermissionEnum.PT_COMPLETE,
        PermissionEnum.PT_CANCEL,
        PermissionEnum.PT_PACKAGES_MANAGE,
        PermissionEnum.ATTENDANCE_READ,
        PermissionEnum.ATTENDANCE_CHECKIN,
        PermissionEnum.ATTENDANCE_CHECKOUT,
        PermissionEnum.ATTENDANCE_MANAGE,
        PermissionEnum.WORKOUTS_READ,
        PermissionEnum.WORKOUTS_CREATE,
        PermissionEnum.WORKOUTS_UPDATE,
        PermissionEnum.DIET_MANAGE,
        PermissionEnum.MEASUREMENTS_RECORD,
        PermissionEnum.INVENTORY_READ,
        PermissionEnum.INVENTORY_ADJUST,
        PermissionEnum.INVENTORY_TRANSFER,
        PermissionEnum.SUPPLIERS_MANAGE,
        PermissionEnum.PURCHASE_ORDERS_MANAGE,
        PermissionEnum.PRODUCTS_MANAGE,
        PermissionEnum.SALES_READ,
        PermissionEnum.SALES_CREATE,
        PermissionEnum.SALES_DAILY_CLOSE,
        PermissionEnum.PAYMENTS_READ,
        PermissionEnum.PAYMENTS_CREATE,
        PermissionEnum.PAYMENTS_REFUND,
        PermissionEnum.INVOICES_MANAGE,
        PermissionEnum.HR_EMPLOYEES_READ,
        PermissionEnum.HR_EMPLOYEES_MANAGE,
        PermissionEnum.HR_LEAVE_REQUEST,
        PermissionEnum.HR_LEAVE_APPROVE,
        PermissionEnum.HR_COMMISSIONS_READ,
        PermissionEnum.REPORTS_READ,
        PermissionEnum.REPORTS_OPERATIONAL,
        PermissionEnum.NOTIFICATIONS_SEND,
    },
    
    RoleEnum.TRAINER: {
        PermissionEnum.BRANCHES_READ,
        PermissionEnum.PT_READ_ASSIGNED,
        PermissionEnum.PT_SCHEDULE,
        PermissionEnum.PT_COMPLETE,
        PermissionEnum.ATTENDANCE_CHECKIN,
        PermissionEnum.ATTENDANCE_CHECKOUT,
        PermissionEnum.WORKOUTS_READ_ASSIGNED,
        PermissionEnum.WORKOUTS_CREATE,
        PermissionEnum.WORKOUTS_UPDATE,
        PermissionEnum.DIET_MANAGE,
        PermissionEnum.MEASUREMENTS_RECORD,
        PermissionEnum.INVENTORY_READ,
        PermissionEnum.SALES_CREATE,
        PermissionEnum.SALES_READ_ASSIGNED,
        PermissionEnum.HR_LEAVE_REQUEST,
        PermissionEnum.HR_COMMISSIONS_READ,
    },
    
    RoleEnum.CLIENT: {
        PermissionEnum.MEMBERSHIPS_READ_SELF,
        PermissionEnum.PT_READ_SELF,
        PermissionEnum.ATTENDANCE_CHECKIN,
        PermissionEnum.WORKOUTS_READ_SELF,
        PermissionEnum.INVENTORY_READ,
        PermissionEnum.SALES_READ_SELF,
        PermissionEnum.PAYMENTS_READ_SELF,
        PermissionEnum.PAYMENTS_CREATE,
    }
}

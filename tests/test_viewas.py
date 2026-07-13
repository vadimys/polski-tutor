"""View-as: чиста мапа ефективної ролі."""

from app.services import viewas


def test_role_for():
    assert viewas.role_for("teacher", "student") == "teacher"
    assert viewas.role_for("student", "teacher") == "student"
    assert viewas.role_for("referred", "admin") == "student"  # референс → студентський UI
    assert viewas.role_for("", "teacher") == "teacher"  # нема режиму → реальна роль
    assert viewas.role_for("", "admin") == "admin"
    assert viewas.role_for("хз", "student") == "student"  # невідомий режим → реальна

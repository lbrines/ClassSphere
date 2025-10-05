"""
Tests for role-based dashboard endpoints
"""
import pytest


class TestAdminDashboard:
    """Test admin dashboard endpoint"""

    def test_admin_dashboard_success(self, client, admin_token, auth_headers):
        """Test admin dashboard with admin token"""
        response = client.get(
            "/api/v1/admin/dashboard",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == 200

        data = response.json()
        assert data["user_role"] == "admin"
        assert "message" in data
        assert "permissions" in data
        assert "stats" in data

        # Verify admin permissions
        assert "manage_users" in data["permissions"]
        assert "manage_courses" in data["permissions"]
        assert "view_analytics" in data["permissions"]
        assert "system_settings" in data["permissions"]

    def test_admin_dashboard_coordinator_access(self, client, coordinator_token, auth_headers):
        """Test admin dashboard with coordinator token (should fail)"""
        response = client.get(
            "/api/v1/admin/dashboard",
            headers=auth_headers(coordinator_token)
        )
        assert response.status_code == 403
        assert "admin role or higher" in response.json()["detail"]

    def test_admin_dashboard_teacher_access(self, client, teacher_token, auth_headers):
        """Test admin dashboard with teacher token (should fail)"""
        response = client.get(
            "/api/v1/admin/dashboard",
            headers=auth_headers(teacher_token)
        )
        assert response.status_code == 403

    def test_admin_dashboard_student_access(self, client, student_token, auth_headers):
        """Test admin dashboard with student token (should fail)"""
        response = client.get(
            "/api/v1/admin/dashboard",
            headers=auth_headers(student_token)
        )
        assert response.status_code == 403

    def test_admin_dashboard_no_auth(self, client):
        """Test admin dashboard without authentication"""
        response = client.get("/api/v1/admin/dashboard")
        assert response.status_code == 403


class TestCoordinatorDashboard:
    """Test coordinator dashboard endpoint"""

    def test_coordinator_dashboard_admin_access(self, client, admin_token, auth_headers):
        """Test coordinator dashboard with admin token (should work)"""
        response = client.get(
            "/api/v1/coordinator/dashboard",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "permissions" in data
        assert "stats" in data

    def test_coordinator_dashboard_coordinator_access(self, client, coordinator_token, auth_headers):
        """Test coordinator dashboard with coordinator token"""
        response = client.get(
            "/api/v1/coordinator/dashboard",
            headers=auth_headers(coordinator_token)
        )
        assert response.status_code == 200

        data = response.json()
        assert data["user_role"] == "coordinator"
        assert "assign_teachers" in data["permissions"]
        assert "manage_curriculum" in data["permissions"]

    def test_coordinator_dashboard_teacher_access(self, client, teacher_token, auth_headers):
        """Test coordinator dashboard with teacher token (should fail)"""
        response = client.get(
            "/api/v1/coordinator/dashboard",
            headers=auth_headers(teacher_token)
        )
        assert response.status_code == 403

    def test_coordinator_dashboard_student_access(self, client, student_token, auth_headers):
        """Test coordinator dashboard with student token (should fail)"""
        response = client.get(
            "/api/v1/coordinator/dashboard",
            headers=auth_headers(student_token)
        )
        assert response.status_code == 403


class TestTeacherDashboard:
    """Test teacher dashboard endpoint"""

    def test_teacher_dashboard_admin_access(self, client, admin_token, auth_headers):
        """Test teacher dashboard with admin token (should work)"""
        response = client.get(
            "/api/v1/teacher/dashboard",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == 200

    def test_teacher_dashboard_coordinator_access(self, client, coordinator_token, auth_headers):
        """Test teacher dashboard with coordinator token (should work)"""
        response = client.get(
            "/api/v1/teacher/dashboard",
            headers=auth_headers(coordinator_token)
        )
        assert response.status_code == 200

    def test_teacher_dashboard_teacher_access(self, client, teacher_token, auth_headers):
        """Test teacher dashboard with teacher token"""
        response = client.get(
            "/api/v1/teacher/dashboard",
            headers=auth_headers(teacher_token)
        )
        assert response.status_code == 200

        data = response.json()
        assert data["user_role"] == "teacher"
        assert "create_courses" in data["permissions"]
        assert "grade_assignments" in data["permissions"]

    def test_teacher_dashboard_student_access(self, client, student_token, auth_headers):
        """Test teacher dashboard with student token (should fail)"""
        response = client.get(
            "/api/v1/teacher/dashboard",
            headers=auth_headers(student_token)
        )
        assert response.status_code == 403


class TestStudentDashboard:
    """Test student dashboard endpoint"""

    def test_student_dashboard_all_roles_access(self, client, admin_token, coordinator_token,
                                               teacher_token, student_token, auth_headers):
        """Test student dashboard with all role tokens (all should work)"""
        tokens = [admin_token, coordinator_token, teacher_token, student_token]

        for token in tokens:
            response = client.get(
                "/api/v1/student/dashboard",
                headers=auth_headers(token)
            )
            assert response.status_code == 200

            data = response.json()
            assert "message" in data
            assert "permissions" in data
            assert "stats" in data

    def test_student_dashboard_student_specific(self, client, student_token, auth_headers):
        """Test student dashboard with student token - verify specific data"""
        response = client.get(
            "/api/v1/student/dashboard",
            headers=auth_headers(student_token)
        )
        assert response.status_code == 200

        data = response.json()
        assert data["user_role"] == "student"
        assert "view_courses" in data["permissions"]
        assert "view_grades" in data["permissions"]
        assert "submit_assignments" in data["permissions"]

        # Verify stats structure
        stats = data["stats"]
        assert "enrolled_courses" in stats
        assert "average_grade" in stats
        assert "pending_assignments" in stats

    def test_student_dashboard_no_auth(self, client):
        """Test student dashboard without authentication"""
        response = client.get("/api/v1/student/dashboard")
        assert response.status_code == 403
import { useState, useEffect } from "react";
import { api } from "../../api/client";
import { useToast } from "../../context/ToastContext";

const ROLES = [
  { id: 1, name: "admin" },
  { id: 2, name: "hod" },
  { id: 3, name: "club_leader" },
  { id: 4, name: "student_leader" },
  { id: 5, name: "student" },
];

export default function ManageUsers() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const { showError, showSuccess } = useToast();
    const [roles, setRoles] = useState([]);

    useEffect(() => {
    loadUsers();
    api.get("/roles/").then(setRoles).catch((err) => showError(err.message));
    }, []);

    async function loadUsers() {
        try {
            const data = await api.get("/admin/users/");
            setUsers(data);
        } catch (err) {
            showError(err.message);
        } finally {
            setLoading(false);
        }
        }

    useEffect(() => {
        loadUsers();
    }, []);

    async function changeRole(userId, roleId) {
        try {
        await api.patch(`/users/${userId}/role`, { role_id: Number(roleId) });
        showSuccess("Role updated");
        loadUsers();
        } catch (err) {
        showError(err.message);
        }
    }

    async function toggleActive(user) {
        try {
        const action = user.is_active ? "deactivate" : "activate";
        await api.patch(`/admin/users/${user.id}/${action}`);
        showSuccess(user.is_active ? "User deactivated" : "User activated");
        loadUsers();
        } catch (err) {
        showError(err.message);
        }
    }

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-xl font-semibold mb-4">Manage Users</h1>
      <div className="bg-white rounded   overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="border-b bg-gray-50">
            <tr>
              <th className="text-left p-3">Name</th>
              <th className="text-left p-3">Email</th>
              <th className="text-left p-3">Role</th>
              <th className="text-left p-3">Status</th>
              <th className="text-left p-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} className="border-b last:border-0">
                <td className="p-3">{u.full_name}</td>
                <td className="p-3">{u.email}</td>
                <td className="p-3">
                  <select
                    value={u.role.id}
                    onChange={(e) => changeRole(u.id, e.target.value)}
                    className="border rounded px-2 py-1"
                  >
                    {roles.map((r) => (
                      <option key={r.id} value={r.id}>{r.role}</option>
                    ))}
                  </select>
                </td>
                <td className="p-3">
                  <span className={u.is_active ? "text-jkuat-green" : "text-red-600"}>
                    {u.is_active ? "Active" : "Inactive"}
                  </span>
                </td>
                <td className="p-3">
                  <button
                    onClick={() => toggleActive(u)}
                    className="text-xs px-2 py-1 border rounded"
                  >
                    {u.is_active ? "Deactivate" : "Activate"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
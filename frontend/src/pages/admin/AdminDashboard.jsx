import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function AdminDashboard() {
  const { pendingCount } = useAuth();

  const links = [
    { to: "/admin/manage-users", label: "Manage Users" },
    { to: "/admin/departments", label: "Manage Departments" },
    { to: "/admin/clubs", label: "Manage Clubs" },
    { to: "/admin/courses", label: "Manage Courses" },
    { to: "/admin/categories", label: "Manage Categories" },
    { to: "/review-queue", label: `Review Queue${pendingCount > 0 ? ` (${pendingCount})` : ""}` },
  ];
  

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-xl font-semibold mb-4">Admin Dashboard</h1>
      <div className="grid grid-cols-2 gap-3">
        {links.map((link) => (
          <Link
            key={link.to}
            to={link.to}
            className="bg-white p-4 rounded  hover:border-jkuat-green text-sm font-medium"
          >
            {link.label}
          </Link>
        ))}
      </div>
    </div>
  );
}
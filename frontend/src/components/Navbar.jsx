import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const POSTING_ROLES = ["admin", "hod", "club_leader", "student_leader"];

export default function Navbar() {
  const { user, loading, logout } = useAuth();

  return (
    <nav className="bg-jkuat-green text-white  px-4 py-3 flex justify-between items-center">
      <Link to="/" className="font-semibold">Noticeboard</Link>

      <div className="flex items-center gap-4 text-sm">
        {!loading && user && POSTING_ROLES.includes(user.role.role) && (
          <Link to="/post-notice" className="text-blue-600">Post Notice</Link>
        )}

        {!loading && user && (
          <button onClick={logout} className="text-gray-600">
            Log out ({user.full_name})
          </button>
        )}

        {!loading && !user && (
          <>
            <Link to="/login" className="text-blue-600">Log in</Link>
            <Link to="/register" className="text-blue-600">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}
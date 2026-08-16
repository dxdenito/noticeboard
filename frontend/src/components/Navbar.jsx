import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import logo from "../images/jkuatlogo.png"

const POSTING_ROLES = ["admin", "hod", "club_leader", "student_leader"];

export default function Navbar() {
  const { user, loading, logout, pendingCount } = useAuth();

  return (
    <>
    <div className="bg-jkuat-red text-white w-full p-2 flex gap-2">
      <a href="https://www.jkuat.ac.ke">Jkuat website</a>
      <a href="https://portal.jkuat.ac.ke">Student portal</a>
    </div>
    <nav className="bg-jkuat-green text-white  px-4 py-3 flex justify-between items-center">
      <div>
          
      
         <Link to="/" className="flex items-center gap-2 font-semibold"><img src={logo} className="w-8 h-8" alt="jkuat logo" />Noticeboard</Link>
    </div>
      <div className="flex items-center gap-4 text-sm">
        {!loading && user && POSTING_ROLES.includes(user.role.role) && (
          <Link to="/post-notice" className="text-white-600">Post Notice</Link>
        )}
        {!loading && user && (
          <>
            <Link to="/my-bookmarks" className="text-white">Bookmarks</Link>
            {POSTING_ROLES.includes(user.role.role) && (
              <Link to="/my-notices" className="text-white">My Notices</Link>
            )}
          </>
        )}
        {!loading && user?.role.role === "admin" && (
          <Link to="/review-queue" className="text-gray-600 relative">
            Review Queue
            {pendingCount > 0 && (
              <span className="ml-1 bg-red-600 text-white text-xs px-1.5 py-0.5 rounded-full">
                {pendingCount}
              </span>
            )}
          </Link>
        )}

        {!loading && user && (
          <button onClick={logout} className="text-white-600">
            Log out ({user.full_name})
          </button>
        )}

        {!loading && !user && (
          <>
            <Link to="/login" className="text-white-600">Log in</Link>
            <Link to="/register" className="text-white-600">Register</Link>
          </>
        )}
      </div>
    </nav>
    </>
  );
}
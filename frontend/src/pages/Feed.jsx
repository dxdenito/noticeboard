import { useState, useEffect } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

export default function Feed() {
  const { user, loading: authLoading, logout } = useAuth();
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadNotices() {
      try {
        const data = await api.get("/notices/");
        setNotices(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    if (!authLoading) loadNotices();
  }, [authLoading]);

  if (loading) return <div className="p-8 text-center">Loading notices...</div>;
  if (error) return <div className="p-8 text-red-600">{error}</div>;

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-xl font-semibold">Noticeboard</h1>
        <Link to={`/post-notice`}>Post notice</Link>
        {user ? (
          <button onClick={logout} className="text-sm text-blue-600">
            Log out ({user.full_name})
          </button>
        ) : (
          <a href="/login" className="text-sm text-blue-600">Log in</a>
        )}
      </div>

      <ul className="space-y-3">
        {notices.map((notice) => (
            <li key={notice.id} className="bg-white rounded shadow-sm ">
                <Link to={`/notices/${notice.id}`} className="block p-4">
                    <h2 className="font-medium">{notice.title}</h2>
                    <p className="text-sm text-gray-600 line-clamp-2">{notice.body}</p>
                </Link>
            </li>
        ))}
      </ul>

      {notices.length === 0 && (
        <p className="text-gray-500 text-center mt-8">No notices yet.</p>
      )}
    </div>
  );
}
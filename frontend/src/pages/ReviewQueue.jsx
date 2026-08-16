import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

export default function ReviewQueue() {
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionLoading, setActionLoading] = useState(null);
  const { refreshPendingCount } = useAuth();
  const { showError } = useToast();

  async function loadPending() {
    try {
      const data = await api.get("/notices/pending");
      setNotices(data);
    } catch (err) {
      showError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadPending();
  }, []);

  async function handleDecision(id, action) {
    setActionLoading(id);
    try {
      await api.patch(`/notices/${id}/${action}`);
      setNotices((prev) => prev.filter((n) => n.id !== id));
      refreshPendingCount();
    } catch (err) {
      showError(err.message);
    } finally {
      setActionLoading(null);
    }
  }

  if (loading) return <div className="p-8 text-center">Loading...</div>;


  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-xl font-semibold mb-4">Review Queue</h1>

      {notices.length === 0 && (
        <p className="text-gray-500 text-center mt-8">Nothing pending review.</p>
      )}

      <ul className="space-y-3">
        {notices.map((notice) => (
          <li key={notice.id} className="bg-white p-4 rounded shadow-sm border">
            <Link to={`/notices/${notice.id}`} className="font-medium hover:underline">
              {notice.title}
            </Link>
            {notice.status !== "approved" && (
                <span
                    className={`inline-block text-xs font-medium px-2 py-1 rounded mb-3 ${
                    notice.status === "pending"
                        ? "bg-yellow-100 text-yellow-800"
                        : "bg-red-100 text-red-800"
                    }`}
                >
                    {notice.status === "pending" ? "Pending Review" : "Rejected"}
                </span>
            )}
            <p className="text-sm text-gray-600 mb-2 line-clamp-2">{notice.body}</p>
            <p className="text-xs text-gray-400 mb-3">
              {notice.scope_level} &middot; {notice.category?.name}
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => handleDecision(notice.id, "approve")}
                disabled={actionLoading === notice.id}
                className="bg-jkuat-green text-white text-sm px-3 py-1 rounded disabled:opacity-50"
              >
                Approve
              </button>
              <button
                onClick={() => handleDecision(notice.id, "reject")}
                disabled={actionLoading === notice.id}
                className="bg-red-600 text-white text-sm px-3 py-1 rounded disabled:opacity-50"
              >
                Reject
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
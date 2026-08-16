import { useState, useEffect } from "react";
import { api } from "../api/client";
import NoticeCard from "../components/NoticeCard";
import { useToast } from "../context/ToastContext";

export default function MyBookmarks() {
  const [bookmarks, setBookmarks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { showError } = useToast();

  useEffect(() => {
    api.get("/users/me/bookmarks")
      .then(setBookmarks)
      .catch((err) => showError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-center">Loading...</div>;


  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-xl font-semibold mb-4">My Bookmarks</h1>
      <ul className="space-y-3">
        {bookmarks.map((b) => (
  <NoticeCard key={b.notice.id} notice={{ ...b.notice, is_bookmarked: true }} />
))}
      </ul>
      {bookmarks.length === 0 && (
        <p className="text-gray-500 text-center mt-8">No bookmarks yet.</p>
      )}
    </div>
  );
}
import { useState, useEffect } from "react";
import { api } from "../api/client";
import NoticeCard from "../components/NoticeCard";

export default function MyNotices() {
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.get("/notices/mine")
      .then(setNotices)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (error) return <div className="p-8 text-red-600">{error}</div>;

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-xl font-semibold mb-4">My Notices</h1>
      <ul className="space-y-3">
        {notices.map((notice) => <NoticeCard key={notice.id} notice={notice} />)}
      </ul>
      {notices.length === 0 && (
        <p className="text-gray-500 text-center mt-8">You haven't posted any notices yet.</p>
      )}
    </div>
  );
}
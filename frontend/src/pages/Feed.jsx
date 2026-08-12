import { useState, useEffect } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import NoticeCard from "../components/NoticeCard";

const PAGE_SIZE = 10;

export default function Feed() {
  const { loading: authLoading } = useAuth();
  const [notices, setNotices] = useState([]);
  const [page, setPage] = useState(1);
  const [hasNextPage, setHasNextPage] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadNotices() {
      setLoading(true);
      try {
        const offset = (page - 1) * PAGE_SIZE;
        // request one extra item to detect if a next page exists
        const data = await api.get(`/notices/?limit=${PAGE_SIZE + 1}&offset=${offset}`);
        setHasNextPage(data.length > PAGE_SIZE);
        setNotices(data.slice(0, PAGE_SIZE));
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    if (!authLoading) loadNotices();
  }, [page, authLoading]);

  if (loading) return <div className="p-8 text-center">Loading notices...</div>;
  if (error) return <div className="p-8 text-red-600">{error}</div>;

  return (
    <div className="max-w-2xl mx-auto p-4">
      <ul className="space-y-3">
        {notices.map((notice) => <NoticeCard key={notice.id} notice={notice} />)}
      </ul>

      {notices.length === 0 && (
        <p className="text-gray-500 text-center mt-8">No notices yet.</p>
      )}

      <div className="flex justify-between items-center mt-6">
        <button
          onClick={() => setPage((p) => p - 1)}
          disabled={page === 1}
          className="px-4 py-2 border rounded disabled:opacity-40"
        >
          Previous
        </button>
        <span className="text-sm text-gray-500">Page {page}</span>
        <button
          onClick={() => setPage((p) => p + 1)}
          disabled={!hasNextPage}
          className="px-4 py-2 border rounded disabled:opacity-40"
        >
          Next
        </button>
      </div>
    </div>
  );
}
import { useState, useEffect } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import NoticeCard from "../components/NoticeCard";
import { useToast } from "../context/ToastContext";

const PAGE_SIZE = 10;

export default function Feed() {
  const { loading: authLoading } = useAuth();
  const [tab, setTab] = useState("all"); // "all" | "pinned"
  const [notices, setNotices] = useState([]);
  const [page, setPage] = useState(1);
  const [hasNextPage, setHasNextPage] = useState(false);
  const [loading, setLoading] = useState(true);
  const { showError } = useToast();

  useEffect(() => {
    async function loadNotices() {
      setLoading(true);
      try {
        if (tab === "pinned") {
          const data = await api.get("/notices/pinned");
          setNotices(data);
          setHasNextPage(false);
        } else {
          const offset = (page - 1) * PAGE_SIZE;
          // request one extra item to detect if a next page exists
          const data = await api.get(`/notices/?limit=${PAGE_SIZE + 1}&offset=${offset}`);
          setHasNextPage(data.length > PAGE_SIZE);
          setNotices(data.slice(0, PAGE_SIZE));
        }
      } catch (err) {
        showError(err.message);
      } finally {
        setLoading(false);
      }
    }
    if (!authLoading) loadNotices();
  }, [page, tab, authLoading]);

  function switchTab(newTab) {
    setTab(newTab);
    setPage(1); // reset pagination when switching tabs
  }

  if (loading) return <div className="p-8 text-center">Loading notices...</div>;

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="flex gap-4 border-b mb-4">
        <button
          onClick={() => switchTab("all")}
          className={`pb-2 px-1 text-sm font-medium border-b-2 ${
            tab === "all" ? "border-jkuat-green text-jkuat-green" : "border-transparent text-gray-500"
          }`}
        >
          All Notices
        </button>
        <button
          onClick={() => switchTab("pinned")}
          className={`pb-2 px-1 text-sm font-medium border-b-2 ${
            tab === "pinned" ? "border-jkuat-green text-jkuat-green" : "border-transparent text-gray-500"
          }`}
        >
          Pinned
        </button>
      </div>

      <ul className="space-y-3">
        {notices.map((notice) => <NoticeCard key={notice.id} notice={notice} />)}
      </ul>

      {notices.length === 0 && (
        <p className="text-gray-500 text-center mt-8">
          {tab === "pinned" ? "Nothing pinned yet." : "No notices yet."}
        </p>
      )}

      {tab === "all" && (
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
      )}
    </div>
  );
}
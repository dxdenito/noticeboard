import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../api/client";

export default function NoticeDetail() {
  const { id } = useParams();
  const [notice, setNotice] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadNotice() {
      try {
        const data = await api.get(`/notices/${id}`);
        setNotice(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    loadNotice();
  }, [id]);

  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (error) return <div className="p-8 text-red-600">{error}</div>;

  return (
    <div className="max-w-2xl mx-auto p-4">
      <Link to="/" className="text-sm text-blue-600 mb-4 inline-block">
        &larr; Back to feed
      </Link>

      <div className="bg-white p-6 rounded  ">
        <h1 className="text-2xl font-semibold mb-2">{notice.title}</h1>
        <p className="text-sm text-gray-500 mb-4">
          {notice.category?.name} &middot; {notice.priority}
        </p>
        <p className="whitespace-pre-wrap">{notice.body}</p>
      </div>
    </div>
  );
}
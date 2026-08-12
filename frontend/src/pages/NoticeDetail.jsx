import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../api/client";
import { QRCodeSVG } from 'qrcode.react';
import { useAuth } from "../context/AuthContext";

export default function NoticeDetail() {
  const { id } = useParams();
  const [notice, setNotice] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const currentPostUrl = window.location.href;
  const [bookmarked, setBookmarked] = useState(false);
  const [bookmarkLoading, setBookmarkLoading] = useState(false);
  const { user } = useAuth();

  async function toggleBookmark() {
    setBookmarkLoading(true);
    try {
      if (bookmarked) {
        await api.delete(`/notices/${id}/bookmark`);
        setBookmarked(false);
      } else {
        await api.post(`/notices/${id}/bookmark`);
        setBookmarked(true);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setBookmarkLoading(false);
    }
  }
  
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
    <>
    <div className="max-w-2xl mx-auto p-4">
      <Link to="/" className="text-sm text-blue-600 mb-4 inline-block">
        &larr; Back to feed
      </Link>
      <br />
      {user && (
        <button
          onClick={toggleBookmark}
          disabled={bookmarkLoading}
          className="text-sm text-blue-600 mb-4"
        >
          {bookmarked ? "★ Bookmarked" : "☆ Bookmark this"}
        </button>
      )}

      <div className="bg-white p-6 rounded  ">
        <h1 className="text-2xl font-semibold mb-2">{notice.title}</h1>
        <p className="text-sm text-gray-500 mb-4">
          {notice.category?.name} &middot; {notice.priority}
        </p>
        <p className="whitespace-pre-wrap">{notice.body}</p>
      </div>
    </div>
    {notice.attachments?.length > 0 && (
      <div className="mt-4 border-t pt-4 flex  justify-center ">
        <h3 className="font-medium mb-2">Attachments</h3>
        <ul className="space-y-1">
          {notice.attachments.map((att) => (
            <li key={att.id}>
              <a
              
                href={`${import.meta.env.VITE_API_URL}/attachments/${att.id}/download`}
                className="text-blue-600 text-sm underline"
              >
                {att.file_name}
              </a>
            </li>
          ))}
        </ul>
      </div>
    )}

    <div className="mt-4 p-2 border border-[#eaeaea] rounded bg-[#fafafa] flex items-center justify-center gap-2" >
        <div>
          <h3>Scan to Read on Mobile</h3>
          <p style={{ color: '#555', fontSize: '0.9em' }}>
            Share this article with friends or switch to your phone by scanning this code.
          </p>
        </div>
        
        
        
        <div style={{ background: '#fff', padding: '10px', borderRadius: '4px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <QRCodeSVG 
            value={currentPostUrl} // Directly encodes the current browser tab URL
            size={60}             // Image width/height in pixels
            bgColor={"#ffffff"}    // Background color
            fgColor={"#000000"}    // QR code block color
            level={"M"}            // Error correction level (L, M, Q, H)
          />
        </div>
      </div>
      </>
  );
}
import { Link } from "react-router-dom";
import { Star } from "lucide-react";

export default function NoticeCard({ notice }) {
  return (
    <li className="bg-white rounded  ">
      <Link to={`/notices/${notice.id}`} className="block p-4">
        <div className="flex justify-between items-start">
          <h2 className="font-medium">{notice.title}</h2>
          {notice.is_bookmarked && (
            <Star size={12} fill="currentColor" className="text-yellow-500 shrink-0 ml-2" />
          )}
        </div>
        <p className="text-sm text-gray-600 line-clamp-2">{notice.body}</p>
      </Link>
    </li>
  );
}
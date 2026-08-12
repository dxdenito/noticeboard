import { Link } from "react-router-dom";

export default function NoticeCard({ notice }) {
  return (
    <li className="bg-white rounded shadow-sm ">
      <Link to={`/notices/${notice.id}`} className="block p-4">
        <div className="flex justify-between items-start">
          <h2 className="font-medium">{notice.title}</h2>
          {notice.is_bookmarked && (
            <span className="text-yellow-500 text-xs shrink-0 ml-2">★</span>
          )}
        </div>
        <p className="text-sm text-gray-600 line-clamp-2">{notice.body}</p>
      </Link>
    </li>
  );
}
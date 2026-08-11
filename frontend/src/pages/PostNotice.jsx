import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { api } from "../api/client";

export default function PostNotice() {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  const [categories, setCategories] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [clubs, setClubs] = useState([]);
  const [courses, setCourses] = useState([]);
  const [files, setFiles] = useState([]);

  const [form, setForm] = useState({
    title: "",
    body: "",
    category_id: "",
    scope_level: "public",
    priority: "low",
    visibility: "internal",
    department_id: "",
    club_id: "",
    course_id: "",
    expiry_date: "",
  });
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    Promise.all([
      api.get("/categories/"),
      api.get("/departments/"),
      api.get("/clubs/"),
      api.get("/courses/"),
    ]).then(([cats, deptList, clubList, courseList]) => {
      setCategories(cats);
      setDepartments(deptList);
      setClubs(clubList);
      setCourses(courseList);
    }).catch((err) => setError(err.message));
  }, []);

  if (authLoading) return <div className="p-8 text-center">Loading...</div>;
  if (!user) return null;

  const role = user.role.role;

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  const allowedScopes = {
    admin: ["public", "campus", "department", "course", "club"],
    hod: ["public", "campus", "department"],
    club_leader: ["public", "campus", "club"],
    student_leader: ["public", "campus", "course"],
  }[role] || [];

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const payload = {
        title: form.title,
        body: form.body,
        category_id: Number(form.category_id),
        scope_level: form.scope_level,
        priority: form.priority,
        visibility: form.visibility,
        department_id: role === "admin" && form.department_id ? Number(form.department_id) : null,
        club_id: form.club_id ? Number(form.club_id) : null,
        course_id: form.course_id ? Number(form.course_id) : null,
        expiry_date: form.expiry_date ? new Date(form.expiry_date).toISOString() : null,
      };

      const notice = await api.post("/notices/", payload);

      for (const file of files) {
        const formData = new FormData();
        formData.append("file", file);
        await api.post(`/notices/${notice.id}/attachments/`, formData);
      }

      navigate(`/notices/${notice.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (allowedScopes.length === 0) {
    return (
      <div className="max-w-xl mx-auto p-8 text-center text-gray-500">
        You don't have permission to post notices.
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto p-4">
      <h1 className="text-xl font-semibold mb-4">Post a Notice</h1>
      {error && <p className="text-red-600 text-sm mb-3">{error}</p>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Title"
          required
          value={form.title}
          onChange={(e) => updateField("title", e.target.value)}
          className="w-full border rounded px-3 py-2"
        />

        <textarea
          placeholder="Body"
          required
          rows={5}
          value={form.body}
          onChange={(e) => updateField("body", e.target.value)}
          className="w-full border rounded px-3 py-2"
        />

        <select
          value={form.category_id}
          onChange={(e) => updateField("category_id", e.target.value)}
          required
          className="w-full border rounded px-3 py-2"
        >
          <option value="">Select category</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>

        <select
          value={form.priority}
          onChange={(e) => updateField("priority", e.target.value)}
          className="w-full border rounded px-3 py-2"
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>

        <select
          value={form.visibility}
          onChange={(e) => updateField("visibility", e.target.value)}
          className="w-full border rounded px-3 py-2"
        >
          <option value="internal">Internal (university only)</option>
          <option value="external">External (public)</option>
        </select>

        <select
          value={form.scope_level}
          onChange={(e) => updateField("scope_level", e.target.value)}
          className="w-full border rounded px-3 py-2"
        >
          {allowedScopes.map((scope) => (
            <option key={scope} value={scope}>
              {scope.charAt(0).toUpperCase() + scope.slice(1)}
            </option>
          ))}
        </select>

        {role === "hod" && form.scope_level === "department" && (
          <p className="text-sm text-gray-500">
            This will be posted under your own department automatically.
          </p>
        )}

        {role === "admin" && form.scope_level === "department" && (
          <select
            value={form.department_id}
            onChange={(e) => updateField("department_id", e.target.value)}
            required
            className="w-full border rounded px-3 py-2"
          >
            <option value="">Select department</option>
            {departments.map((d) => (
              <option key={d.id} value={d.id}>{d.name}</option>
            ))}
          </select>
        )}

        {role === "club_leader" && form.scope_level === "club" && (
          <select
            value={form.club_id}
            onChange={(e) => updateField("club_id", e.target.value)}
            required
            className="w-full border rounded px-3 py-2"
          >
            <option value="">Select your club</option>
            {clubs.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        )}

        {role === "student_leader" && form.scope_level === "course" && (
          <select
            value={form.course_id}
            onChange={(e) => updateField("course_id", e.target.value)}
            required
            className="w-full border rounded px-3 py-2"
          >
            <option value="">Select your course</option>
            {courses.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        )}

        {role === "admin" && form.scope_level === "club" && (
          <select
            value={form.club_id}
            onChange={(e) => updateField("club_id", e.target.value)}
            required
            className="w-full border rounded px-3 py-2"
          >
            <option value="">Select club</option>
            {clubs.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        )}

        {role === "admin" && form.scope_level === "course" && (
          <select
            value={form.course_id}
            onChange={(e) => updateField("course_id", e.target.value)}
            required
            className="w-full border rounded px-3 py-2"
          >
            <option value="">Select course</option>
            {courses.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        )}

        <input
          type="datetime-local"
          value={form.expiry_date}
          onChange={(e) => updateField("expiry_date", e.target.value)}
          className="w-full border rounded px-3 py-2"
        />
        <input
          type="file"
          multiple
          onChange={(e) => setFiles(Array.from(e.target.files))}
          className="w-full border rounded px-3 py-2"
        />

        <button
          type="submit"
          disabled={submitting}
          className="w-full bg-blue-600 text-white rounded py-2 disabled:opacity-50"
        >
          {submitting ? "Posting..." : "Post Notice"}
        </button>
      </form>
    </div>
  );
}
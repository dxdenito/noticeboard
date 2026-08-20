import { useState, useEffect } from "react";
import { api } from "../../api/client";
import { useToast } from "../../context/ToastContext";

export default function ManageCourses(){
        const [courses, setCourses] = useState([]);
        const [departments, setDepartments] = useState([]);
        const [loading, setLoading] = useState(true);
        const [form, setForm] = useState({ name: "",code:"", department_id: "" });
        const [submitting, setSubmitting] = useState(false);
        const { showError, showSuccess } = useToast();

        async function loadCourses() {
            try {
            const data = await api.get("/courses/");
            setCourses(data);
            } catch (err) {
            showError(err.message);
            } finally {
            setLoading(false);
            }
        }
        async function loadDepartments(){
            try{
                const data = await api.get("/departments/");
                setDepartments(data);
            }catch (err){
                showError(err.message);
            }
        }

        useEffect(() => {
            loadCourses();
            loadDepartments();
        }, []);

        async function handleDelete(id) {
            if (!confirm("Delete this course? This cannot be undone.")) return;
            try {
                await api.delete(`/courses/${id}`);
                showSuccess("Course deleted");
                loadCourses();
            } catch (err) {
                showError(err.message);
            }
        }

        async function handleSubmit(e) {
            e.preventDefault();
            setSubmitting(true);
            const parsedId = parseInt(form.department_id, 10);
            const payload = {
                ...form,
                department_id: isNaN(parsedId) ? null : parsedId // Falls back to null if empty
            };
            try {
            await api.post("/courses/", payload);
            showSuccess("Course created");
            setForm({ name: "", code: "", department_id:"" });
            loadCourses();
            } catch (err) {
            showError(err.message);
            } finally {
            setSubmitting(false);
            }
        }
        async function handleClearMembers(id) {
            if (!confirm("Remove all members from this course?")) return;
            try {
                await api.patch(`/courses/${id}/remove-all-enrollments`);
                showSuccess("Members removed");
            } catch (err) {
                showError(err.message);
            }
        }


        if (loading) return <div className="p-8 text-center">Loading...</div>;
    return(

            <div className="max-w-2xl mx-auto p-4">
                <h1 className="text-xl font-semibold mb-4">Manage Courses</h1>
                <form onSubmit={handleSubmit} className="bg-white p-4 rounded   mb-6 flex gap-2">
                    <input
                    type="text"
                    placeholder="Name"
                    required
                    value={form.name}
                    onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                    className="flex-1 bg-jkuat-green/20 rounded px-3 py-2"
                    />
                    <input
                    type="text"
                    placeholder="code"
                    required
                    value={form.code}
                    onChange={(e) => setForm((f) => ({ ...f, code: e.target.value }))}
                    className="w-24 bg-jkuat-green/20 rounded px-3 py-2"
                    />
                    <select
                        required
                        value={form.department_id}
                        onChange={(e) => setForm((f) => ({ ...f, department_id: e.target.value }))}
                        className="w-24 bg-jkuat-green/20 rounded px-3 py-2"
                        >
                        <option value="">Select department</option>
                        {departments.map((d) => (
                            <option key={d.id} value={d.id}>{d.name}</option>
                        ))}
                    </select>
                    <button
                    type="submit"
                    disabled={submitting}
                    className="bg-jkuat-green text-white px-4 py-2 rounded disabled:opacity-50"
                    >
                    Add
                    </button>
                </form>
                <div className="bg-white rounded ">
                    <table className="w-full text-sm">
                    <thead className="border-b bg-gray-50">
                    <tr>
                        <th className="text-left p-3">Name</th>
                        <th className="text-left p-3">code</th>
                        <th className="text-left p-3">department</th>
                        <th className="text-left p-3">Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {courses.map((c) => (
                        <tr key={c.id} className="border-b last:border-0">
                        <td className="p-3">{c.name}</td>
                        <td className="p-3">{c.code}</td>
                        <td className="p-3">{c.department?.name ?? c.department_id}</td>
                        <td className="p-3 flex gap-2">
                            <button onClick={() => handleClearMembers(c.id)} className="text-xs text-gray-600 underline">
                            Clear Enrollments
                            </button>
                            <button onClick={() => handleDelete(c.id)} className="text-red-600 text-xs">
                            Delete
                            </button>
                        </td>
                        </tr>
                    ))}
                    </tbody>
                    </table>
                </div>
            </div>
  
    )
}
import { useState, useEffect } from "react";
import { api } from "../../api/client";
import { useToast } from "../../context/ToastContext";

export default function ManageClubs(){
      const [clubs, setClubs] = useState([]);
        const [loading, setLoading] = useState(true);
        const [form, setForm] = useState({ name: "", description: "" });
        const [submitting, setSubmitting] = useState(false);
        const { showError, showSuccess } = useToast();

        async function loadClubs() {
            try {
            const data = await api.get("/clubs/");
            setClubs(data);
            } catch (err) {
            showError(err.message);
            } finally {
            setLoading(false);
            }
        }

        useEffect(() => {
            loadClubs();
        }, []);

        async function handleDelete(id) {
            if (!confirm("Delete this club? This cannot be undone.")) return;
            try {
                await api.delete(`/clubs/${id}`);
                showSuccess("club deleted");
                loadClubs();
            } catch (err) {
                showError(err.message);
            }
        }

        async function handleSubmit(e) {
            e.preventDefault();
            setSubmitting(true);
            try {
            await api.post("/clubs/", form);
            showSuccess("Club created");
            setForm({ name: "", description: "" });
            loadClubs();
            } catch (err) {
            showError(err.message);
            } finally {
            setSubmitting(false);
            }
        }
        async function handleClearMembers(id) {
            if (!confirm("Remove all members from this club?")) return;
            try {
                await api.patch(`/clubs/${id}/remove-all-members`);
                showSuccess("Members removed");
            } catch (err) {
                showError(err.message);
            }
        }


        if (loading) return <div className="p-8 text-center">Loading...</div>;
    return(

            <div className="max-w-2xl mx-auto p-4">
                <h1 className="text-xl font-semibold mb-4">Manage clubs</h1>
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
                    placeholder="description"
                    required
                    value={form.code}
                    onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
                    className="w-24 bg-jkuat-green/20 rounded px-3 py-2"
                    />
                    <button
                    type="submit"
                    disabled={submitting}
                    className="bg-jkuat-green text-white px-4 py-2 rounded disabled:opacity-50"
                    >
                    Add
                    </button>
                </form>
                <div className="bg-white rounded shadow-sm border">
                    <table className="w-full text-sm">
                    <thead className="border-b bg-gray-50">
                    <tr>
                        <th className="text-left p-3">Name</th>
                        <th className="text-left p-3">Description</th>
                        <th className="text-left p-3">Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {clubs.map((c) => (
                        <tr key={c.id} className="border-b last:border-0">
                        <td className="p-3">{c.name}</td>
                        <td className="p-3">{c.description}</td>
                        <td className="p-3 flex gap-2">
                            <button onClick={() => handleClearMembers(c.id)} className="text-xs text-gray-600 underline">
                            Clear Members
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
import { useState, useEffect } from "react";
import { api } from "../../api/client";
import { useToast } from "../../context/ToastContext";

export default function ManageCategories(){
      const [categories, setCategories] = useState([]);
        const [loading, setLoading] = useState(true);
        const [form, setForm] = useState({ name: "" });
        const [submitting, setSubmitting] = useState(false);
        const { showError, showSuccess } = useToast();

        async function loadCategories() {
            try {
            const data = await api.get("/categories/");
            setCategories(data);
            } catch (err) {
            showError(err.message);
            } finally {
            setLoading(false);
            }
        }

        useEffect(() => {
            loadCategories();
        }, []);

        async function handleSubmit(e) {
            e.preventDefault();
            setSubmitting(true);
            try {
            await api.post("/categories/", form);
            showSuccess("Category created");
            setForm({ name: "", description: "" });
            loadCategories();
            } catch (err) {
            showError(err.message);
            } finally {
            setSubmitting(false);
            }
        }

        if (loading) return <div className="p-8 text-center">Loading...</div>;
    return(

            <div className="max-w-2xl mx-auto p-4">
                <h1 className="text-xl font-semibold mb-4">Manage categories</h1>
                <form onSubmit={handleSubmit} className="bg-white p-4 rounded   mb-6 flex gap-2">
                    <input
                    type="text"
                    placeholder="Name"
                    required
                    value={form.name}
                    onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                    className="flex-1 bg-jkuat-green/20 rounded px-3 py-2"
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
                        
                        </tr>
                    </thead>
                    <tbody>
                        {categories.map((c) => (
                        <tr key={c.id} className="border-b last:border-0">
                            <td className="p-3">{c.name}</td>
                        </tr>
                        ))}
                    </tbody>
                    </table>
                </div>
            </div>
  
    )
}
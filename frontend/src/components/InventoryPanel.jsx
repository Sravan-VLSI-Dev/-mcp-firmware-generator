import React from "react";

export default function InventoryPanel({
  products,
  filteredProducts,
  filter,
  setFilter,
  form,
  editId,
  loading,
  message,
  error,
  handleChange,
  handleSubmit,
  handleEdit,
  handleDelete,
  handleSort,
  sortField,
  sortDirection,
  resetForm
}) {
  const currency = (n) =>
    typeof n === "number" ? n.toFixed(2) : Number(n || 0).toFixed(2);

  return (
    <section id="inventory" className="mx-auto w-full max-w-6xl px-6 py-16">
      <div className="mb-8 flex flex-col gap-4">
        <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Inventory Control</div>
        <h2 className="text-3xl font-semibold text-white">Firmware asset registry</h2>
        <p className="max-w-2xl text-slate-400">
          Manage firmware components with MCP-aware metadata, quantities, and pricing telemetry.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="card-glass rounded-3xl p-6">
          <h3 className="text-lg font-semibold text-white">{editId ? "Edit component" : "Register component"}</h3>
          <form onSubmit={handleSubmit} className="mt-4 grid gap-3">
            <input
              type="number"
              name="id"
              placeholder="ID"
              value={form.id}
              onChange={handleChange}
              required
              disabled={!!editId}
              className="rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-sm text-white outline-none focus:border-cyan-500/40"
            />
            <input
              type="text"
              name="name"
              placeholder="Name"
              value={form.name}
              onChange={handleChange}
              required
              className="rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-sm text-white outline-none focus:border-cyan-500/40"
            />
            <input
              type="text"
              name="description"
              placeholder="Description"
              value={form.description}
              onChange={handleChange}
              required
              className="rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-sm text-white outline-none focus:border-cyan-500/40"
            />
            <div className="grid gap-3 md:grid-cols-2">
              <input
                type="number"
                name="price"
                placeholder="Price"
                value={form.price}
                onChange={handleChange}
                required
                step="0.01"
                className="rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-sm text-white outline-none focus:border-cyan-500/40"
              />
              <input
                type="number"
                name="quantity"
                placeholder="Quantity"
                value={form.quantity}
                onChange={handleChange}
                required
                className="rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-sm text-white outline-none focus:border-cyan-500/40"
              />
            </div>
            <div className="mt-2 flex flex-wrap gap-3">
              <button
                className="rounded-xl bg-gradient-to-r from-indigo-500 via-cyan-400 to-indigo-500 px-4 py-3 text-xs font-semibold uppercase tracking-[0.3em] text-slate-950"
                type="submit"
                disabled={loading}
              >
                {editId ? "Update" : "Add"}
              </button>
              {editId && (
                <button
                  className="rounded-xl border border-slate-700 px-4 py-3 text-xs uppercase tracking-[0.3em] text-slate-300"
                  type="button"
                  onClick={() => {
                    resetForm();
                  }}
                >
                  Cancel
                </button>
              )}
            </div>
          </form>
          {message && <div className="mt-4 rounded-xl border border-cyan-500/40 bg-cyan-500/10 px-4 py-3 text-sm text-cyan-200">{message}</div>}
          {error && <div className="mt-4 rounded-xl border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">{error}</div>}
        </div>

        <div className="card-glass rounded-3xl p-6">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <div className="text-sm uppercase tracking-[0.3em] text-slate-500">Inventory</div>
            <div className="rounded-full border border-slate-700 px-3 py-1 text-xs text-slate-400">
              Total: {products.length}
            </div>
            <input
              type="text"
              placeholder="Search by id, name, description"
              value={filter}
              onChange={(event) => setFilter(event.target.value)}
              className="w-full rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-2 text-sm text-white outline-none focus:border-cyan-500/40 md:w-64"
            />
          </div>
          <div className="scrollbar-hidden overflow-x-auto">
            <table className="min-w-[640px] text-left text-sm text-slate-300">
              <thead className="text-xs uppercase tracking-[0.2em] text-slate-500">
                <tr>
                  {[
                    { key: "id", label: "ID" },
                    { key: "name", label: "Name" },
                    { key: "description", label: "Description" },
                    { key: "price", label: "Price" },
                    { key: "quantity", label: "Qty" }
                  ].map((col) => (
                    <th
                      key={col.key}
                      className="cursor-pointer px-3 py-3"
                      onClick={() => handleSort(col.key)}
                    >
                      {col.label}
                      {sortField === col.key && (sortDirection === "asc" ? " ?" : " ?")}
                    </th>
                  ))}
                  <th className="px-3 py-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={6} className="px-3 py-8 text-center text-slate-500">
                      Loading...
                    </td>
                  </tr>
                ) : (
                  filteredProducts.map((p) => (
                    <tr key={p.id} className="border-t border-slate-800/60">
                      <td className="px-3 py-3 text-slate-200">{p.id}</td>
                      <td className="px-3 py-3 text-white">{p.name}</td>
                      <td className="px-3 py-3 text-slate-400">{p.description}</td>
                      <td className="px-3 py-3 text-cyan-200">${currency(p.price)}</td>
                      <td className="px-3 py-3">
                        <span className="rounded-full border border-slate-700 px-3 py-1 text-xs text-slate-300">
                          {p.quantity}
                        </span>
                      </td>
                      <td className="px-3 py-3">
                        <div className="flex gap-2">
                          <button
                            className="rounded-lg border border-slate-700 px-3 py-1 text-xs uppercase tracking-[0.2em] text-slate-300"
                            onClick={() => handleEdit(p)}
                          >
                            Edit
                          </button>
                          <button
                            className="rounded-lg border border-rose-500/40 px-3 py-1 text-xs uppercase tracking-[0.2em] text-rose-200"
                            onClick={() => handleDelete(p.id)}
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
                {!loading && filteredProducts.length === 0 && (
                  <tr>
                    <td colSpan={6} className="px-3 py-8 text-center text-slate-500">
                      No components found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}

from flask import Flask, redirect, render_template_string, request, url_for

from .manager import AssetManager

HTML_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Asset Pro</title>
    <style>
      :root {
        color-scheme: light;
        --bg: #f4f7fb;
        --card: #ffffff;
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --accent: #38bdf8;
        --text: #0f172a;
        --muted: #64748b;
        --border: #e2e8f0;
        --shadow: 0 12px 40px rgba(15, 23, 42, 0.08);
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: "Segoe UI", Arial, sans-serif;
        background:
          radial-gradient(circle at top left, rgba(56, 189, 248, 0.18), transparent 22%),
          linear-gradient(135deg, #eef6ff, var(--bg));
        color: var(--text);
      }
      .page {
        max-width: 1280px;
        margin: 0 auto;
        padding: 36px 20px 56px;
      }
      .hero {
        background: linear-gradient(135deg, var(--primary), var(--accent));
        color: white;
        padding: 28px 30px;
        border-radius: 24px;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
      }
      .hero::after {
        content: "";
        position: absolute;
        inset: auto -20px -40px auto;
        width: 180px;
        height: 180px;
        background: rgba(255,255,255,0.16);
        border-radius: 50%;
      }
      .hero h1 { margin: 0 0 8px; font-size: 2.1rem; }
      .hero p { margin: 0; opacity: 0.95; font-size: 1rem; }
      .grid { display: grid; grid-template-columns: minmax(300px, 0.9fr) 1.4fr; gap: 22px; margin-top: 22px; }
      .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 22px;
        box-shadow: var(--shadow);
      }
      .card h2 { margin-top: 0; margin-bottom: 14px; font-size: 1.12rem; }
      form { display: grid; gap: 10px; }
      .row { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
      input, select, button {
        border-radius: 12px;
        border: 1px solid var(--border);
        padding: 10px 12px;
        font-size: 0.95rem;
        transition: all 0.2s ease;
      }
      input:focus, select:focus {
        outline: none;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        border-color: var(--primary);
      }
      button {
        background: linear-gradient(135deg, var(--primary), var(--accent));
        color: white;
        cursor: pointer;
        border: none;
        font-weight: 700;
        box-shadow: 0 8px 16px rgba(37, 99, 235, 0.16);
      }
      button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2);
      }
      .secondary {
        background: #f1f5f9;
        color: var(--text);
        box-shadow: none;
      }
      .secondary:hover {
        background: #e2e8f0;
        transform: none;
        box-shadow: none;
      }
      table { width: 100%; border-collapse: collapse; margin-top: 8px; }
      th, td { padding: 12px; border-bottom: 1px solid var(--border); text-align: left; }
      th { color: var(--muted); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em; }
      .actions { display: flex; flex-direction: column; gap: 8px; }
      .actions form { display: inline-block; margin: 0; }
      .badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 999px;
        background: #dbeafe;
        color: var(--primary-dark);
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: capitalize;
      }
      .muted { color: var(--muted); }
      @media (max-width: 900px) {
        .grid { grid-template-columns: 1fr; }
      }
    </style>
  </head>
  <body>
    <div class="page">
      <div class="hero">
        <h1>Asset Pro</h1>
        <p>Track and manage your assets with a clean, modern workspace.</p>
      </div>

      <div class="grid">
        <div class="card">
          <h2>Add New Asset</h2>
          <form method="post" action="/assets">
            <input name="name" placeholder="Name" required>
            <input name="category" placeholder="Category" required>
            <input name="value" type="number" step="0.01" placeholder="Value" required>
            <select name="status">
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
            <button type="submit">Save Asset</button>
          </form>
        </div>

        <div class="card">
          <h2>Assets</h2>
          {% if assets %}
            <table>
              <tr><th>ID</th><th>Name</th><th>Category</th><th>Value</th><th>Status</th><th>Actions</th></tr>
              {% for asset in assets %}
                <tr>
                  <td><span class="badge">{{ asset.id }}</span></td>
                  <td>{{ asset.name }}</td>
                  <td>{{ asset.category }}</td>
                  <td>${{ "%.2f"|format(asset.value) }}</td>
                  <td><span class="badge">{{ asset.status }}</span></td>
                  <td class="actions">
                    <form method="post" action="/assets/{{ asset.id }}/update">
                      <div class="row">
                        <input name="name" value="{{ asset.name }}" size="8">
                        <input name="category" value="{{ asset.category }}" size="8">
                        <input name="value" type="number" step="0.01" value="{{ asset.value }}" size="6">
                        <select name="status">
                          <option value="active" {% if asset.status == 'active' %}selected{% endif %}>Active</option>
                          <option value="inactive" {% if asset.status == 'inactive' %}selected{% endif %}>Inactive</option>
                        </select>
                        <button type="submit">Update</button>
                      </div>
                    </form>
                    <form method="post" action="/assets/{{ asset.id }}/delete">
                      <button class="secondary" type="submit">Delete</button>
                    </form>
                  </td>
                </tr>
              {% endfor %}
            </table>
          {% else %}
            <p class="muted">No assets found.</p>
          {% endif %}
        </div>
      </div>
    </div>
  </body>
</html>
"""


def create_app(storage_path=None):
    app = Flask(__name__)
    manager = AssetManager(storage_path=storage_path)

    def get_asset(asset_ref):
        assets = manager.list_assets()
        if asset_ref.isdigit():
            index = int(asset_ref) - 1
            if 0 <= index < len(assets):
                return assets[index]
        for asset in assets:
            if asset.id == asset_ref:
                return asset
        return None

    @app.get("/")
    def index():
        assets = manager.list_assets()
        return render_template_string(HTML_TEMPLATE, assets=assets)

    @app.post("/assets")
    def add_asset():
        manager.add_asset(
            name=request.form["name"],
            category=request.form["category"],
            value=float(request.form["value"]),
            status=request.form.get("status", "active"),
        )
        return redirect(url_for("index"))

    @app.post("/assets/<asset_ref>/update")
    def update_asset(asset_ref):
        asset = get_asset(asset_ref)
        if asset is None:
            return redirect(url_for("index"))

        manager.update_asset(
            asset.id,
            name=request.form["name"],
            category=request.form["category"],
            value=float(request.form["value"]),
            status=request.form.get("status", "active"),
        )
        return redirect(url_for("index"))

    @app.post("/assets/<asset_ref>/delete")
    def delete_asset(asset_ref):
        asset = get_asset(asset_ref)
        if asset is not None:
            manager.delete_asset(asset.id)
        return redirect(url_for("index"))

    return app


app = create_app()

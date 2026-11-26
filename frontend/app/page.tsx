"use client";

import { useEffect, useState } from "react";

type Incident = {
  id: number; service: string; metric: string; severity: string;
  title: string; description: string; status: string; created_at: string;
};

type Service = { service: string; event_count: number; last_seen: string; error_events: number };

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export default function Dashboard() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [services, setServices] = useState<Service[]>([]);
  const [error, setError] = useState("");

  async function refresh() {
    try {
      const [incidentResponse, serviceResponse] = await Promise.all([
        fetch(`${API}/api/v1/incidents`, { cache: "no-store" }),
        fetch(`${API}/api/v1/services`, { cache: "no-store" })
      ]);
      if (!incidentResponse.ok || !serviceResponse.ok) throw new Error("API request failed");
      setIncidents(await incidentResponse.json());
      setServices(await serviceResponse.json());
      setError("");
    } catch {
      setError("Cannot reach the API. Start the backend at http://127.0.0.1:8000.");
    }
  }

  useEffect(() => {
    refresh();
    const timer = window.setInterval(refresh, 10000);
    return () => window.clearInterval(timer);
  }, []);

  async function updateStatus(id: number, status: string) {
    await fetch(`${API}/api/v1/incidents/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status })
    });
    refresh();
  }

  const openCount = incidents.filter(item => item.status !== "resolved").length;
  const eventCount = services.reduce((sum, item) => sum + item.event_count, 0);

  return (
    <main className="shell">
      <header className="topbar">
        <div><div className="eyebrow">OBSERVABILITY PLATFORM</div><h1>TraceForge <span>AI</span></h1></div>
        <div className="live"><i /> LIVE OVERVIEW</div>
      </header>

      <section className="intro">
        <div><p className="eyebrow">COMMAND CENTER</p><h2>Application health at a glance.</h2>
          <p className="muted">Monitor telemetry, surface anomalies, and manage incidents.</p></div>
        <button onClick={refresh}>Refresh data ↻</button>
      </section>

      {error && <div className="notice">{error}</div>}

      <section className="metrics">
        <article className="metric-card"><p>MONITORED SERVICES</p><strong>{services.length}</strong><small>Reporting services</small></article>
        <article className="metric-card"><p>TELEMETRY EVENTS</p><strong>{eventCount.toLocaleString()}</strong><small>Stored measurements</small></article>
        <article className="metric-card"><p>ACTIVE INCIDENTS</p><strong>{openCount}</strong><small>Require attention</small></article>
        <article className="metric-card"><p>DETECTED INCIDENTS</p><strong>{incidents.length}</strong><small>All recorded incidents</small></article>
      </section>

      <section className="panel">
        <div className="panel-heading"><div><p className="eyebrow">OPERATIONS</p><h3>Service inventory</h3></div><span>{services.length} services</span></div>
        {services.length === 0 ? <p className="empty">No telemetry received yet. Send a metric to the ingestion API to get started.</p> :
          <div className="table-wrap"><table><thead><tr><th>Service</th><th>Events</th><th>Error metrics</th><th>Last seen</th></tr></thead>
            <tbody>{services.map(service => <tr key={service.service}><td className="service-name">{service.service}</td><td>{service.event_count}</td><td>{service.error_events}</td><td>{new Date(service.last_seen).toLocaleString()}</td></tr>)}</tbody></table></div>}
      </section>

      <section className="panel">
        <div className="panel-heading"><div><p className="eyebrow">DETECTION ENGINE</p><h3>Incident queue</h3></div><span>{openCount} active</span></div>
        {incidents.length === 0 ? <p className="empty">No incidents detected. The system will create an incident when incoming telemetry deviates from its baseline.</p> :
          <div className="incident-list">{incidents.map(item => <article className="incident" key={item.id}>
            <div className="incident-main"><div className="incident-meta"><b className={item.severity}>{item.severity}</b><span>{item.service}</span><span>{new Date(item.created_at).toLocaleString()}</span></div>
              <h4>{item.title}</h4><p>{item.description}</p></div>
            <select value={item.status} onChange={event => updateStatus(item.id, event.target.value)} aria-label={`Status for incident ${item.id}`}>
              <option value="open">Open</option><option value="investigating">Investigating</option><option value="resolved">Resolved</option>
            </select>
          </article>)}</div>}
      </section>
      <footer>TraceForge AI <span>•</span> Application observability and incident intelligence</footer>
    </main>
  );
}

import { useState, useEffect } from "react";

const API_URL = "http://localhost:8000/api";

export default function App() {
  // ====================== STATE ======================
  const [phase, setPhase] = useState("phase_1");
  const [activeTab, setActiveTab] = useState("dashboard");
  const [company, setCompany] = useState("");
  const [goal, setGoal] = useState("");
  const [loading, setLoading] = useState(false);

  // Real-time data state
  const [leads, setLeads] = useState([]);
  const [pipeline, setPipeline] = useState(null);
  const [campaigns, setCampaigns] = useState([]);
  const [swarmStatus, setSwarmStatus] = useState({
    prospectorDeals: 0,
    outreachDeals: 0,
    discoveryDeals: 0,
    negotiationDeals: 0,
    health: 0,
  });
  const [activities, setActivities] = useState([]);
  const [scaleFactor, setScaleFactor] = useState(1);
  const [logs, setLogs] = useState([]);
  const [result, setResult] = useState(null);

  // Load real data on mount
  useEffect(() => {
    const loadData = async () => {
      try {
        // Load pipeline data
        const pipelineRes = await fetch(`${API_URL}/analytics/pipeline`);
        if (pipelineRes.ok) {
          setPipeline(await pipelineRes.json());
        }
      } catch (err) {
        console.log("Pipeline API not available");
      }

      try {
        // Load leads data
        const leadsRes = await fetch(`${API_URL}/prospecting/find-leads`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ limit: 10 }),
        });
        if (leadsRes.ok) {
          const data = await leadsRes.json();
          setLeads(data.leads || []);
        }
      } catch (err) {
        console.log("Leads API not available");
      }
    };

    loadData();
  }, []);

  // ====================== API CALLS ======================

  const runFullCampaign = async () => {
    if (!company.trim() || !goal.trim()) return;
    setLoading(true);
    setLogs([]);
    try {
      const res = await fetch(`${API_URL}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ company, goal }),
      });
      const data = await res.json();
      const newLogs = data.logs || ["✅ Campaign executed"];
      setLogs(newLogs);
      setActivities((prev) => [
        { time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }), action: "🚀 Campaign started", icon: "⚡" },
        ...prev.slice(0, 4),
      ]);
      setResult(data);
      // Reload leads if campaign returned any
      if (data.leads) setLeads((prev) => [...prev, ...data.leads]);
    } catch (err) {
      setLogs(["❌ Campaign failed. Backend running?"]);
    } finally {
      setLoading(false);
    }
  };

  const findLeads = async () => {
    setLoading(true);
    setLogs([]);
    try {
      const res = await fetch(`${API_URL}/prospecting/find-leads`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ company_name: company, limit: 50 }),
      });
      const data = await res.json();
      setLogs(data.logs || ["✅ Leads found"]);
      if (data.leads) {
        setLeads(data.leads);
        setActivities((prev) => [
          { time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }), action: `🔍 Found ${data.leads.length} leads`, icon: "✅" },
          ...prev.slice(0, 4),
        ]);
      }
      setResult(data);
    } catch (err) {
      setLogs(["❌ Lead discovery failed"]);
    } finally {
      setLoading(false);
    }
  };

  const getPipelineMetrics = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/analytics/pipeline`);
      const data = await res.json();
      setPipeline(data || pipeline);
      setLogs(["✅ Pipeline metrics loaded"]);
      setActivities((prev) => [
        { time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }), action: "📊 Pipeline updated", icon: "✅" },
        ...prev.slice(0, 4),
      ]);
    } catch (err) {
      setLogs(["❌ Pipeline fetch failed"]);
    } finally {
      setLoading(false);
    }
  };

  const scaleSwarm = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/swarm/scale?multiplier=${scaleFactor}`, { method: "POST" });
      const data = await res.json();
      setSwarmStatus((prev) => ({ ...prev, health: 94 }));
      setLogs([
        `🚀 Scaled to ${scaleFactor}x`,
        `📊 New capacity: ${data.monthly_lead_capacity}`,
        `💰 Revenue increase: ${data.expected_revenue_increase}`,
      ]);
      setActivities((prev) => [
        { time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }), action: `🚀 Scaled to ${scaleFactor}x capacity`, icon: "⚡" },
        ...prev.slice(0, 4),
      ]);
    } catch (err) {
      setLogs(["❌ Scaling failed"]);
    } finally {
      setLoading(false);
    }
  };

  // ====================== RENDER ======================

  return (
    <div style={styles.app}>
      {/* Header */}
      <div style={styles.header}>
        <h1 style={styles.logo}>⚡ FlowForge</h1>
        <p style={styles.tagline}>AI-powered agentic sales system</p>
        <div style={styles.phaseSelector}>
          <button style={phase === "phase_1" ? styles.phaseButtonActive : styles.phaseButton} onClick={() => { setPhase("phase_1"); setActiveTab("dashboard"); }}>Phase 1: 4th Teammate</button>
          <button style={phase === "phase_2" ? styles.phaseButtonActive : styles.phaseButton} onClick={() => { setPhase("phase_2"); setActiveTab("swarm"); }}>Phase 2: Full Autonomy</button>
        </div>
      </div>

      {/* Navigation */}
      <div style={styles.navContainer}>
        <div style={styles.tabNav}>
          {phase === "phase_1" ? (
            <>
              <NavTab active={activeTab === "dashboard"} onClick={() => setActiveTab("dashboard")}>📊 Dashboard</NavTab>
              <NavTab active={activeTab === "leads"} onClick={() => setActiveTab("leads")}>🔍 Leads</NavTab>
              <NavTab active={activeTab === "campaigns"} onClick={() => setActiveTab("campaigns")}>📧 Campaigns</NavTab>
              <NavTab active={activeTab === "pipeline"} onClick={() => setActiveTab("pipeline")}>📈 Pipeline</NavTab>
            </>
          ) : (
            <>
              <NavTab active={activeTab === "swarm"} onClick={() => setActiveTab("swarm")}>🐝 Swarm</NavTab>
              <NavTab active={activeTab === "scaling"} onClick={() => setActiveTab("scaling")}>📈 Scaling</NavTab>
              <NavTab active={activeTab === "roi"} onClick={() => setActiveTab("roi")}>💰 ROI</NavTab>
              <NavTab active={activeTab === "experiments"} onClick={() => setActiveTab("experiments")}>🧪 Experiments</NavTab>
            </>
          )}
          <NavTab active={activeTab === "activity"} onClick={() => setActiveTab("activity")}>📡 Activity</NavTab>
        </div>
      </div>

      {/* Main Layout: Content + Activity Sidebar */}
      <div style={styles.mainLayout}>
        {/* Content Area */}
        <div style={styles.contentArea}>
          {/* PHASE 1 */}
          {phase === "phase_1" && activeTab === "dashboard" && (
            <GlassCard title="🎯 Quick Start" subtitle="Run a complete sales campaign">
              <div style={styles.form}>
                <input style={styles.input} placeholder="Company name..." value={company} onChange={(e) => setCompany(e.target.value)} />
                <textarea style={styles.textarea} placeholder="Business goal..." value={goal} onChange={(e) => setGoal(e.target.value)} rows={3} />
                <div style={styles.btnGroup}>
                  <ActionButton primary onClick={runFullCampaign} disabled={loading}>{loading ? "⏳ Running..." : "🚀 Run Campaign"}</ActionButton>
                  <ActionButton onClick={findLeads} disabled={loading}>{loading ? "⏳ Searching..." : "🔍 Find Leads"}</ActionButton>
                  <ActionButton onClick={getPipelineMetrics} disabled={loading}>{loading ? "⏳ Loading..." : "📊 Pipeline"}</ActionButton>
                </div>
              </div>
              {logs.length > 0 && <div style={styles.logs}>{logs.map((l, i) => <div key={i} style={styles.logLine}>{l}</div>)}</div>}
              <StatsGrid items={[
                { label: "Total Leads", value: leads.length },
                { label: "Pipeline", value: pipeline ? `$${(pipeline.total_pipeline / 1000).toFixed(0)}K` : "—" },
                { label: "This Month", value: pipeline ? `$${(pipeline.closing_this_month / 1000).toFixed(0)}K` : "—" },
                { label: "Health", value: "94%" },
              ]} />
            </GlassCard>
          )}

          {phase === "phase_1" && activeTab === "leads" && (
            <GlassCard title="🔍 Lead Prospecting" subtitle="Real-time lead discovery engine">
              <ActionButton primary onClick={findLeads} disabled={loading} style={{ marginBottom: "20px" }}>{loading ? "🔄 Searching..." : "🚀 Start Prospecting"}</ActionButton>
              {leads.length > 0 ? (
                <div style={styles.leadsGrid}>
                  {leads.map((lead) => (
                    <LeadCard key={lead.id || lead.name} lead={lead} />
                  ))}
                </div>
              ) : (
                <p style={{ color: "#888", textAlign: "center", padding: "40px 20px" }}>Click "Start Prospecting" to load leads from Apollo</p>
              )}
            </GlassCard>
          )}

          {phase === "phase_1" && activeTab === "campaigns" && (
            <GlassCard title="📧 Campaign Results" subtitle="From run campaign">
              {result?.emails || result?.campaigns || result?.tasks ? (
                <>
                  {result.tasks && (
                    <div style={{ marginBottom: "20px" }}>
                      <h4 style={{ color: "#a78bfa" }}>📋 Tasks</h4>
                      <ul style={{ color: "#888" }}>
                        {result.tasks.map((task, i) => <li key={i}>{task}</li>)}
                      </ul>
                    </div>
                  )}
                  {result.emails && (
                    <div>
                      <h4 style={{ color: "#a78bfa" }}>✉️ Email Sequence</h4>
                      {result.emails.email_1 && <EmailCard title="Email 1" email={result.emails.email_1} />}
                      {result.emails.email_2 && <EmailCard title="Email 2" email={result.emails.email_2} />}
                      {result.emails.email_3 && <EmailCard title="Email 3" email={result.emails.email_3} />}
                    </div>
                  )}
                </>
              ) : (
                <p style={{ color: "#888", textAlign: "center", padding: "40px 20px" }}>Run a campaign first to see results here</p>
              )}
            </GlassCard>
          )}

          {phase === "phase_1" && activeTab === "pipeline" && (
            <GlassCard title="📈 Sales Pipeline" subtitle="Track deals by stage">
              {pipeline ? (
                <>
                  <StatsGrid items={[
                    { label: "Total Pipeline", value: `$${(pipeline.total_pipeline / 1000).toFixed(0)}K` },
                    { label: "Weighted Forecast", value: `$${(pipeline.weighted_forecast / 1000).toFixed(0)}K` },
                    { label: "This Month", value: `$${(pipeline.closing_this_month / 1000).toFixed(0)}K` },
                  ]} />
                  <div style={styles.stagesGrid}>
                    {Object.entries(pipeline.by_stage || {}).map(([stage, info]) => (
                      <StageCard key={stage} stage={stage} count={info.count} value={info.value} />
                    ))}
                  </div>
                </>
              ) : (
                <div style={{ textAlign: "center", padding: "40px 20px", color: "#888" }}>
                  <p>Click "Pipeline" on dashboard to load pipeline data</p>
                  <ActionButton onClick={getPipelineMetrics} disabled={loading} style={{ width: "200px", margin: "0 auto" }}>Load Pipeline</ActionButton>
                </div>
              )}
            </GlassCard>
          )}

          {/* PHASE 2 */}
          {phase === "phase_2" && activeTab === "swarm" && (
            <GlassCard title="🐝 Multi-Agent Swarm" subtitle="Full autonomous sales operation">
              <StatsGrid items={[
                { label: "Prospector Deals", value: swarmStatus.prospectorDeals },
                { label: "Outreach Active", value: swarmStatus.outreachDeals },
                { label: "Discovery Calls", value: swarmStatus.discoveryDeals },
                { label: "Closed This Month", value: swarmStatus.negotiationDeals },
              ]} />
              <div style={styles.agentsGrid}>
                <AgentCard name="Prospector" deals={swarmStatus.prospectorDeals} status="running" />
                <AgentCard name="Outreach" deals={swarmStatus.outreachDeals} status="active" />
                <AgentCard name="Discovery" deals={swarmStatus.discoveryDeals} status="running" />
                <AgentCard name="Negotiation" deals={swarmStatus.negotiationDeals} status="active" />
              </div>
            </GlassCard>
          )}

          {phase === "phase_2" && activeTab === "scaling" && (
            <GlassCard title="📈 One-Click Scaling" subtitle="Scale without hiring">
              <p style={{ color: "#888", marginBottom: "16px" }}>Select scaling multiplier</p>
              <div style={styles.scaleButtons}>
                {[1, 5, 10, 50].map((mult) => (
                  <button key={mult} style={scaleFactor === mult ? styles.scaleButtonActive : styles.scaleButton} onClick={() => setScaleFactor(mult)}>{mult}x</button>
                ))}
              </div>
              <ActionButton primary onClick={scaleSwarm} disabled={loading} style={{ marginTop: "20px", width: "100%" }}>🚀 Scale to {scaleFactor}x</ActionButton>
              <StatsGrid items={[
                { label: "Monthly Leads", value: (400 * scaleFactor).toFixed(0) },
                { label: "Expected Deals", value: (25 * scaleFactor).toFixed(0) },
                { label: "Revenue Impact", value: `+$${(1212000 * scaleFactor / 1000).toFixed(0)}K` },
              ]} style={{ marginTop: "24px" }} />
            </GlassCard>
          )}

          {phase === "phase_2" && activeTab === "roi" && (
            <GlassCard title="💰 Economic ROI" subtitle="Agent team vs human team">
              <div style={styles.roiComparison}>
                <div style={styles.roiColumn}>
                  <h3>🤖 Agent Team</h3>
                  <div style={styles.roiRow}><span>Deals/Month:</span><strong>25</strong></div>
                  <div style={styles.roiRow}><span>Monthly Revenue:</span><strong>$1,212,500</strong></div>
                  <div style={styles.roiRow}><span>Cost:</span><strong>$500</strong></div>
                  <div style={{ ...styles.roiRow, borderTop: "2px solid #10b981", color: "#10b981" }}><span>Net Profit:</span><strong>$1,212,000</strong></div>
                </div>
                <div style={styles.roiColumn}>
                  <h3>👥 3-Person Team</h3>
                  <div style={styles.roiRow}><span>Deals/Month:</span><strong>12</strong></div>
                  <div style={styles.roiRow}><span>Monthly Revenue:</span><strong>$420,000</strong></div>
                  <div style={styles.roiRow}><span>Cost:</span><strong>$45,000</strong></div>
                  <div style={{ ...styles.roiRow, borderTop: "2px solid #ef4444", color: "#ef4444" }}><span>Net Profit:</span><strong>$375,000</strong></div>
                </div>
              </div>
              <div style={styles.roiConclusion}>
                <h3>⚡ Automation Advantage</h3>
                <p><strong>+$792,500/month revenue | Cost reduction: 99% | ROI pays in 1st hour</strong></p>
              </div>
            </GlassCard>
          )}

          {phase === "phase_2" && activeTab === "experiments" && (
            <GlassCard title="🧪 A/B Experiments" subtitle="Optimize messaging & timing">
              <div style={styles.experimentsGrid}>
                <ExperimentCard name="Subject Line" variantA="Standard" variantB="Personalized" winner="B" confidence="82%" improvement="+15%" />
                <ExperimentCard name="Email Length" variantA="Long form" variantB="Short" winner="B" confidence="78%" improvement="+12%" />
                <ExperimentCard name="Send Time" variantA="9 AM" variantB="2 PM" winner="B" confidence="85%" improvement="+18%" />
              </div>
            </GlassCard>
          )}

          {activeTab === "activity" && (
            <GlassCard title="📡 Real-Time Activity Feed" subtitle="Latest operations & insights">
              <div style={styles.activityFeed}>
                {activities.map((act, i) => (
                  <div key={i} style={styles.activityItem}>
                    <span style={styles.activityIcon}>{act.icon}</span>
                    <div style={styles.activityContent}>{act.action}</div>
                    <div style={styles.activityTime}>{act.time}</div>
                  </div>
                ))}
              </div>
            </GlassCard>
          )}
        </div>

        {/* Activity Sidebar (Always Visible) */}
        <div style={styles.sidebar}>
          <GlassCard title="📡 Quick Stats" subtitle="Live metrics">
            <div style={styles.quickStats}>
              <Stat label="Active Leads" value={leads.length} icon="👥" color="#a78bfa" />
              <Stat label="Pipeline" value={pipeline ? `$${(pipeline.total_pipeline / 1000000).toFixed(1)}M` : "—"} icon="💰" color="#10b981" />
              <Stat label="This Month" value={pipeline ? `$${(pipeline.closing_this_month / 1000).toFixed(0)}K` : "—"} icon="📈" color="#60a5fa" />
              <Stat label="Swarm Health" value="94%" icon="🐝" color="#f59e0b" />
            </div>
          </GlassCard>

          <div style={styles.spacer} />

          <GlassCard title="⚡ Latest Activity" subtitle="">
            {activities.length > 0 ? (
              <div style={styles.miniActivityFeed}>
                {activities.slice(0, 5).map((act, i) => (
                  <div key={i} style={styles.miniActivityItem}>
                    <span style={styles.miniActivityTime}>{act.time}</span>
                    <span style={styles.miniActivityIcon}>{act.icon}</span>
                    <div style={styles.miniActivityText}>{act.action.substring(0, 50)}...</div>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: "#888", fontSize: "0.85rem" }}>No activity yet. Run a campaign or find leads to start.</p>
            )}
          </GlassCard>
        </div>
      </div>
    </div>
  );
}

/* ====================== COMPONENTS ====================== */

function GlassCard({ title, subtitle, children, style }) {
  return (
    <div style={{ ...styles.glassCard, ...style }}>
      {title && <h2 style={styles.cardTitle}>{title}</h2>}
      {subtitle && <p style={styles.cardSubtitle}>{subtitle}</p>}
      {children}
    </div>
  );
}

function NavTab({ active, children, onClick }) {
  return (
    <button style={active ? styles.navTabActive : styles.navTab} onClick={onClick}>
      {children}
    </button>
  );
}

function ActionButton({ primary, disabled, children, onClick, style }) {
  return (
    <button
      style={{ ...(primary ? styles.btnPrimary : styles.btnSecondary), ...style, opacity: disabled ? 0.5 : 1 }}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}

function Stat({ label, value, icon, color }) {
  return (
    <div style={styles.stat}>
      <div style={{ fontSize: "1.8rem" }}>{icon}</div>
      <div style={styles.statLabel}>{label}</div>
      <div style={{ ...styles.statValue, color }}>{value}</div>
    </div>
  );
}

function LeadCard({ lead }) {
  const fullName = `${lead.first_name} ${lead.last_name}`;
  const scoreColors = { hot: "#ff6b6b", warm: "#ffa500", cold: "#60a5fa" };
  const scoreColor = scoreColors[lead.score?.toLowerCase()] || "#888";
  
  return (
    <div style={styles.leadCard}>
      <div style={styles.leadHeader}>
        <div>
          <h4 style={{ margin: "0 0 4px 0" }}>{fullName}</h4>
          <p style={{ color: "#888", fontSize: "0.8rem", margin: 0 }}>{lead.email}</p>
        </div>
        <span style={{ ...styles.leadScore, backgroundColor: scoreColor }}>{lead.score}</span>
      </div>
      <p style={styles.leadDetail}>{lead.title}</p>
      <p style={{ ...styles.leadDetail, color: "#888" }}>{lead.company_name}</p>
      <div style={styles.leadMeta}>
        <span>📍 {lead.phone || "—"}</span>
        <span>🔗 {lead.source}</span>
      </div>
    </div>
  );
}

function StageCard({ stage, count, value }) {
  return (
    <div style={styles.stageCard}>
      <div style={styles.stageName}>{stage}</div>
      <div style={styles.stageCount}>{count} deals</div>
      <div style={styles.stageValue}>${(value / 1000).toFixed(0)}K</div>
    </div>
  );
}

function AgentCard({ name, deals, status }) {
  const statusColor = status === "running" ? "#10b981" : "#f59e0b";
  return (
    <div style={{ ...styles.agentCard, borderColor: statusColor }}>
      <h4>{name}</h4>
      <p style={styles.agentStatus}>● {status}</p>
      <p style={styles.agentDeals}>{deals} deals</p>
    </div>
  );
}

function ExperimentCard({ name, variantA, variantB, winner, confidence, improvement }) {
  return (
    <div style={styles.experimentCard}>
      <h4>{name}</h4>
      <div style={styles.experimentVariants}>
        <span>A: {variantA}</span>
        <span>B: {variantB}</span>
      </div>
      <div style={styles.experimentResult}>🏆 {winner} wins ({confidence}) <span style={{ color: "#10b981" }}>{improvement}</span></div>
    </div>
  );
}

function EmailCard({ title, email }) {
  return (
    <div style={styles.emailBox}>
      <div style={styles.emailNumber}>{title}</div>
      <p style={styles.emailSubject}>Subject: {email.subject}</p>
      <div style={styles.emailBody}>{email.body}</div>
    </div>
  );
}

function StatsGrid({ items, style }) {
  return (
    <div style={{ ...styles.statsGrid, ...style }}>
      {items.map((item, i) => (
        <div key={i} style={styles.statBox}>
          <div style={styles.statBoxLabel}>{item.label}</div>
          <div style={styles.statBoxValue}>{item.value}</div>
        </div>
      ))}
    </div>
  );
}

/* ====================== STYLES ====================== */
const styles = {
  app: {
    minHeight: "100vh",
    backgroundColor: "#0a0a0a",
    backgroundImage: "linear-gradient(135deg, rgba(167, 139, 250, 0.05) 0%, rgba(96, 165, 250, 0.05) 50%, rgba(52, 211, 153, 0.05) 100%)",
    color: "#f0f0f0",
    fontFamily: "'Segoe UI', 'Segoe UI Symbol', sans-serif",
  },
  header: {
    background: "rgba(15, 15, 15, 0.7)",
    backdropFilter: "blur(10px)",
    borderBottom: "1px solid rgba(167, 139, 250, 0.2)",
    padding: "32px 20px",
    textAlign: "center",
  },
  logo: {
    fontSize: "2rem",
    fontWeight: "800",
    margin: 0,
    background: "linear-gradient(90deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    marginBottom: "8px",
  },
  tagline: { color: "#888", fontSize: "0.9rem", margin: 0, marginBottom: "16px" },
  phaseSelector: { display: "flex", gap: "12px", justifyContent: "center", marginTop: "16px" },
  phaseButton: {
    padding: "8px 16px",
    backgroundColor: "rgba(255, 255, 255, 0.05)",
    border: "1px solid rgba(167, 139, 250, 0.2)",
    borderRadius: "8px",
    color: "#888",
    fontWeight: "600",
    fontSize: "0.85rem",
    cursor: "pointer",
  },
  phaseButtonActive: {
    padding: "8px 16px",
    background: "linear-gradient(90deg, #a78bfa 0%, #60a5fa 100%)",
    border: "none",
    borderRadius: "8px",
    color: "#fff",
    fontWeight: "600",
    fontSize: "0.85rem",
    cursor: "pointer",
  },
  navContainer: {
    background: "rgba(15, 15, 15, 0.5)",
    backdropFilter: "blur(5px)",
    borderBottom: "1px solid rgba(255, 255, 255, 0.05)",
    padding: "0 20px",
    position: "sticky",
    top: 0,
    zIndex: 10,
  },
  tabNav: { display: "flex", gap: "8px", maxWidth: "1400px", margin: "0 auto", overflowX: "auto", paddingY: "12px" },
  navTab: {
    padding: "8px 16px",
    backgroundColor: "transparent",
    border: "1px solid rgba(255, 255, 255, 0.1)",
    borderRadius: "6px",
    color: "#888",
    fontWeight: "600",
    fontSize: "0.85rem",
    cursor: "pointer",
    whiteSpace: "nowrap",
  },
  navTabActive: {
    padding: "8px 16px",
    background: "linear-gradient(90deg, #a78bfa 0%, #60a5fa 100%)",
    border: "none",
    borderRadius: "6px",
    color: "#fff",
    fontWeight: "600",
    fontSize: "0.85rem",
    cursor: "pointer",
    whiteSpace: "nowrap",
  },
  mainLayout: { display: "grid", gridTemplateColumns: "1fr 320px", gap: "20px", maxWidth: "1400px", margin: "0 auto", padding: "20px", minHeight: "calc(100vh - 200px)" },
  contentArea: { display: "flex", flexDirection: "column", gap: "20px" },
  glassCard: {
    background: "rgba(26, 26, 26, 0.6)",
    backdropFilter: "blur(10px)",
    border: "1px solid rgba(255, 255, 255, 0.08)",
    borderRadius: "12px",
    padding: "24px",
    boxShadow: "0 8px 32px rgba(167, 139, 250, 0.1)",
  },
  cardTitle: { fontSize: "1.5rem", fontWeight: "700", margin: 0, marginBottom: "4px", color: "#a78bfa" },
  cardSubtitle: { fontSize: "0.85rem", color: "#888", margin: 0, marginBottom: "16px" },
  form: { display: "flex", flexDirection: "column", gap: "12px" },
  input: {
    width: "100%",
    padding: "12px",
    backgroundColor: "rgba(0, 0, 0, 0.3)",
    border: "1px solid rgba(167, 139, 250, 0.3)",
    borderRadius: "8px",
    color: "#f0f0f0",
    fontSize: "0.95rem",
    outline: "none",
    boxSizing: "border-box",
  },
  textarea: {
    width: "100%",
    padding: "12px",
    backgroundColor: "rgba(0, 0, 0, 0.3)",
    border: "1px solid rgba(167, 139, 250, 0.3)",
    borderRadius: "8px",
    color: "#f0f0f0",
    fontSize: "0.95rem",
    outline: "none",
    resize: "vertical",
    boxSizing: "border-box",
  },
  btnGroup: { display: "flex", gap: "12px", flexWrap: "wrap" },
  btnPrimary: {
    padding: "12px 24px",
    background: "linear-gradient(90deg, #a78bfa 0%, #60a5fa 100%)",
    border: "none",
    borderRadius: "8px",
    color: "#fff",
    fontWeight: "700",
    fontSize: "0.95rem",
    cursor: "pointer",
    flex: 1,
    minWidth: "120px",
  },
  btnSecondary: {
    padding: "12px 24px",
    background: "rgba(255, 255, 255, 0.1)",
    border: "1px solid rgba(167, 139, 250, 0.3)",
    borderRadius: "8px",
    color: "#a78bfa",
    fontWeight: "700",
    fontSize: "0.95rem",
    cursor: "pointer",
    flex: 1,
    minWidth: "120px",
  },
  logs: {
    marginTop: "16px",
    backgroundColor: "rgba(0, 0, 0, 0.3)",
    borderRadius: "8px",
    padding: "12px",
    maxHeight: "200px",
    overflowY: "auto",
    borderLeft: "3px solid #a3e635",
  },
  logLine: { padding: "4px 0", fontSize: "0.85rem", color: "#a3e635", borderBottom: "1px solid rgba(255, 255, 255, 0.05)" },
  statsGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: "12px", marginTop: "16px" },
  statBox: { background: "rgba(0, 0, 0, 0.3)", borderRadius: "8px", padding: "12px", textAlign: "center", border: "1px solid rgba(167, 139, 250, 0.2)" },
  statBoxLabel: { fontSize: "0.8rem", color: "#888", marginBottom: "6px" },
  statBoxValue: { fontSize: "1.3rem", fontWeight: "700", color: "#34d399" },
  leadsGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))", gap: "12px", marginTop: "16px" },
  leadCard: {
    background: "rgba(0, 0, 0, 0.2)",
    border: "1px solid rgba(167, 139, 250, 0.3)",
    borderRadius: "8px",
    padding: "12px",
  },
  leadHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" },
  leadScore: { padding: "4px 8px", borderRadius: "4px", fontSize: "0.75rem", fontWeight: "700", color: "#fff" },
  leadDetail: { fontSize: "0.85rem", margin: "4px 0" },
  leadMeta: { display: "flex", gap: "8px", fontSize: "0.75rem", color: "#888", marginTop: "8px", borderTop: "1px solid rgba(255,255,255,0.1)", paddingTop: "8px" },
  campaignsGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: "12px", marginTop: "16px" },
  campaignCard: { background: "rgba(0, 0, 0, 0.2)", border: "1px solid rgba(52, 211, 153, 0.3)", borderRadius: "8px", padding: "12px" },
  stats: { display: "flex", gap: "12px", fontSize: "0.85rem", marginTop: "8px", color: "#888" },
  stagesGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: "12px", marginTop: "16px" },
  stageCard: { background: "rgba(0, 0, 0, 0.2)", border: "1px solid rgba(96, 165, 250, 0.3)", borderRadius: "8px", padding: "12px", textAlign: "center" },
  stageName: { fontSize: "0.85rem", color: "#888", marginBottom: "6px" },
  stageCount: { fontSize: "1.2rem", fontWeight: "700", color: "#60a5fa" },
  stageValue: { fontSize: "0.9rem", color: "#a78bfa" },
  agentsGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: "12px", marginTop: "16px" },
  agentCard: { background: "rgba(0, 0, 0, 0.2)", border: "2px solid", borderRadius: "8px", padding: "12px" },
  agentStatus: { fontSize: "0.85rem", margin: "4px 0" },
  agentDeals: { fontSize: "1rem", fontWeight: "700", color: "#34d399" },
  scaleButtons: { display: "flex", gap: "8px", flexWrap: "wrap" },
  scaleButton: { padding: "8px 16px", backgroundColor: "rgba(255, 255, 255, 0.05)", border: "1px solid rgba(255, 255, 255, 0.1)", borderRadius: "6px", color: "#888", fontWeight: "600", cursor: "pointer" },
  scaleButtonActive: { padding: "8px 16px", background: "linear-gradient(90deg, #a78bfa, #60a5fa)", border: "none", borderRadius: "6px", color: "#fff", fontWeight: "600", cursor: "pointer" },
  roiComparison: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginTop: "16px" },
  roiColumn: { background: "rgba(0, 0, 0, 0.2)", border: "1px solid rgba(255, 255, 255, 0.1)", borderRadius: "8px", padding: "12px" },
  roiRow: { display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: "1px solid rgba(255, 255, 255, 0.05)", fontSize: "0.9rem" },
  roiConclusion: { background: "rgba(16, 185, 129, 0.1)", border: "1px solid rgba(16, 185, 129, 0.3)", borderRadius: "8px", padding: "12px", marginTop: "16px" },
  experimentsGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", gap: "12px", marginTop: "16px" },
  experimentCard: { background: "rgba(0, 0, 0, 0.2)", border: "1px solid rgba(255, 255, 255, 0.1)", borderRadius: "8px", padding: "12px" },
  experimentVariants: { display: "flex", gap: "12px", fontSize: "0.85rem", margin: "8px 0" },
  experimentResult: { fontSize: "0.85rem", color: "#f59e0b", marginTop: "6px" },
  activityFeed: { display: "flex", flexDirection: "column", gap: "8px", maxHeight: "400px", overflowY: "auto", marginTop: "12px" },
  activityItem: { display: "flex", gap: "12px", padding: "8px", background: "rgba(0, 0, 0, 0.2)", borderRadius: "6px", alignItems: "center" },
  activityIcon: { fontSize: "1.1rem" },
  activityContent: { flex: 1, fontSize: "0.85rem" },
  activityTime: { fontSize: "0.7rem", color: "#888", whiteSpace: "nowrap" },
  emailBox: {
    background: "rgba(0, 0, 0, 0.2)",
    border: "1px solid rgba(167, 139, 250, 0.3)",
    borderRadius: "8px",
    padding: "12px",
    marginTop: "12px",
  },
  emailNumber: { fontWeight: "700", color: "#a78bfa", marginBottom: "8px", fontSize: "0.9rem" },
  emailSubject: { fontWeight: "600", color: "#60a5fa", marginBottom: "8px", fontSize: "0.85rem", margin: "0 0 8px 0" },
  emailBody: {
    color: "#e2e8f0",
    lineHeight: "1.6",
    fontSize: "0.85rem",
    whiteSpace: "pre-wrap",
    wordWrap: "break-word",
  },
  sidebar: { display: "flex", flexDirection: "column", gap: "20px" },
  spacer: { flex: 1 },
  stat: { display: "flex", flexDirection: "column", alignItems: "center", gap: "6px", padding: "12px", background: "rgba(0, 0, 0, 0.2)", borderRadius: "8px", border: "1px solid rgba(255, 255, 255, 0.05)" },
  statLabel: { fontSize: "0.75rem", color: "#888" },
  statValue: { fontSize: "1.1rem", fontWeight: "700" },
  quickStats: { display: "grid", gridTemplateColumns: "1fr", gap: "8px" },
  miniActivityFeed: { display: "flex", flexDirection: "column", gap: "6px", maxHeight: "300px", overflowY: "auto" },
  miniActivityItem: { display: "flex", gap: "8px", alignItems: "flex-start", padding: "6px", fontSize: "0.7rem", color: "#888" },
  miniActivityTime: { color: "#666", whiteSpace: "nowrap" },
  miniActivityIcon: { fontSize: "0.9rem" },
  miniActivityText: { flex: 1, color: "#aaa" },
};
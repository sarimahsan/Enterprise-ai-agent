export default function AgentActivityLog({ logs, loading }) {
  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>🤖 Agent Activity Log</h2>
        <span style={styles.badge}>{loading ? "🔵 LIVE" : "⚪ IDLE"}</span>
      </div>

      <div style={styles.logsContainer}>
        {logs.length === 0 ? (
          <div style={styles.emptyState}>
            <div style={styles.emptyIcon}>📭</div>
            <p style={styles.emptyText}>Waiting for agent logs...</p>
            <p style={styles.emptySubtext}>Generate a campaign to see live updates</p>
          </div>
        ) : (
          <div style={styles.logsList}>
            {logs.map((log, idx) => (
              <div key={idx} style={styles.logEntry}>
                <span style={styles.timestamp}>[{new Date().toLocaleTimeString()}]</span>
                <span style={styles.logMessage}>{log}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

const styles = {
  container: {
    backgroundColor: "#1e293b",
    border: "1px solid #334155",
    borderRadius: "12px",
    padding: "24px",
    height: "100%",
    display: "flex",
    flexDirection: "column",
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "16px",
    paddingBottom: "12px",
    borderBottom: "1px solid #334155",
  },

  title: {
    fontSize: "1.1rem",
    fontWeight: "700",
    color: "#e2e8f0",
    margin: "0",
  },

  badge: {
    fontSize: "0.8rem",
    fontWeight: "600",
    padding: "4px 10px",
    backgroundColor: "#1e293b",
    borderRadius: "4px",
    color: "#a78bfa",
  },

  logsContainer: {
    flex: 1,
    overflow: "hidden",
    display: "flex",
    flexDirection: "column",
  },

  emptyState: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100%",
    textAlign: "center",
    color: "#64748b",
  },

  emptyIcon: {
    fontSize: "3rem",
    marginBottom: "12px",
  },

  emptyText: {
    fontSize: "0.95rem",
    fontWeight: "500",
    margin: "0 0 4px 0",
  },

  emptySubtext: {
    fontSize: "0.85rem",
    color: "#475569",
    margin: "0",
  },

  logsList: {
    overflowY: "auto",
    backgroundColor: "#0f172a",
    borderRadius: "8px",
    padding: "12px",
    display: "flex",
    flexDirection: "column",
    gap: "4px",
  },

  logEntry: {
    display: "flex",
    gap: "10px",
    padding: "8px",
    fontSize: "0.85rem",
    fontFamily: "monospace",
    lineHeight: "1.4",
    borderRadius: "4px",
  },

  timestamp: {
    color: "#64748b",
    minWidth: "110px",
    fontWeight: "600",
  },

  logMessage: {
    color: "#cbd5e1",
    flex: 1,
    wordBreak: "break-word",
  },
}

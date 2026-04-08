export default function CampaignAnalytics({ analytics }) {
  const metrics = [
    { icon: "📧", label: "Total Emails", value: analytics.total_emails || 0 },
    { icon: "📡", label: "Channels", value: analytics.channels?.length || 0 },
    { icon: "🎯", label: "Estimated Reach", value: analytics.estimated_reach || "N/A" },
    { icon: "⚡", label: "Optimization Score", value: `${analytics.optimization_score || 0}%` },
    { icon: "🏆", label: "Best Channel", value: analytics.best_channel || "Email" },
    { icon: "🕐", label: "Peak Send Time", value: analytics.peak_send_time || "9:00 AM" },
  ]

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>📊 Campaign Analytics</h2>
      <div style={styles.grid}>
        {metrics.map((metric, idx) => (
          <div key={idx} style={styles.tile}>
            <div style={styles.tileIcon}>{metric.icon}</div>
            <div style={styles.tileLabel}>{metric.label}</div>
            <div style={styles.tileValue}>{metric.value}</div>
          </div>
        ))}
      </div>

      {analytics.channels && (
        <div style={styles.channelsSection}>
          <h3 style={styles.sectionTitle}>📡 Active Channels</h3>
          <div style={styles.channelsList}>
            {analytics.channels.map((channel, idx) => (
              <span key={idx} style={styles.channel}>
                {channel === "email" && "📧"} {channel}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

const styles = {
  container: {
    backgroundColor: "rgba(30, 30, 30, 0.4)",
    backdropFilter: "blur(10px)",
    border: "1px solid rgba(255, 255, 255, 0.08)",
    boxShadow: "0 8px 32px rgba(0, 0, 0, 0.3)",
    borderRadius: "12px",
    padding: "24px",
  },

  title: {
    fontSize: "1.2rem",
    fontWeight: "700",
    color: "#e2e8f0",
    marginBottom: "20px",
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gap: "16px",
    marginBottom: "24px",
  },

  tile: {
    backgroundColor: "#0f172a",
    border: "1px solid #334155",
    borderRadius: "8px",
    padding: "20px",
    textAlign: "center",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "10px",
  },

  tileIcon: {
    fontSize: "2rem",
  },

  tileLabel: {
    fontSize: "0.8rem",
    fontWeight: "600",
    color: "#94a3b8",
    textTransform: "uppercase",
  },

  tileValue: {
    fontSize: "1.5rem",
    fontWeight: "700",
    color: "#ffffff",
  },

  channelsSection: {
    paddingTop: "20px",
    borderTop: "1px solid #334155",
  },

  sectionTitle: {
    fontSize: "0.95rem",
    fontWeight: "600",
    color: "#cbd5e1",
    marginBottom: "12px",
  },

  channelsList: {
    display: "flex",
    gap: "10px",
    flexWrap: "wrap",
  },

  channel: {
    display: "inline-block",
    padding: "6px 12px",
    backgroundColor: "#334155",
    borderRadius: "6px",
    fontSize: "0.9rem",
    fontWeight: "500",
    color: "#cbd5e1",
  },
}

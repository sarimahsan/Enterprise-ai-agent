export default function EmailStatusTracker({ stats }) {
  return (
    <div style={styles.container}>
      <h2 style={styles.title}>📊 Email Sending Statistics</h2>
      
      <div style={styles.gridContainer}>
        <div style={styles.statCard}>
          <div style={styles.statIcon}>📤</div>
          <div style={styles.statNumber}>{stats.total_sent}</div>
          <div style={styles.statLabel}>Total Sent</div>
        </div>

        <div style={styles.statCard}>
          <div style={styles.statIcon}>⏳</div>
          <div style={styles.statNumber}>{stats.pending}</div>
          <div style={styles.statLabel}>Pending</div>
        </div>

        <div style={styles.statCard}>
          <div style={styles.statIcon}>❌</div>
          <div style={styles.statNumber}>{stats.failed}</div>
          <div style={styles.statLabel}>Failed</div>
        </div>

        <div style={styles.statCard}>
          <div style={styles.statIcon}>✅</div>
          <div style={styles.statNumber}>{stats.success_rate.toFixed(1)}%</div>
          <div style={styles.statLabel}>Success Rate</div>
        </div>
      </div>

      {/* Recent Failures */}
      {stats.failed_emails.length > 0 && (
        <div style={styles.failedSection}>
          <h3 style={styles.sectionTitle}>⚠️ Failed Emails</h3>
          <div style={styles.emailList}>
            {stats.failed_emails.slice(0, 3).map((email, idx) => (
              <div key={idx} style={styles.emailItem}>
                <span style={styles.iconFailed}>❌</span>
                <div style={styles.emailInfo}>
                  <div style={styles.emailAddr}>{email.to_email}</div>
                  <div style={styles.emailError}>{email.error}</div>
                </div>
              </div>
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
    borderRadius: "12px",
    padding: "clamp(12px, 3vw, 24px)",
    boxShadow: "0 8px 32px rgba(0, 0, 0, 0.3)",
  },

  title: {
    fontSize: "clamp(1rem, 2.5vw, 1.2rem)",
    fontWeight: "700",
    color: "#ffffff",
    marginBottom: "clamp(12px, 2vw, 20px)",
  },

  gridContainer: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))",
    gap: "clamp(8px, 1.5vw, 16px)",
    marginBottom: "clamp(12px, 2vw, 24px)",
  },

  statCard: {
    backgroundColor: "rgba(255, 255, 255, 0.05)",
    border: "1px solid rgba(255, 255, 255, 0.1)",
    borderRadius: "8px",
    padding: "clamp(12px, 2vw, 20px)",
    textAlign: "center",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "clamp(6px, 1vw, 10px)",
    backdropFilter: "blur(5px)",
    transition: "all 0.3s ease",
  },

  statIcon: {
    fontSize: "clamp(1.5rem, 3vw, 2rem)",
  },

  statNumber: {
    fontSize: "clamp(1.3rem, 3.5vw, 1.8rem)",
    fontWeight: "700",
    color: "#ffffff",
  },

  statLabel: {
    fontSize: "0.85rem",
    color: "#a0a0a0",
    fontWeight: "500",
  },

  failedSection: {
    marginTop: "20px",
    paddingTop: "20px",
    borderTop: "1px solid rgba(255, 255, 255, 0.08)",
  },

  sectionTitle: {
    fontSize: "0.95rem",
    fontWeight: "600",
    color: "#ff6b6b",
    marginBottom: "12px",
  },

  emailList: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },

  emailItem: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    padding: "12px",
    backgroundColor: "rgba(255, 107, 107, 0.1)",
    borderRadius: "6px",
    border: "1px solid rgba(255, 107, 107, 0.2)",
    backdropFilter: "blur(5px)",
  },

  iconFailed: {
    fontSize: "1.2rem",
  },

  emailInfo: {
    flex: 1,
  },

  emailAddr: {
    fontSize: "0.9rem",
    color: "#cbd5e1",
    fontWeight: "500",
  },

  emailError: {
    fontSize: "0.8rem",
    color: "#ff6b6b",
    marginTop: "2px",
  },
}

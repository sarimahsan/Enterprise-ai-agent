export default function IntelligenceCards({ analysis }) {
  const cards = [
    { icon: "🎯", title: "Opportunity ID", value: analysis.opportunity },
    { icon: "👤", title: "Decision Maker", value: analysis.decision_maker },
    { icon: "📌", title: "Key Facts", value: analysis.key_fact },
    { icon: "⚠️", title: "Pain Points", value: analysis.pain_points?.join(", ") || "N/A" },
  ]

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>🧠 Intelligence Cards</h2>
      <div style={styles.grid}>
        {cards.map((card, idx) => (
          <div key={idx} style={styles.card}>
            <div style={styles.cardIcon}>{card.icon}</div>
            <div style={styles.cardLabel}>{card.title}</div>
            <div style={styles.cardValue}>{card.value}</div>
          </div>
        ))}
      </div>
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
    marginBottom: "16px",
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)",
    gap: "16px",
  },

  card: {
    backgroundColor: "#0f172a",
    border: "1px solid #334155",
    borderRadius: "8px",
    padding: "16px",
    textAlign: "center",
  },

  cardIcon: {
    fontSize: "2rem",
    marginBottom: "8px",
  },

  cardLabel: {
    fontSize: "0.8rem",
    fontWeight: "600",
    color: "#a78bfa",
    textTransform: "uppercase",
    marginBottom: "8px",
  },

  cardValue: {
    fontSize: "0.9rem",
    color: "#cbd5e1",
    lineHeight: "1.4",
  },
}

export default function EmailVariants({ variants, emails }) {
  return (
    <div style={styles.container}>
      <h2 style={styles.title}>📬 Email Variants (A/B Testing)</h2>
      <div style={styles.grid}>
        <div style={styles.variantCard}>
          <div style={styles.badgeA}>VARIANT A</div>
          <div style={styles.subBadge}>Direct Approach</div>
          
          <div style={styles.content}>
            <div style={styles.field}>
              <span style={styles.fieldLabel}>Subject:</span>
              <span style={styles.fieldValue}>{variants.ab_variants?.subject_a}</span>
            </div>
            
            <div style={styles.field}>
              <span style={styles.fieldLabel}>Tone:</span>
              <span style={styles.fieldValue}>{variants.ab_variants?.tone_a}</span>
            </div>
            
            <div style={styles.preview}>
              <span style={styles.fieldLabel}>Preview:</span>
              <p style={styles.previewText}>{emails.email_1?.body?.substring(0, 120)}...</p>
            </div>
          </div>
          
          <div style={styles.confidence}>
            <span style={styles.confidenceLabel}>Confidence</span>
            <span style={styles.confidenceValue}>84%</span>
          </div>
        </div>

        <div style={styles.variantCard}>
          <div style={styles.badgeB}>VARIANT B</div>
          <div style={styles.subBadge}>Insightful Approach</div>
          
          <div style={styles.content}>
            <div style={styles.field}>
              <span style={styles.fieldLabel}>Subject:</span>
              <span style={styles.fieldValue}>{variants.ab_variants?.subject_b}</span>
            </div>
            
            <div style={styles.field}>
              <span style={styles.fieldLabel}>Tone:</span>
              <span style={styles.fieldValue}>{variants.ab_variants?.tone_b}</span>
            </div>
            
            <div style={styles.preview}>
              <span style={styles.fieldLabel}>Preview:</span>
              <p style={styles.previewText}>{emails.email_2?.body?.substring(0, 120)}...</p>
            </div>
          </div>
          
          <div style={styles.confidence}>
            <span style={styles.confidenceLabel}>Confidence</span>
            <span style={styles.confidenceValue}>89%</span>
          </div>
        </div>
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
    gridTemplateColumns: "1fr 1fr",
    gap: "16px",
  },

  variantCard: {
    backgroundColor: "#0f172a",
    border: "1px solid #334155",
    borderRadius: "8px",
    padding: "20px",
  },

  badgeA: {
    display: "inline-block",
    padding: "4px 10px",
    backgroundColor: "rgba(255, 255, 255, 0.3)",
    backdropFilter: "blur(5px)",
    color: "#fff",
    fontSize: "0.75rem",
    fontWeight: "700",
    borderRadius: "4px",
    marginBottom: "4px",
  },

  badgeB: {
    display: "inline-block",
    padding: "4px 10px",
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    backdropFilter: "blur(5px)",
    color: "#fff",
    fontSize: "0.75rem",
    fontWeight: "700",
    borderRadius: "4px",
    marginBottom: "4px",
  },

  subBadge: {
    display: "block",
    fontSize: "0.8rem",
    color: "#94a3b8",
    marginBottom: "12px",
  },

  content: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
    marginBottom: "16px",
  },

  field: {
    display: "flex",
    flexDirection: "column",
    gap: "4px",
  },

  fieldLabel: {
    fontSize: "0.8rem",
    fontWeight: "600",
    color: "#ffffff",
    textTransform: "uppercase",
  },

  fieldValue: {
    fontSize: "0.9rem",
    color: "#cbd5e1",
  },

  preview: {
    backgroundColor: "#1e293b",
    padding: "12px",
    borderRadius: "6px",
  },

  previewText: {
    fontSize: "0.85rem",
    color: "#94a3b8",
    margin: "4px 0 0 0",
    lineHeight: "1.4",
  },

  confidence: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "12px",
    backgroundColor: "#1e293b",
    borderRadius: "6px",
    borderTop: "1px solid #334155",
  },

  confidenceLabel: {
    fontSize: "0.8rem",
    fontWeight: "600",
    color: "#94a3b8",
    textTransform: "uppercase",
  },

  confidenceValue: {
    fontSize: "1.2rem",
    fontWeight: "700",
    color: "#10b981",
  },
}

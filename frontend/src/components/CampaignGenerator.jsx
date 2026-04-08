import { Zap, Building2, Target, Send } from "lucide-react"

export default function CampaignGenerator({ company, goal, onCompanyChange, onGoalChange, onGenerate, loading }) {
  return (
    <div style={styles.container} className="glass-panel">
      <div style={styles.header}>
        <div style={styles.headerIcon}>
          <Zap size={24} color="currentColor" />
        </div>
        <div>
          <h2 style={styles.title}>Campaign Generator</h2>
          <p style={styles.subtitle}>Create intelligent outreach campaigns</p>
        </div>
      </div>

      <form onSubmit={(e) => { e.preventDefault(); onGenerate() }} style={styles.form}>
        {/* Company Input */}
        <div style={styles.formGroup}>
          <label style={styles.label}>
            <Building2 size={16} />
            <span>Company Name</span>
          </label>
          <input
            type="text"
            placeholder="Enter target company..."
            value={company}
            onChange={(e) => onCompanyChange(e.target.value)}
            style={styles.input}
            required
          />
          {company && (
            <span style={styles.hint}>✓ {company}</span>
          )}
        </div>

        {/* Goal Input */}
        <div style={styles.formGroup}>
          <label style={styles.label}>
            <Target size={16} />
            <span>Outreach Goal</span>
          </label>
          <textarea
            placeholder="What do you want to achieve? E.g., Partnership, Demo, Meeting..."
            value={goal}
            onChange={(e) => onGoalChange(e.target.value)}
            style={styles.textarea}
            required
          />
          {goal && (
            <span style={styles.hint}>✓ {goal.length} characters</span>
          )}
        </div>

        {/* Generate Button */}
        <button
          type="submit"
          disabled={loading || !company.trim() || !goal.trim()}
          style={{
            ...styles.generateBtn,
            ...(loading ? styles.generateBtnLoading : {}),
            ...(!(company.trim() && goal.trim()) ? styles.generateBtnDisabled : {})
          }}
        >
          {loading ? (
            <>
              <span className="spinner" style={{width: "16px", height: "16px"}}></span>
              <span>Generating...</span>
            </>
          ) : (
            <>
              <Send size={18} />
              <span>Generate Campaign</span>
            </>
          )}
        </button>
      </form>

      {/* Features */}
      <div style={styles.features}>
        <h3 style={styles.featuresTitle}>Key Features</h3>
        <div style={styles.featuresList}>
          <div style={styles.featureItem}>
            <div style={styles.featureCheckmark}>✓</div>
            <div>
              <div style={styles.featureName}>Smart Analysis</div>
              <div style={styles.featureDesc}>AI-powered company insights</div>
            </div>
          </div>
          <div style={styles.featureItem}>
            <div style={styles.featureCheckmark}>✓</div>
            <div>
              <div style={styles.featureName}>Multi-Variant Emails</div>
              <div style={styles.featureDesc}>A/B test different approaches</div>
            </div>
          </div>
          <div style={styles.featureItem}>
            <div style={styles.featureCheckmark}>✓</div>
            <div>
              <div style={styles.featureName}>Calendar Integration</div>
              <div style={styles.featureDesc}>Schedule sends automatically</div>
            </div>
          </div>
          <div style={styles.featureItem}>
            <div style={styles.featureCheckmark}>✓</div>
            <div>
              <div style={styles.featureName}>LinkedIn Targeting</div>
              <div style={styles.featureDesc}>Find decision makers easily</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

const styles = {
  container: {
    padding: "clamp(16px, 3vw, 28px)",
    animation: "fadeIn 0.3s ease-out",
    height: "100%",
    display: "flex",
    flexDirection: "column",
  },

  header: {
    display: "flex",
    alignItems: "flex-start",
    gap: "14px",
    marginBottom: "clamp(20px, 4vw, 28px)",
    paddingBottom: "clamp(14px, 2vw, 20px)",
    borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
  },

  headerIcon: {
    width: "40px",
    height: "40px",
    borderRadius: "10px",
    background: "linear-gradient(135deg, #06b6d4, #8b5cf6)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "white",
    flexShrink: 0,
  },

  title: {
    fontSize: "clamp(1.1rem, 2.5vw, 1.4rem)",
    fontWeight: "700",
    margin: "0",
    color: "#f1f5f9",
    background: "linear-gradient(135deg, #22d3ee, #a78bfa)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },

  subtitle: {
    fontSize: "clamp(0.75rem, 1.5vw, 0.9rem)",
    color: "#94a3b8",
    margin: "4px 0 0 0",
  },

  form: {
    display: "flex",
    flexDirection: "column",
    gap: "clamp(16px, 2.5vw, 22px)",
    marginBottom: "clamp(20px, 3vw, 28px)",
  },

  formGroup: {
    display: "flex",
    flexDirection: "column",
    gap: "clamp(8px, 1.5vw, 10px)",
  },

  label: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    fontSize: "clamp(0.75rem, 1.2vw, 0.9rem)",
    fontWeight: "600",
    color: "#cbd5e1",
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },

  input: {
    padding: "clamp(10px, 1.5vw, 12px) clamp(12px, 2vw, 16px)",
    background: "rgba(255, 255, 255, 0.05)",
    border: "1px solid rgba(255, 255, 255, 0.1)",
    borderRadius: "var(--radius-md)",
    color: "#f1f5f9",
    fontSize: "clamp(0.85rem, 1.2vw, 0.95rem)",
    outline: "none",
    boxSizing: "border-box",
    transition: "all 0.2s ease",
    backdropFilter: "blur(10px)",
  },

  textarea: {
    padding: "clamp(10px, 1.5vw, 12px) clamp(12px, 2vw, 16px)",
    background: "rgba(255, 255, 255, 0.05)",
    border: "1px solid rgba(255, 255, 255, 0.1)",
    borderRadius: "var(--radius-md)",
    color: "#f1f5f9",
    fontSize: "clamp(0.85rem, 1.2vw, 0.95rem)",
    minHeight: "clamp(100px, 15vw, 140px)",
    resize: "vertical",
    fontFamily: "inherit",
    outline: "none",
    boxSizing: "border-box",
    transition: "all 0.2s ease",
    backdropFilter: "blur(10px)",
  },

  hint: {
    fontSize: "clamp(0.7rem, 1vw, 0.8rem)",
    color: "#6ee7b7",
    marginTop: "4px",
  },

  generateBtn: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "10px",
    padding: "clamp(10px, 1.5vw, 14px) clamp(16px, 2vw, 24px)",
    background: "linear-gradient(135deg, #06b6d4, #00d9ff)",
    border: "1px solid rgba(34, 211, 238, 0.5)",
    borderRadius: "var(--radius-md)",
    color: "white",
    fontWeight: "700",
    fontSize: "clamp(0.85rem, 1.2vw, 0.95rem)",
    cursor: "pointer",
    transition: "all 0.2s ease",
    boxShadow: "0 4px 12px rgba(6, 182, 212, 0.3)",
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },

  generateBtnLoading: {
    opacity: 0.8,
    cursor: "not-allowed",
    boxShadow: "0 0 20px rgba(6, 182, 212, 0.5)",
  },

  generateBtnDisabled: {
    opacity: 0.5,
    cursor: "not-allowed",
  },

  features: {
    marginTop: "auto",
    paddingTop: "clamp(16px, 2vw, 24px)",
    borderTop: "1px solid rgba(255, 255, 255, 0.1)",
  },

  featuresTitle: {
    fontSize: "clamp(0.95rem, 2vw, 1.1rem)",
    fontWeight: "600",
    color: "#22d3ee",
    margin: "0 0 clamp(12px, 2vw, 16px) 0",
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },

  featuresList: {
    display: "flex",
    flexDirection: "column",
    gap: "clamp(10px, 1.5vw, 14px)",
  },

  featureItem: {
    display: "flex",
    gap: "12px",
    padding: "clamp(10px, 1.5vw, 12px)",
    background: "rgba(6, 182, 212, 0.08)",
    border: "1px solid rgba(6, 182, 212, 0.2)",
    borderRadius: "var(--radius-md)",
    transition: "all 0.2s ease",
  },

  featureCheckmark: {
    color: "#6ee7b7",
    fontWeight: "700",
    minWidth: "20px",
    textAlign: "center",
  },

  featureName: {
    fontSize: "clamp(0.8rem, 1.2vw, 0.9rem)",
    fontWeight: "600",
    color: "#f1f5f9",
    marginBottom: "2px",
  },

  featureDesc: {
    fontSize: "clamp(0.7rem, 1vw, 0.8rem)",
    color: "#94a3b8",
  },
}

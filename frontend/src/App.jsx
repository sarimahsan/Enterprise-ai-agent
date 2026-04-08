import { useState, useEffect } from "react"
import {
  Mail, BarChart3, Zap, Calendar, Globe, Activity,
  CheckCircle, AlertCircle, RefreshCw, Send, TrendingUp,
  Target, Settings, LogOut, Menu, X
} from "lucide-react"
import EmailManagementPanel from "./components/EmailManagementPanel"
import EmailStatusTracker from "./components/EmailStatusTracker"
import CampaignGenerator from "./components/CampaignGenerator"
import AgentActivityLog from "./components/AgentActivityLog"
import IntelligenceCards from "./components/IntelligenceCards"
import EmailVariants from "./components/EmailVariants"
import CampaignAnalytics from "./components/CampaignAnalytics"
import CalendarScheduler from "./components/CalendarScheduler"
import LinkedInOutreach from "./components/LinkedInOutreach"
import "./App.css"

const API_URL = "http://localhost:8000/api"

export default function App() {
  // Main State
  const [activeTab, setActiveTab] = useState("dashboard")
  const [menuOpen, setMenuOpen] = useState(false)
  const [loading, setLoading] = useState(false)

  // Form State
  const [company, setCompany] = useState("")
  const [goal, setGoal] = useState("")

  // API Response Data
  const [analysis, setAnalysis] = useState(null)
  const [emails, setEmails] = useState(null)
  const [emailTemplates, setEmailTemplates] = useState(null)
  const [followUpSchedule, setFollowUpSchedule] = useState(null)
  const [variants, setVariants] = useState(null)
  const [logs, setLogs] = useState([])
  const [analytics, setAnalytics] = useState(null)

  // Status Data
  const [gmailStatus, setGmailStatus] = useState(null)
  const [emailStats, setEmailStats] = useState(null)

  // Initialize & Poll
  useEffect(() => {
    checkGmailStatus()
    loadEmailStats()
    const interval = setInterval(loadEmailStats, 30000)
    return () => clearInterval(interval)
  }, [])

  // Check Gmail Connection
  const checkGmailStatus = async () => {
    try {
      const res = await fetch(`${API_URL}/gmail-auth-status`)
      const data = await res.json()
      setGmailStatus(data)
    } catch (err) {
      console.error("Gmail status check failed:", err)
      setGmailStatus({ is_authenticated: false })
    }
  }

  // Load Email Stats
  const loadEmailStats = async () => {
    try {
      const res = await fetch(`${API_URL}/email-stats`)
      const data = await res.json()
      setEmailStats(data)
    } catch (err) {
      console.error("Email stats load failed:", err)
    }
  }

  // Run Campaign Generation Agent
  const runAgent = async () => {
    if (!company.trim() || !goal.trim()) {
      alert("Please enter both company name and campaign goal")
      return
    }

    setLogs([])
    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ company, goal })
      })

      if (!response.ok) {
        throw new Error("Campaign generation failed")
      }

      const data = await response.json()
      setLogs(data.logs || [])
      setAnalysis(data.analysis || null)
      setEmails(data.emails || null)
      setEmailTemplates(data.email_templates || null)
      setFollowUpSchedule(data.follow_up_schedule || null)
      setVariants(data.variants || null)
      setAnalytics(data.analytics || null)
      setActiveTab("campaign")
    } catch (err) {
      setLogs([`Error: ${err.message}`])
      alert("Failed to generate campaign: " + err.message)
    } finally {
      setLoading(false)
    }
  }

  // Tab Navigation Component
  const TabButton = ({ id, label, icon: Icon, badge }) => (
    <button
      onClick={() => {
        setActiveTab(id)
        setMenuOpen(false)
      }}
      className={`tab-btn ${activeTab === id ? "active" : ""}`}
    >
      <Icon size={20} />
      <span>{label}</span>
      {badge > 0 && <span className="badge">{badge}</span>}
    </button>
  )

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <div className="logo">
            <div className="logo-icon">
              <Zap size={24} />
            </div>
            <div className="logo-text">
              <h1>FlowForge AI</h1>
              <p>Enterprise Campaign Automation</p>
            </div>
          </div>
        </div>

        <nav className={`nav ${menuOpen ? "open" : ""}`}>
          <TabButton id="dashboard" label="Dashboard" icon={Zap} />
          <TabButton id="campaign" label="Campaign" icon={Target} />
          <TabButton id="emails" label="Emails" icon={Mail} badge={emailStats?.total_sent || 0} />
          <TabButton id="analytics" label="Analytics" icon={BarChart3} />
        </nav>

        <div className="header-right">
          <div className={`status-badge ${gmailStatus?.is_authenticated ? "connected" : "disconnected"}`}>
            {gmailStatus?.is_authenticated ? (
              <>
                <CheckCircle size={16} />
                <span>Gmail Connected</span>
              </>
            ) : (
              <>
                <AlertCircle size={16} />
                <span>Gmail Offline</span>
              </>
            )}
          </div>

          <button
            className="icon-btn"
            onClick={checkGmailStatus}
            title="Refresh Gmail status"
          >
            <RefreshCw size={18} />
          </button>

          <button
            className="menu-toggle"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            {menuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* Dashboard Tab */}
        {activeTab === "dashboard" && (
          <div className="dashboard-layout">
            <div className="section">
              <div className="section-header">
                <Zap size={28} />
                <div>
                  <h2>Campaign Generator</h2>
                  <p>Create intelligent outreach campaigns with AI</p>
                </div>
              </div>

              <div className="dashboard-grid">
                <div className="card generator-card">
                  <CampaignGenerator
                    company={company}
                    goal={goal}
                    onCompanyChange={setCompany}
                    onGoalChange={setGoal}
                    onGenerate={runAgent}
                    loading={loading}
                  />
                </div>

                <div className="card activity-card">
                  <div className="card-header">
                    <Activity size={20} />
                    <h3>Agent Activity</h3>
                  </div>
                  <AgentActivityLog logs={logs} loading={loading} />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Campaign Tab */}
        {activeTab === "campaign" && (
          <div className="campaign-layout">
            <div className="section-header">
              <Target size={28} />
              <div>
                <h2>Campaign Overview</h2>
                <p>{company || "No Company"} — {goal || "No Goal Set"}</p>
              </div>
            </div>

            {analysis ? (
              <>
                <div className="grid-2">
                  <div className="card">
                    <IntelligenceCards analysis={analysis} />
                  </div>
                  <div className="card">
                    {analytics ? <CampaignAnalytics analytics={analytics} /> : <div className="placeholder">Analytics loading...</div>}
                  </div>
                </div>

                <div className="grid-2">
                  <div className="card">
                    <CalendarScheduler campaign={{ name: `${company} Campaign`, company, analysis }} />
                  </div>
                  <div className="card">
                    <LinkedInOutreach company={company} goal={goal} analysis={analysis} />
                  </div>
                </div>
              </>
            ) : (
              <div className="empty-state">
                <Zap size={48} />
                <h3>No Campaign Generated Yet</h3>
                <p>Generate a campaign from the Dashboard tab to see insights</p>
              </div>
            )}
          </div>
        )}

        {/* Emails Tab */}
        {activeTab === "emails" && (
          <div className="emails-layout">
            <div className="section-header">
              <Mail size={28} />
              <div>
                <h2>Email Management</h2>
                <p>Create, send, and track your campaigns</p>
              </div>
            </div>

            <div className="card">
              <div className="card-header">
                <BarChart3 size={20} />
                <h3>Performance Analytics</h3>
              </div>
              {emailStats ? (
                <EmailStatusTracker stats={emailStats} />
              ) : (
                <div className="placeholder">Loading stats...</div>
              )}
            </div>

            <div className="card">
              <div className="card-header">
                <Send size={20} />
                <h3>Email Creator</h3>
              </div>
              {emailTemplates ? (
                <EmailManagementPanel
                  emailTemplates={emailTemplates}
                  emails={emails}
                  followUpSchedule={followUpSchedule}
                  onStatsUpdated={loadEmailStats}
                />
              ) : (
                <div className="placeholder">No templates available</div>
              )}
            </div>

            <div className="card">
              <div className="card-header">
                <TrendingUp size={20} />
                <h3>A/B Testing</h3>
              </div>
              {variants ? (
                <EmailVariants variants={variants} emails={emails} />
              ) : (
                <div className="placeholder">No variants available</div>
              )}
            </div>
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === "analytics" && (
          <div className="analytics-layout">
            <div className="section-header">
              <BarChart3 size={28} />
              <div>
                <h2>Analytics Dashboard</h2>
                <p>Campaign performance and insights</p>
              </div>
            </div>

            <div className="grid-2">
              <div className="card stat-card">
                <div className="stat-icon">
                  <Mail size={24} />
                </div>
                <div className="stat-content">
                  <p className="stat-label">Total Emails Sent</p>
                  <p className="stat-value">{emailStats?.total_sent || 0}</p>
                </div>
              </div>

              <div className="card stat-card">
                <div className="stat-icon success">
                  <CheckCircle size={24} />
                </div>
                <div className="stat-content">
                  <p className="stat-label">Open Rate</p>
                  <p className="stat-value">{emailStats?.open_rate ? `${emailStats.open_rate}%` : "N/A"}</p>
                </div>
              </div>

              <div className="card stat-card">
                <div className="stat-icon">
                  <TrendingUp size={24} />
                </div>
                <div className="stat-content">
                  <p className="stat-label">Click Rate</p>
                  <p className="stat-value">{emailStats?.click_rate ? `${emailStats.click_rate}%` : "N/A"}</p>
                </div>
              </div>

              <div className="card stat-card">
                <div className="stat-icon">
                  <Target size={24} />
                </div>
                <div className="stat-content">
                  <p className="stat-label">Conversion Rate</p>
                  <p className="stat-value">{emailStats?.conversion_rate ? `${emailStats.conversion_rate}%` : "N/A"}</p>
                </div>
              </div>
            </div>

            {analytics && (
              <div className="card">
                <CampaignAnalytics analytics={analytics} />
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
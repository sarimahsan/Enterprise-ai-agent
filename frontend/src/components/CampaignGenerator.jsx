import { Zap, Building2, Target, Send } from "lucide-react"

export default function CampaignGenerator({ company, goal, onCompanyChange, onGoalChange, onGenerate, loading }) {
  return (
    <div className="h-full flex flex-col p-4 md:p-6 gap-4 animate-fadeIn">
      {/* Header */}
      <div className="flex items-start gap-4 pb-4 md:pb-6 border-b border-white/10">
        <div className="w-10 h-10 rounded bg-gradient-to-br from-primary to-secondary flex items-center justify-center flex-shrink-0">
          <Zap size={24} className="text-white" />
        </div>
        <div>
          <h2 className="text-xl md:text-2xl font-bold text-gradient m-0">Campaign Generator</h2>
          {/* <p className="text-xs md:text-sm text-text-tertiary m-0 mt-1">Create intelligent outreach campaigns</p> */}
        </div>
      </div>

      {/* Form */}
      <form onSubmit={(e) => { e.preventDefault(); onGenerate() }} className="flex flex-col gap-4">
        {/* Company Input */}
        <div className="flex flex-col gap-2">
          <label className="flex items-center gap-2 text-xs font-semibold text-text-secondary uppercase tracking-wide">
            <Building2 size={16} />
            <span>Company Name</span>
          </label>
          <input
            type="text"
            placeholder="Enter target company..."
            value={company}
            onChange={(e) => onCompanyChange(e.target.value)}
            className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-md text-white placeholder-text-tertiary focus:bg-white/10 focus:border-primary-light focus:shadow-lg transition-all duration-150"
            required
          />
          {company && (
            <span className="text-xs text-success">✓ {company}</span>
          )}
        </div>

        {/* Goal Input */}
        <div className="flex flex-col gap-2">
          <label className="flex items-center gap-2 text-xs font-semibold text-text-secondary uppercase tracking-wide">
            <Target size={16} />
            <span>Outreach Goal</span>
          </label>
          <textarea
            placeholder="What do you want to achieve? E.g., Partnership, Demo, Meeting..."
            value={goal}
            onChange={(e) => onGoalChange(e.target.value)}
            className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-md text-white placeholder-text-tertiary focus:bg-white/10 focus:border-primary-light focus:shadow-lg transition-all duration-150 min-h-24 resize-vertical"
            required
          />
          {goal && (
            <span className="text-xs text-success">✓ {goal.length} characters</span>
          )}
        </div>

        {/* Generate Button */}
        <button
          type="submit"
          disabled={loading || !company.trim() || !goal.trim()}
          className={`flex items-center justify-center gap-2 px-4 py-3 rounded-md font-bold text-sm uppercase tracking-wide transition-all duration-150 ${
            loading || !company.trim() || !goal.trim()
              ? 'opacity-50 cursor-not-allowed'
              : 'bg-gradient-to-r from-primary to-cyan-400 border border-primary-light shadow-md hover:shadow-lg hover:-translate-y-0.5'
          } text-white`}
        >
          {loading ? (
            <>
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
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
      <div className="mt-auto pt-4 md:pt-6 border-t border-white/10">
        <h3 className="text-sm md:text-base font-semibold text-primary uppercase tracking-wide mb-3">Key Features</h3>
        <div className="flex flex-col gap-2">
          {[
            { name: "Smart Analysis", desc: "AI-powered company insights" },
            { name: "Multi-Variant Emails", desc: "A/B test different approaches" },
            { name: "Calendar Integration", desc: "Schedule sends automatically" },
            { name: "LinkedIn Targeting", desc: "Find decision makers easily" },
          ].map((feature, i) => (
            <div key={i} className="flex gap-3 p-2.5 bg-cyan-500/10 border border-cyan-500/20 rounded-md hover:bg-cyan-500/20 transition-all">
              <div className="text-success font-bold min-w-fit">✓</div>
              <div>
                <div className="text-xs md:text-sm font-semibold text-white">{feature.name}</div>
                <div className="text-xs text-text-tertiary">{feature.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}


export default function EmailStatusTracker({ stats }) {
  return (
    <div className="bg-black/40 backdrop-blur-sm border border-white/10 rounded-lg p-4 md:p-6 shadow-lg">
      <h2 className="text-lg md:text-xl font-bold text-white mb-4">📊 Email Sending Statistics</h2>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4 mb-6">
        {[
          { icon: "📤", value: stats.total_sent, label: "Total Sent" },
          { icon: "⏳", value: stats.pending, label: "Pending" },
          { icon: "❌", value: stats.failed, label: "Failed" },
          { icon: "✅", value: `${stats.success_rate.toFixed(1)}%`, label: "Success Rate" },
        ].map((stat, i) => (
          <div key={i} className="bg-white/5 border border-white/10 rounded-lg p-3 md:p-5 text-center flex flex-col items-center gap-2 backdrop-blur-sm hover:bg-white/10 transition-all">
            <div className="text-xl md:text-2xl">{stat.icon}</div>
            <div className="text-lg md:text-2xl font-bold text-white">{stat.value}</div>
            <div className="text-xs md:text-sm text-gray-400 font-medium">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Failed Emails Section */}
      {stats.failed_emails.length > 0 && (
        <div className="mt-6 pt-6 border-t border-white/10">
          <h3 className="text-sm md:text-base font-semibold text-red-500 mb-3">⚠️ Failed Emails (Last 3)</h3>
          <div className="flex flex-col gap-2.5">
            {stats.failed_emails.slice(0, 3).map((email, idx) => (
              <div key={idx} className="flex items-start gap-3 p-3 bg-red-500/10 border border-red-500/20 rounded-lg backdrop-blur-sm">
                <span className="text-lg mt-0.5">❌</span>
                <div className="flex-1">
                  <div className="text-sm md:text-base text-slate-300 font-medium">{email.to_email}</div>
                  <div className="text-xs md:text-sm text-red-400 mt-0.5">{email.error}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

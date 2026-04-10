export default function AgentActivityLog({ logs, loading }) {
  return (
    <div className="h-full flex flex-col bg-slate-900/60 border border-slate-600/30 rounded-2xl p-5">
      {/* Header */}
      <div className="flex justify-between items-center mb-4 pb-3 border-b border-slate-600/30">
        <h2 className="text-base font-bold text-white m-0 flex items-center gap-2">
          <span className="text-lg">🤖</span> Agent Activity
        </h2>
        <span className={`text-xs font-semibold px-3 py-1 rounded-full transition-all ${
          loading 
            ? "bg-purple-500/20 border border-purple-500/30 text-purple-300" 
            : "bg-slate-500/20 border border-slate-500/30 text-slate-300"
        }`}>
          {loading ? "🔴 LIVE" : "⚪ IDLE"}
        </span>
      </div>

      {/* Logs container - Terminal Style */}
      <div className="flex-1 overflow-hidden flex flex-col bg-black rounded-xl border border-black  -500/20 p-4 relative font-mono text-sm">
        {/* Terminal scanlines effect */}
        <div className="absolute inset-0 pointer-events-none opacity-5 bg-repeat"
          style={{
            backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0, 255, 0, 0.03) 2px, rgba(0, 255, 0, 0.03) 4px)'
          }}
        />
        
        {logs.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-green-600/60">  
            <p className="text-xs m-0 mb-1 text-green-600/70 font-bold">Waiting for input....</p>
          </div>
        ) : (
          <div className="overflow-y-auto flex flex-col gap-0 relative z-10">
            {logs.map((log, idx) => {
              // Determine color based on log content
              let textColor = "text-green-400";
              let accentColor = "text-green-500";
              
              if (log.includes("❌") || log.includes("Error")) {
                textColor = "text-red-400";
                accentColor = "text-red-500";
              } else if (log.includes("✅") || log.includes("saved")) {
                textColor = "text-lime-400";
                accentColor = "text-lime-500";
              } else if (log.includes("📧") || log.includes("📂")) {
                textColor = "text-cyan-400";
                accentColor = "text-cyan-500";
              }

              return (
                <div key={idx} className={`flex gap-2.5 py-1 px-2 leading-relaxed ${textColor} hover:bg-green-900/10 transition-colors`}>
                  <span className={`${accentColor} font-bold min-w-fit flex-shrink-0 opacity-70`}>
                    [{new Date().toLocaleTimeString()}]
                  </span>
                  <span className="flex-1 break-words opacity-90 font-medium">{log}</span>
                </div>
              )
            })}
            {/* Terminal cursor */}
            <div className="flex gap-2.5 pt-1 px-2">
              <span className="text-green-500 font-bold opacity-70 min-w-fit">▌</span>
              <span className="text-green-400/50 text-xs">Waiting for next event...</span>
            </div>
          </div>
        )}
      </div>

      {/* Terminal info footer */}
      <div className="mt-3 pt-2 border-t border-slate-600/30 text-xs text-slate-500 flex justify-between">
        <span>Terminal &gt; Agent Logs</span>
        <span>{logs.length} events</span>
      </div>
    </div>
  )
}

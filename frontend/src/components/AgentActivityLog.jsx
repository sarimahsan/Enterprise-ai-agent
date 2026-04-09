export default function AgentActivityLog({ logs, loading }) {
  return (
    <div className="h-full flex flex-col bg-slate-800 border border-slate-700 rounded-lg p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-4 pb-3 border-b border-slate-700">
        <h2 className="text-lg font-bold text-slate-200 m-0">🤖 Agent Activity Log</h2>
        <span className={`text-xs font-semibold px-2.5 py-1 rounded ${loading ? "text-purple-400" : "text-slate-400"}`}>
          {loading ? "🔵 LIVE" : "⚪ IDLE"}
        </span>
      </div>

      {/* Logs container */}
      <div className="flex-1 overflow-hidden flex flex-col">
        {logs.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-slate-500">
            <div className="text-4xl mb-3">📭</div>
            <p className="text-sm font-medium m-0 mb-1">Waiting for agent logs...</p>
            <p className="text-xs text-slate-600 m-0">Generate a campaign to see live updates</p>
          </div>
        ) : (
          <div className="overflow-y-auto bg-slate-900 rounded p-3 flex flex-col gap-1">
            {logs.map((log, idx) => (
              <div key={idx} className="flex gap-2.5 p-2 text-xs font-mono leading-relaxed rounded">
                <span className="text-slate-500 font-semibold min-w-fit">[{new Date().toLocaleTimeString()}]</span>
                <span className="text-slate-300 flex-1 break-words">{log}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

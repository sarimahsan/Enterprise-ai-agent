export default function IntelligenceCards({ analysis }) {
  const cards = [
    { icon: "🎯", title: "Opportunity ID", value: analysis.opportunity },
    { icon: "👤", title: "Decision Maker", value: analysis.decision_maker },
    { icon: "📌", title: "Key Facts", value: analysis.key_fact },
    { icon: "⚠️", title: "Pain Points", value: analysis.pain_points?.join(", ") || "N/A" },
  ]

  return (
    <div className="bg-black/40 backdrop-blur-sm border border-white/10 rounded-lg p-6 shadow-lg">
      <h2 className="text-xl font-bold text-slate-200 mb-4">🧠 Intelligence Cards</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {cards.map((card, idx) => (
          <div key={idx} className="bg-slate-900 border border-slate-700 rounded-lg p-4 text-center">
            <div className="text-3xl mb-2">{card.icon}</div>
            <div className="text-xs font-semibold text-purple-400 uppercase mb-2">{card.title}</div>
            <div className="text-sm text-slate-300 leading-relaxed line-clamp-3">{card.value}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

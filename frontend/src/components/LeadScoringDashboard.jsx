import React, { useState } from 'react'
import { Search, Filter, Globe, MapPin, Target, Zap } from 'lucide-react'

const API_URL = 'http://localhost:8000/api'

export const LeadScoringDashboard = ({ onStartCampaign }) => {
  const [searchQuery, setSearchQuery] = useState('')
  const [companies, setCompanies] = useState([])
  const [loading, setLoading] = useState(false)
  const [filterUrgency, setFilterUrgency] = useState('all')
  const [error, setError] = useState('')

  const searchCompanies = async () => {
    if (!searchQuery.trim()) {
      setError('Please enter a company name')
      return
    }

    try {
      setLoading(true)
      setError('')
      setCompanies([])

      // Call backend to search for companies on web
      const response = await fetch(`${API_URL}/companies/search-web`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery })
      })

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || 'Failed to search companies')
      }

      const data = await response.json()
      setCompanies(data.companies || [])

      if (!data.companies || data.companies.length === 0) {
        setError('No companies found. Try a different search term.')
      }
    } catch (err) {
      console.error('Error searching companies:', err)
      setError(err.message || 'Failed to search companies')
    } finally {
      setLoading(false)
    }
  }

  const handleStartCampaign = (company) => {
    if (onStartCampaign) {
      onStartCampaign(company.name)
    }
  }


  const filteredCompanies = filterUrgency === 'all'
    ? companies
    : companies.filter(c => c.urgency_level === filterUrgency)

  const getUrgencyBadgeColor = (urgency) => {
    const colors = {
      critical: 'bg-red-500/20 text-red-400 border-red-500/30',
      high: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
      medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
      low: 'bg-green-500/20 text-green-400 border-green-500/30'
    }
    return colors[urgency] || colors.medium
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'from-green-500 to-emerald-500'
    if (score >= 60) return 'from-yellow-500 to-orange-500'
    if (score >= 40) return 'from-orange-500 to-red-500'
    return 'from-red-500 to-red-600'
  }

  return (
    <div className="h-full w-full flex flex-col gap-6 p-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Lead Scoring Dashboard</h1>
        <p className="text-slate-400">Search for companies and launch targeted campaigns</p>
      </div>

      {/* Search Section */}
      <div className="bg-slate-800/40 border border-slate-700/50 rounded-lg p-6">
        <label className="block text-sm font-medium text-slate-300 mb-3">Search Company</label>
        <div className="flex gap-3">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && searchCompanies()}
            placeholder="e.g., Microsoft, Google, Stripe..."
            className="flex-1 px-4 py-2 bg-slate-900/50 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />
          <button
            onClick={searchCompanies}
            disabled={loading}
            className="px-6 py-2 bg-cyan-500/20 border border-cyan-500/30 rounded-lg text-cyan-400 hover:bg-cyan-500/30 transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            <Search size={18} />
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 text-red-400">
          {error}
        </div>
      )}

      {/* Filters */}
      {companies.length > 0 && (
        <div className="flex items-center gap-4">
          <Filter size={18} className="text-slate-400" />
          <select
            value={filterUrgency}
            onChange={(e) => setFilterUrgency(e.target.value)}
            className="px-3 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white text-sm"
          >
            <option value="all">All Urgency Levels</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
          <div className="ml-auto text-slate-400 text-sm">
            {filteredCompanies.length} of {companies.length} results
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin">
            <div className="w-8 h-8 border-4 border-slate-600 border-t-cyan-400 rounded-full"></div>
          </div>
          <p className="mt-4 text-slate-400">Searching companies...</p>
        </div>
      )}

      {/* Empty State */}
      {!loading && companies.length === 0 && !error && (
        <div className="text-center py-16 bg-slate-800/20 border border-slate-700/50 rounded-lg">
          <Globe size={48} className="mx-auto text-slate-600 mb-4" />
          <p className="text-slate-400 mb-2">Search for companies to get started</p>
          <p className="text-slate-500 text-sm">Enter a company name and click Search to discover leads</p>
        </div>
      )}

      {/* Companies Grid */}
      {!loading && filteredCompanies.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {filteredCompanies.map((company, idx) => (
            <div key={idx} className="bg-slate-800/40 border border-slate-700/50 rounded-lg p-4 hover:border-slate-600 transition-colors flex flex-col">
              {/* Company Info */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-white mb-1">{company.name}</h3>
                  <div className="flex items-center gap-3 text-xs text-slate-400">
                    {company.industry && (
                      <span className="flex items-center gap-1">
                        <Target size={14} />
                        {company.industry}
                      </span>
                    )}
                    {company.decision_maker && (
                      <span className="flex items-center gap-1">
                        <MapPin size={14} />
                        {company.decision_maker}
                      </span>
                    )}
                  </div>
                </div>
                <div className={`px-3 py-1 rounded-lg border text-xs font-semibold ${getUrgencyBadgeColor(company.urgency_level)}`}>
                  {company.urgency_level?.toUpperCase() || 'MEDIUM'}
                </div>
              </div>

              {/* Scores */}
              <div className="space-y-3 mb-4 flex-1">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-slate-400">Opportunity</span>
                    <span className="text-lg font-bold text-white">{company.opportunity_score || 0}/100</span>
                  </div>
                  <div className="w-full bg-slate-700/50 rounded-full h-2 overflow-hidden">
                    <div
                      className={`h-full bg-gradient-to-r ${getScoreColor(company.opportunity_score || 0)}`}
                      style={{ width: `${company.opportunity_score || 0}%` }}
                    ></div>
                  </div>
                </div>
                {company.fit_score > 0 && (
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-slate-400">Fit Score</span>
                      <span className="text-lg font-bold text-white">{company.fit_score || 0}/100</span>
                    </div>
                    <div className="w-full bg-slate-700/50 rounded-full h-2 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
                        style={{ width: `${company.fit_score || 0}%` }}
                      ></div>
                    </div>
                  </div>
                )}
              </div>

              {/* Start Campaign Button */}
              <button 
                onClick={() => handleStartCampaign(company)}
                className="w-full px-4 py-2 bg-cyan-500/20 border border-cyan-500/30 rounded-lg text-cyan-400 hover:bg-cyan-500/30 transition-colors text-sm font-medium flex items-center justify-center gap-2"
              >
                <Zap size={16} />
                Start Campaign
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default LeadScoringDashboard

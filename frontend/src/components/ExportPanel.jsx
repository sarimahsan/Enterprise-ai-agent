import React, { useState } from 'react'
import { Download, FileText, BookOpen, CheckCircle, AlertCircle } from 'lucide-react'

const API_URL = 'http://localhost:8000/api'

export const ExportPanel = ({ campaignId, campaignData }) => {
  const [exporting, setExporting] = useState(false)
  const [exportResult, setExportResult] = useState(null)
  const [notionDatabaseId, setNotionDatabaseId] = useState('')
  const [showNotionInput, setShowNotionInput] = useState(false)

  const exportToNotion = async () => {
    if (!notionDatabaseId.trim()) {
      alert('Please enter your Notion Database ID')
      return
    }

    try {
      setExporting(true)
      const response = await fetch(`${API_URL}/export/to-notion`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          campaign_id: campaignId,
          notion_database_id: notionDatabaseId,
          include_emails: true,
          include_objections: true
        })
      })

      const data = await response.json()
      
      if (response.ok) {
        setExportResult({
          type: 'notion',
          success: true,
          notionPageId: data.notion_page_id,
          message: data.message
        })
        setShowNotionInput(false)
      } else {
        setExportResult({
          type: 'notion',
          success: false,
          message: data.detail || 'Failed to export to Notion'
        })
      }
    } catch (error) {
      console.error('Error exporting to Notion:', error)
      setExportResult({
        type: 'notion',
        success: false,
        message: error.message
      })
    } finally {
      setExporting(false)
    }
  }

  const exportToGoogleDocs = async () => {
    try {
      setExporting(true)
      const response = await fetch(`${API_URL}/export/to-google-docs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          campaign_id: campaignId,
          include_emails: true,
          include_objections: true
        })
      })

      const data = await response.json()

      if (response.ok) {
        setExportResult({
          type: 'google_docs',
          success: true,
          docUrl: data.google_docs_url,
          docId: data.google_doc_id,
          message: data.message
        })
        // Open in new tab
        window.open(data.google_docs_url, '_blank')
      } else {
        setExportResult({
          type: 'google_docs',
          success: false,
          message: data.detail || 'Failed to export to Google Docs'
        })
      }
    } catch (error) {
      console.error('Error exporting to Google Docs:', error)
      setExportResult({
        type: 'google_docs',
        success: false,
        message: error.message
      })
    } finally {
      setExporting(false)
    }
  }

  const saveToDB = async () => {
    try {
      setExporting(true)
      const response = await fetch(`${API_URL}/export/save-to-database`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(campaignData)
      })

      const data = await response.json()

      if (response.ok) {
        setExportResult({
          type: 'database',
          success: true,
          message: data.message
        })
      } else {
        setExportResult({
          type: 'database',
          success: false,
          message: data.detail || 'Failed to save to database'
        })
      }
    } catch (error) {
      console.error('Error saving to database:', error)
      setExportResult({
        type: 'database',
        success: false,
        message: error.message
      })
    } finally {
      setExporting(false)
    }
  }

  return (
    <div className="h-full flex flex-col gap-4 p-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white mb-1">Export Intelligence Report</h2>
        <p className="text-slate-400 text-sm">One-click export to your favorite tools</p>
      </div>

      {/* Export Options */}
      <div className="space-y-3 flex-1">
        {/* Save to Database */}
        <button
          onClick={saveToDB}
          disabled={exporting}
          className="w-full flex items-start gap-4 p-4 bg-slate-800/40 border border-slate-700/50 rounded-lg hover:border-slate-600 transition-colors disabled:opacity-50"
        >
          <div className="mt-1">
            <BookOpen size={24} className="text-slate-400" />
          </div>
          <div className="flex-1 text-left">
            <h4 className="text-white font-bold mb-1">Save to Database</h4>
            <p className="text-sm text-slate-400">Store all campaign data in SQL database for future reference</p>
          </div>
          {exporting && exportResult?.type === 'database' ? (
            <div className="animate-spin">
              <div className="w-5 h-5 border-2 border-slate-600 border-t-cyan-400 rounded-full"></div>
            </div>
          ) : (
            <Download size={20} className="text-slate-400" />
          )}
        </button>

        {/* Export to Google Docs */}
        <button
          onClick={exportToGoogleDocs}
          disabled={exporting}
          className="w-full flex items-start gap-4 p-4 bg-slate-800/40 border border-slate-700/50 rounded-lg hover:border-slate-600 transition-colors disabled:opacity-50"
        >
          <div className="mt-1">
            <FileText size={24} className="text-blue-400" />
          </div>
          <div className="flex-1 text-left">
            <h4 className="text-white font-bold mb-1">Export to Google Docs</h4>
            <p className="text-sm text-slate-400">Create a formatted document with all campaign details</p>
          </div>
          {exporting && exportResult?.type === 'google_docs' ? (
            <div className="animate-spin">
              <div className="w-5 h-5 border-2 border-slate-600 border-t-cyan-400 rounded-full"></div>
            </div>
          ) : (
            <Download size={20} className="text-slate-400" />
          )}
        </button>

        {/* Export to Notion */}
        <div className="border border-slate-700/50 rounded-lg overflow-hidden bg-slate-800/40">
          <button
            onClick={() => setShowNotionInput(!showNotionInput)}
            disabled={exporting}
            className="w-full flex items-start gap-4 p-4 hover:bg-slate-900/30 transition-colors disabled:opacity-50 text-left"
          >
            <div className="mt-1">
              <BookOpen size={24} className="text-purple-400" />
            </div>
            <div className="flex-1">
              <h4 className="text-white font-bold mb-1">Export to Notion</h4>
              <p className="text-sm text-slate-400">Push campaign to your Notion workspace</p>
            </div>
            {exporting && exportResult?.type === 'notion' ? (
              <div className="animate-spin flex-shrink-0">
                <div className="w-5 h-5 border-2 border-slate-600 border-t-cyan-400 rounded-full"></div>
              </div>
            ) : (
              <Download size={20} className="text-slate-400 flex-shrink-0" />
            )}
          </button>

          {/* Notion Input */}
          {showNotionInput && (
            <div className="border-t border-slate-700 px-4 py-3 bg-slate-900/20 space-y-3">
              <div>
                <label className="text-sm text-slate-400 mb-2 block">Notion Database ID</label>
                <input
                  type="text"
                  value={notionDatabaseId}
                  onChange={(e) => setNotionDatabaseId(e.target.value)}
                  placeholder="Your Notion Database ID (32 characters)"
                  className="w-full px-3 py-2 bg-slate-900/50 border border-slate-600 rounded text-white text-sm placeholder-slate-500"
                />
                <p className="text-xs text-slate-500 mt-2">
                  Don't have a Database ID? Create one in Notion, then get it from the URL or share options.
                </p>
              </div>
              <button
                onClick={exportToNotion}
                disabled={exporting || !notionDatabaseId.trim()}
                className="w-full px-4 py-2 bg-purple-500/20 border border-purple-500/30 rounded text-purple-400 hover:bg-purple-500/30 disabled:opacity-50 transition-colors font-medium text-sm"
              >
                {exporting ? 'Exporting...' : 'Export to Notion'}
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Result Message */}
      {exportResult && (
        <div className={`p-4 rounded-lg border flex items-start gap-3 ${
          exportResult.success
            ? 'bg-green-500/10 border-green-500/30'
            : 'bg-red-500/10 border-red-500/30'
        }`}>
          {exportResult.success ? (
            <CheckCircle size={20} className="text-green-400 flex-shrink-0 mt-0.5" />
          ) : (
            <AlertCircle size={20} className="text-red-400 flex-shrink-0 mt-0.5" />
          )}
          <div className="flex-1">
            <p className={`text-sm ${exportResult.success ? 'text-green-300' : 'text-red-300'}`}>
              {exportResult.message}
            </p>
            {exportResult.notionPageId && (
              <p className="text-xs text-slate-400 mt-2">Notion Page ID: {exportResult.notionPageId}</p>
            )}
          </div>
        </div>
      )}

      {/* Info Box */}
      <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-3 text-xs text-blue-300">
        <strong>💡 Pro Tip:</strong> Export to Google Docs for easy sharing with your sales team. Export to Notion to integrate with your deal pipeline.
      </div>
    </div>
  )
}

export default ExportPanel

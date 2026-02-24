import { useState, useEffect } from 'react';
import { Send, X } from 'lucide-react';
import StatsCard from '../components/StatsCard';
import DataTable, { type Column } from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';
import api from '../lib/api';
import {
  Users,
  Mail,
  MessageSquare,
  CalendarCheck,
  Trophy,
} from 'lucide-react';

interface Lead {
  id: string;
  name: string;
  company: string;
  email: string;
  status: string;
  market: string;
  language: string;
  sequence_step: number;
  total_steps: number;
  last_contacted: string;
  [key: string]: unknown;
}

interface OutreachStats {
  total_leads: number;
  contacted: number;
  replied: number;
  meetings: number;
  won: number;
}

interface OutreachHistoryItem {
  step: number;
  type: string;
  subject: string;
  sent_at: string;
  status: string;
}

const mockStats: OutreachStats = {
  total_leads: 245,
  contacted: 156,
  replied: 42,
  meetings: 18,
  won: 8,
};

const mockLeads: Lead[] = [
  { id: 'l1', name: 'John Smith', company: 'Alpha Tech Inc', email: 'john@alphatech.com', status: 'contacted', market: 'UK', language: 'en', sequence_step: 2, total_steps: 5, last_contacted: '2026-02-22' },
  { id: 'l2', name: 'Maria Garcia', company: 'Bella Properties', email: 'maria@bellaprops.ae', status: 'replied', market: 'Dubai', language: 'en', sequence_step: 3, total_steps: 5, last_contacted: '2026-02-21' },
  { id: 'l3', name: 'Ivan Petrov', company: 'RussoTech', email: 'ivan@russotech.ru', status: 'meeting', market: 'Russian Dubai', language: 'ru', sequence_step: 4, total_steps: 5, last_contacted: '2026-02-20' },
  { id: 'l4', name: 'Lisa Brown', company: 'BrownStone Digital', email: 'lisa@brownstone.co.uk', status: 'contacted', market: 'UK', language: 'en', sequence_step: 1, total_steps: 5, last_contacted: '2026-02-23' },
  { id: 'l5', name: 'Omar Khalil', company: 'Desert Ventures', email: 'omar@desertventures.ae', status: 'won', market: 'Dubai', language: 'ar', sequence_step: 5, total_steps: 5, last_contacted: '2026-02-15' },
  { id: 'l6', name: 'Anna Volkov', company: 'Stellar Holdings', email: 'anna@stellar.ae', status: 'lead', market: 'Russian Dubai', language: 'ru', sequence_step: 0, total_steps: 5, last_contacted: '' },
  { id: 'l7', name: 'David Wilson', company: 'WilsonTech Group', email: 'david@wilsontech.com', status: 'not_interested', market: 'Global', language: 'en', sequence_step: 3, total_steps: 5, last_contacted: '2026-02-18' },
  { id: 'l8', name: 'Aisha Rahman', company: 'Gulf Excellence', email: 'aisha@gulfexcellence.ae', status: 'contacted', market: 'Dubai', language: 'en', sequence_step: 2, total_steps: 5, last_contacted: '2026-02-22' },
  { id: 'l9', name: 'Mark Taylor', company: 'TaylorMade SaaS', email: 'mark@taylormade.io', status: 'replied', market: 'UK', language: 'en', sequence_step: 3, total_steps: 5, last_contacted: '2026-02-19' },
  { id: 'l10', name: 'Svetlana Kuznetsova', company: 'Kuznetsova Consulting', email: 'svetlana@kc.ae', status: 'meeting', market: 'Russian Dubai', language: 'ru', sequence_step: 4, total_steps: 5, last_contacted: '2026-02-20' },
];

const LEAD_STATUS_FILTERS = ['All', 'Lead', 'Contacted', 'Replied', 'Meeting', 'Won', 'Not Interested'];
const MARKET_FILTERS = ['All', 'Dubai', 'UK', 'Global', 'Russian Dubai'];
const LANGUAGE_FILTERS = ['All', 'en', 'ar', 'ru'];

export default function OutreachPage() {
  const [stats, setStats] = useState<OutreachStats>(mockStats);
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('All');
  const [marketFilter, setMarketFilter] = useState('All');
  const [languageFilter, setLanguageFilter] = useState('All');
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const [batchLoading, setBatchLoading] = useState(false);

  useEffect(() => {
    const fetchOutreach = async () => {
      try {
        const [statsRes, leadsRes] = await Promise.all([
          api.get('/outreach/stats'),
          api.get('/outreach/leads'),
        ]);
        setStats(statsRes.data);
        setLeads(leadsRes.data);
      } catch {
        setStats(mockStats);
        setLeads(mockLeads);
      } finally {
        setLoading(false);
      }
    };
    fetchOutreach();
  }, []);

  const filtered = leads.filter((l) => {
    const statusMatch =
      statusFilter === 'All' ||
      l.status.toLowerCase().replace(/_/g, ' ') === statusFilter.toLowerCase();
    const marketMatch = marketFilter === 'All' || l.market === marketFilter;
    const langMatch = languageFilter === 'All' || l.language === languageFilter;
    return statusMatch && marketMatch && langMatch;
  });

  const handleGenerateBatch = async () => {
    setBatchLoading(true);
    try {
      await api.post('/outreach/generate-batch');
    } catch {
      // Silently handle
    } finally {
      setTimeout(() => setBatchLoading(false), 2000);
    }
  };

  const columns: Column<Lead>[] = [
    { key: 'name', label: 'Name', sortable: true },
    { key: 'company', label: 'Company', sortable: true },
    {
      key: 'status',
      label: 'Status',
      sortable: true,
      render: (row) => <StatusBadge status={row.status} />,
    },
    { key: 'market', label: 'Market', sortable: true },
    { key: 'language', label: 'Lang', sortable: true },
    {
      key: 'sequence_step',
      label: 'Sequence',
      sortable: true,
      render: (row) => (
        <div className="flex items-center gap-2">
          <div className="flex gap-0.5">
            {Array.from({ length: row.total_steps }, (_, i) => (
              <div
                key={i}
                className={`w-4 h-1.5 rounded-full ${
                  i < row.sequence_step
                    ? 'bg-blue-500'
                    : 'bg-slate-700'
                }`}
              />
            ))}
          </div>
          <span className="text-xs text-slate-500">
            {row.sequence_step}/{row.total_steps}
          </span>
        </div>
      ),
    },
    {
      key: 'last_contacted',
      label: 'Last Contacted',
      sortable: true,
      render: (row) => (
        <span className="text-slate-400">
          {row.last_contacted || 'Never'}
        </span>
      ),
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-blue-500/30 border-t-blue-500 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-100">Outreach</h2>
        <button
          onClick={handleGenerateBatch}
          disabled={batchLoading}
          className="btn-primary flex items-center gap-2"
        >
          <Send size={16} />
          {batchLoading ? 'Generating...' : 'Generate Batch'}
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        <StatsCard icon={Users} label="Total Leads" value={stats.total_leads} iconColor="text-blue-400" />
        <StatsCard icon={Mail} label="Contacted" value={stats.contacted} iconColor="text-cyan-400" />
        <StatsCard icon={MessageSquare} label="Replied" value={stats.replied} iconColor="text-purple-400" />
        <StatsCard icon={CalendarCheck} label="Meetings" value={stats.meetings} iconColor="text-orange-400" />
        <StatsCard icon={Trophy} label="Won" value={stats.won} iconColor="text-green-400" />
      </div>

      {/* Filters */}
      <div className="space-y-3">
        <div className="flex flex-wrap gap-2">
          <span className="text-sm text-slate-400 py-1.5 mr-1">Status:</span>
          {LEAD_STATUS_FILTERS.map((s) => (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                statusFilter === s
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-700'
              }`}
            >
              {s}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          <span className="text-sm text-slate-400 py-1.5 mr-1">Market:</span>
          {MARKET_FILTERS.map((m) => (
            <button
              key={m}
              onClick={() => setMarketFilter(m)}
              className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                marketFilter === m
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-700'
              }`}
            >
              {m}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          <span className="text-sm text-slate-400 py-1.5 mr-1">Language:</span>
          {LANGUAGE_FILTERS.map((l) => (
            <button
              key={l}
              onClick={() => setLanguageFilter(l)}
              className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                languageFilter === l
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-700'
              }`}
            >
              {l === 'All' ? 'All' : l.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Leads Table */}
      <div className="card p-0 overflow-hidden">
        <DataTable
          columns={columns}
          data={filtered}
          keyExtractor={(row) => row.id}
          onRowClick={(row) => setSelectedLead(row)}
          pageSize={10}
          emptyMessage="No leads match the current filters."
        />
      </div>

      {/* Lead Detail Panel */}
      {selectedLead && (
        <LeadDetailPanel
          lead={selectedLead}
          onClose={() => setSelectedLead(null)}
        />
      )}
    </div>
  );
}

function LeadDetailPanel({
  lead,
  onClose,
}: {
  lead: Lead;
  onClose: () => void;
}) {
  const mockHistory: OutreachHistoryItem[] = [
    { step: 1, type: 'email', subject: 'Growth opportunity for your business', sent_at: '2026-02-15', status: 'delivered' },
    { step: 2, type: 'email', subject: 'Follow-up: AI-powered marketing insights', sent_at: '2026-02-18', status: 'delivered' },
    { step: 3, type: 'linkedin', subject: 'Connection request + message', sent_at: '2026-02-20', status: 'sent' },
  ].slice(0, lead.sequence_step);

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/40">
      <div className="absolute inset-0" onClick={onClose} />
      <div className="relative w-full max-w-md bg-slate-800 border-l border-slate-700 h-full overflow-y-auto p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-slate-100">
            Lead Details
          </h3>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-200"
          >
            <X size={20} />
          </button>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <div>
              <p className="text-sm text-slate-400">Name</p>
              <p className="text-slate-200 font-medium">{lead.name}</p>
            </div>
            <div>
              <p className="text-sm text-slate-400">Company</p>
              <p className="text-slate-200">{lead.company}</p>
            </div>
            <div>
              <p className="text-sm text-slate-400">Email</p>
              <p className="text-slate-200">{lead.email}</p>
            </div>
            <div className="flex gap-6">
              <div>
                <p className="text-sm text-slate-400">Market</p>
                <p className="text-slate-200">{lead.market}</p>
              </div>
              <div>
                <p className="text-sm text-slate-400">Language</p>
                <p className="text-slate-200">{lead.language.toUpperCase()}</p>
              </div>
            </div>
            <div>
              <p className="text-sm text-slate-400 mb-1">Status</p>
              <StatusBadge status={lead.status} />
            </div>
          </div>

          {/* Sequence Progress */}
          <div>
            <p className="text-sm text-slate-400 mb-3">Sequence Progress</p>
            <div className="flex items-center gap-1 mb-2">
              {Array.from({ length: lead.total_steps }, (_, i) => (
                <div
                  key={i}
                  className={`flex-1 h-2 rounded-full ${
                    i < lead.sequence_step ? 'bg-blue-500' : 'bg-slate-700'
                  }`}
                />
              ))}
            </div>
            <p className="text-xs text-slate-500">
              Step {lead.sequence_step} of {lead.total_steps}
            </p>
          </div>

          {/* Outreach History */}
          <div>
            <p className="text-sm text-slate-400 mb-3">Outreach History</p>
            {mockHistory.length === 0 ? (
              <p className="text-sm text-slate-500">No outreach yet.</p>
            ) : (
              <div className="space-y-3">
                {mockHistory.map((item, idx) => (
                  <div
                    key={idx}
                    className="bg-slate-700/50 rounded-lg p-3"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-medium text-slate-400 uppercase">
                        Step {item.step} - {item.type}
                      </span>
                      <StatusBadge status={item.status} />
                    </div>
                    <p className="text-sm text-slate-300">{item.subject}</p>
                    <p className="text-xs text-slate-500 mt-1">{item.sent_at}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

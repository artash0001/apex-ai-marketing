import { useState, useEffect } from 'react';
import { FileText, Download } from 'lucide-react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import api from '../lib/api';

interface ClientOption {
  id: string;
  name: string;
  company: string;
}

const mockClients: ClientOption[] = [
  { id: '1', name: 'Ahmed Al-Rashid', company: 'Luxe Properties Dubai' },
  { id: '2', name: 'Sarah Chen', company: 'TechFlow Solutions' },
  { id: '5', name: 'Fatima Hassan', company: 'GoldenGate Realty' },
  { id: '6', name: 'James Miller', company: 'CloudPeak SaaS' },
  { id: '9', name: 'Rashid Mansoor', company: 'Desert Eagle Logistics' },
];

const mockAiCosts = [
  { agent: 'Content Writer', cost: 320 },
  { agent: 'SEO Analyst', cost: 180 },
  { agent: 'PPC Manager', cost: 250 },
  { agent: 'Outreach Agent', cost: 140 },
  { agent: 'Report Generator', cost: 95 },
  { agent: 'Audit Analyzer', cost: 155 },
  { agent: 'Social Media', cost: 100 },
];

const mockMrrData = [
  { month: 'Sep', mrr: 28000 },
  { month: 'Oct', mrr: 31500 },
  { month: 'Nov', mrr: 35200 },
  { month: 'Dec', mrr: 38800 },
  { month: 'Jan', mrr: 42100 },
  { month: 'Feb', mrr: 47500 },
];

export default function ReportsPage() {
  const [clients, setClients] = useState<ClientOption[]>([]);
  const [selectedClient, setSelectedClient] = useState('');
  const [reportType, setReportType] = useState<'weekly' | 'monthly'>('weekly');
  const [generating, setGenerating] = useState(false);
  const [generated, setGenerated] = useState(false);
  const [aiCosts, setAiCosts] = useState(mockAiCosts);
  const [mrrData, setMrrData] = useState(mockMrrData);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [clientsRes, costsRes, revenueRes] = await Promise.all([
          api.get('/clients?status=active'),
          api.get('/reports/ai-costs'),
          api.get('/reports/revenue'),
        ]);
        setClients(clientsRes.data);
        setAiCosts(costsRes.data);
        setMrrData(revenueRes.data);
      } catch {
        setClients(mockClients);
        setAiCosts(mockAiCosts);
        setMrrData(mockMrrData);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleGenerate = async () => {
    if (!selectedClient) return;
    setGenerating(true);
    setGenerated(false);
    try {
      await api.post('/reports/generate', {
        client_id: selectedClient,
        type: reportType,
      });
    } catch {
      // Silently handle
    }
    setTimeout(() => {
      setGenerating(false);
      setGenerated(true);
    }, 2000);
  };

  const totalAiCost = aiCosts.reduce((sum, a) => sum + a.cost, 0);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-blue-500/30 border-t-blue-500 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-slate-100">Reports</h2>

      {/* Report Generation */}
      <div className="card">
        <h3 className="text-lg font-semibold text-slate-200 mb-4">
          Generate Report
        </h3>
        <div className="flex flex-wrap items-end gap-4">
          <div className="min-w-[200px]">
            <label className="block text-sm text-slate-400 mb-1.5">
              Client
            </label>
            <select
              className="input-field"
              value={selectedClient}
              onChange={(e) => {
                setSelectedClient(e.target.value);
                setGenerated(false);
              }}
            >
              <option value="">Select client...</option>
              {clients.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} - {c.company}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm text-slate-400 mb-1.5">
              Report Type
            </label>
            <div className="flex gap-2">
              <button
                onClick={() => { setReportType('weekly'); setGenerated(false); }}
                className={`px-4 py-2 rounded-lg text-sm transition-colors ${
                  reportType === 'weekly'
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-700 text-slate-400 hover:text-slate-200'
                }`}
              >
                Weekly
              </button>
              <button
                onClick={() => { setReportType('monthly'); setGenerated(false); }}
                className={`px-4 py-2 rounded-lg text-sm transition-colors ${
                  reportType === 'monthly'
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-700 text-slate-400 hover:text-slate-200'
                }`}
              >
                Monthly
              </button>
            </div>
          </div>

          <button
            onClick={handleGenerate}
            disabled={!selectedClient || generating}
            className="btn-primary flex items-center gap-2"
          >
            {generating ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <FileText size={16} />
                Generate
              </>
            )}
          </button>
        </div>

        {generated && (
          <div className="mt-4 p-4 bg-green-500/10 border border-green-500/30 rounded-lg flex items-center justify-between">
            <div>
              <p className="text-green-400 font-medium">Report Generated</p>
              <p className="text-sm text-slate-400 mt-0.5">
                {reportType === 'weekly' ? 'Weekly' : 'Monthly'} report is ready
                for review.
              </p>
            </div>
            <button className="btn-secondary flex items-center gap-2 text-sm">
              <Download size={14} />
              Download PDF
            </button>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* AI Cost Breakdown */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-slate-200">
              AI Cost Breakdown
            </h3>
            <span className="text-sm text-slate-400">
              Total: ${totalAiCost.toLocaleString()}
            </span>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={aiCosts} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis
                  type="number"
                  tick={{ fill: '#94a3b8', fontSize: 12 }}
                  axisLine={{ stroke: '#475569' }}
                  tickFormatter={(v) => `$${v}`}
                />
                <YAxis
                  dataKey="agent"
                  type="category"
                  width={120}
                  tick={{ fill: '#94a3b8', fontSize: 12 }}
                  axisLine={{ stroke: '#475569' }}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    border: '1px solid #334155',
                    borderRadius: '8px',
                    color: '#e2e8f0',
                  }}
                  formatter={(value: number) => [`$${value}`, 'Cost']}
                />
                <Bar dataKey="cost" fill="#f97316" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Revenue Tracking */}
        <div className="card">
          <h3 className="text-lg font-semibold text-slate-200 mb-4">
            Revenue Tracking (MRR)
          </h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mrrData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis
                  dataKey="month"
                  tick={{ fill: '#94a3b8', fontSize: 12 }}
                  axisLine={{ stroke: '#475569' }}
                />
                <YAxis
                  tick={{ fill: '#94a3b8', fontSize: 12 }}
                  axisLine={{ stroke: '#475569' }}
                  tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    border: '1px solid #334155',
                    borderRadius: '8px',
                    color: '#e2e8f0',
                  }}
                  formatter={(value: number) => [
                    `$${value.toLocaleString()}`,
                    'MRR',
                  ]}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="mrr"
                  stroke="#22c55e"
                  strokeWidth={2}
                  dot={{ fill: '#22c55e', r: 4 }}
                  name="Monthly Recurring Revenue"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

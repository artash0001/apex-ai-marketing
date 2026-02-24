import { useState, useEffect } from 'react';
import { Plus, X } from 'lucide-react';
import DataTable, { type Column } from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';
import api from '../lib/api';

interface Experiment {
  id: string;
  client: string;
  hypothesis: string;
  status: string;
  result: string;
  decision: string;
  engine: string;
  start_date: string;
  end_date: string;
  metrics: { label: string; control: string; variant: string }[];
  notes: string;
  [key: string]: unknown;
}

const mockExperiments: Experiment[] = [
  {
    id: 'EXP-001', client: 'Luxe Properties Dubai', hypothesis: 'Shorter CTAs increase click-through rate on property listings',
    status: 'won', result: '+23% CTR improvement', decision: 'Implement across all listings',
    engine: 'Content Engine', start_date: '2026-01-15', end_date: '2026-02-15',
    metrics: [
      { label: 'Click-Through Rate', control: '2.1%', variant: '2.6%' },
      { label: 'Bounce Rate', control: '45%', variant: '38%' },
    ],
    notes: 'Clear winner. Shorter CTAs consistently outperformed across all property types.',
  },
  {
    id: 'EXP-002', client: 'TechFlow Solutions', hypothesis: 'Video thumbnails in blog posts increase time on page',
    status: 'running', result: 'Pending', decision: 'Pending',
    engine: 'Content Engine', start_date: '2026-02-10', end_date: '',
    metrics: [
      { label: 'Time on Page', control: '2m 15s', variant: '3m 45s' },
      { label: 'Scroll Depth', control: '62%', variant: '78%' },
    ],
    notes: 'Promising early results. Need more data for statistical significance.',
  },
  {
    id: 'EXP-003', client: 'GoldenGate Realty', hypothesis: 'Arabic-first landing pages convert better for Dubai market',
    status: 'won', result: '+18% conversion rate', decision: 'Create Arabic variants for top 10 pages',
    engine: 'SEO Engine', start_date: '2026-01-05', end_date: '2026-02-05',
    metrics: [
      { label: 'Conversion Rate', control: '3.2%', variant: '3.8%' },
      { label: 'Form Completions', control: '45/day', variant: '53/day' },
    ],
    notes: 'Significant improvement. Arabic-first approach resonates with local audience.',
  },
  {
    id: 'EXP-004', client: 'CloudPeak SaaS', hypothesis: 'Reducing form fields from 8 to 4 increases lead gen',
    status: 'lost', result: '-5% qualified leads', decision: 'Revert to original form',
    engine: 'PPC Engine', start_date: '2026-01-20', end_date: '2026-02-20',
    metrics: [
      { label: 'Form Submissions', control: '120/week', variant: '145/week' },
      { label: 'Qualified Leads', control: '35/week', variant: '28/week' },
    ],
    notes: 'More submissions but lower quality. Additional fields help qualify leads.',
  },
  {
    id: 'EXP-005', client: 'Desert Eagle Logistics', hypothesis: 'Case study ads outperform generic service ads',
    status: 'running', result: 'Pending', decision: 'Pending',
    engine: 'PPC Engine', start_date: '2026-02-18', end_date: '',
    metrics: [
      { label: 'CTR', control: '1.8%', variant: '2.4%' },
      { label: 'Cost per Lead', control: '$45', variant: '$38' },
    ],
    notes: 'Early signs of improvement. Running for 2 more weeks.',
  },
  {
    id: 'EXP-006', client: 'Luxe Properties Dubai', hypothesis: 'Personalized email subject lines increase open rates',
    status: 'inconclusive', result: 'No significant difference', decision: 'Run extended test with larger sample',
    engine: 'Email Engine', start_date: '2026-01-25', end_date: '2026-02-10',
    metrics: [
      { label: 'Open Rate', control: '28%', variant: '29.5%' },
      { label: 'Click Rate', control: '4.2%', variant: '4.5%' },
    ],
    notes: 'Results not statistically significant. Need larger sample size.',
  },
];

const STATUS_FILTERS = ['All', 'Running', 'Won', 'Lost', 'Inconclusive'];

export default function ExperimentsPage() {
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('All');
  const [clientFilter, setClientFilter] = useState('All');
  const [selectedExp, setSelectedExp] = useState<Experiment | null>(null);
  const [showNewModal, setShowNewModal] = useState(false);

  useEffect(() => {
    const fetchExperiments = async () => {
      try {
        const res = await api.get('/experiments');
        setExperiments(res.data);
      } catch {
        setExperiments(mockExperiments);
      } finally {
        setLoading(false);
      }
    };
    fetchExperiments();
  }, []);

  const clients = ['All', ...Array.from(new Set(experiments.map((e) => e.client)))];

  const filtered = experiments.filter((e) => {
    const statusMatch = statusFilter === 'All' || e.status.toLowerCase() === statusFilter.toLowerCase();
    const clientMatch = clientFilter === 'All' || e.client === clientFilter;
    return statusMatch && clientMatch;
  });

  const columns: Column<Experiment>[] = [
    { key: 'id', label: 'ID', sortable: true, className: 'w-28' },
    { key: 'client', label: 'Client', sortable: true },
    {
      key: 'hypothesis',
      label: 'Hypothesis',
      sortable: false,
      render: (row) => (
        <span className="line-clamp-1" title={row.hypothesis}>
          {row.hypothesis}
        </span>
      ),
    },
    {
      key: 'status',
      label: 'Status',
      sortable: true,
      render: (row) => <StatusBadge status={row.status} />,
    },
    {
      key: 'result',
      label: 'Result',
      sortable: false,
      render: (row) => (
        <span className={
          row.status === 'won' ? 'text-green-400' :
          row.status === 'lost' ? 'text-red-400' :
          'text-slate-400'
        }>
          {row.result}
        </span>
      ),
    },
    {
      key: 'decision',
      label: 'Decision',
      sortable: false,
      render: (row) => (
        <span className="text-slate-400 line-clamp-1" title={row.decision}>
          {row.decision}
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
        <h2 className="text-2xl font-bold text-slate-100">Experiments</h2>
        <button
          onClick={() => setShowNewModal(true)}
          className="btn-primary flex items-center gap-2"
        >
          <Plus size={16} />
          New Experiment
        </button>
      </div>

      {/* Filters */}
      <div className="space-y-3">
        <div className="flex flex-wrap gap-2">
          <span className="text-sm text-slate-400 py-1.5 mr-1">Status:</span>
          {STATUS_FILTERS.map((s) => (
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
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-sm text-slate-400 mr-1">Client:</span>
          <select
            className="input-field max-w-xs"
            value={clientFilter}
            onChange={(e) => setClientFilter(e.target.value)}
          >
            {clients.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="card p-0 overflow-hidden">
        <DataTable
          columns={columns}
          data={filtered}
          keyExtractor={(row) => row.id}
          onRowClick={(row) => setSelectedExp(row)}
          pageSize={10}
          emptyMessage="No experiments match the current filters."
        />
      </div>

      {/* Experiment Detail Panel */}
      {selectedExp && (
        <ExperimentDetailPanel
          experiment={selectedExp}
          onClose={() => setSelectedExp(null)}
        />
      )}

      {/* New Experiment Modal */}
      {showNewModal && (
        <NewExperimentModal
          onClose={() => setShowNewModal(false)}
          onAdd={(exp) => {
            setExperiments((prev) => [exp, ...prev]);
            setShowNewModal(false);
          }}
        />
      )}
    </div>
  );
}

function ExperimentDetailPanel({
  experiment,
  onClose,
}: {
  experiment: Experiment;
  onClose: () => void;
}) {
  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/40">
      <div className="absolute inset-0" onClick={onClose} />
      <div className="relative w-full max-w-lg bg-slate-800 border-l border-slate-700 h-full overflow-y-auto p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-slate-100">
            {experiment.id}
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200">
            <X size={20} />
          </button>
        </div>

        <div className="space-y-6">
          <div>
            <p className="text-sm text-slate-400">Client</p>
            <p className="text-slate-200 font-medium">{experiment.client}</p>
          </div>

          <div>
            <p className="text-sm text-slate-400">Engine</p>
            <p className="text-slate-200">{experiment.engine}</p>
          </div>

          <div>
            <p className="text-sm text-slate-400">Hypothesis</p>
            <p className="text-slate-200">{experiment.hypothesis}</p>
          </div>

          <div className="flex gap-6">
            <div>
              <p className="text-sm text-slate-400 mb-1">Status</p>
              <StatusBadge status={experiment.status} />
            </div>
            <div>
              <p className="text-sm text-slate-400">Start Date</p>
              <p className="text-slate-200">{experiment.start_date}</p>
            </div>
            {experiment.end_date && (
              <div>
                <p className="text-sm text-slate-400">End Date</p>
                <p className="text-slate-200">{experiment.end_date}</p>
              </div>
            )}
          </div>

          <div>
            <p className="text-sm text-slate-400">Result</p>
            <p className={`font-medium ${
              experiment.status === 'won' ? 'text-green-400' :
              experiment.status === 'lost' ? 'text-red-400' :
              'text-slate-300'
            }`}>
              {experiment.result}
            </p>
          </div>

          <div>
            <p className="text-sm text-slate-400">Decision</p>
            <p className="text-slate-200">{experiment.decision}</p>
          </div>

          {/* Metrics */}
          <div>
            <p className="text-sm text-slate-400 mb-3">Metrics</p>
            <div className="space-y-3">
              {experiment.metrics.map((m, idx) => (
                <div key={idx} className="bg-slate-700/50 rounded-lg p-3">
                  <p className="text-sm text-slate-300 mb-2">{m.label}</p>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-xs text-slate-500">Control</p>
                      <p className="text-slate-300 font-medium">{m.control}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Variant</p>
                      <p className="text-slate-200 font-medium">{m.variant}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <p className="text-sm text-slate-400">Notes</p>
            <p className="text-slate-300 text-sm">{experiment.notes}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function NewExperimentModal({
  onClose,
  onAdd,
}: {
  onClose: () => void;
  onAdd: (exp: Experiment) => void;
}) {
  const [form, setForm] = useState({
    client: '',
    engine: '',
    hypothesis: '',
  });
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await api.post('/experiments', form);
      onAdd(res.data);
    } catch {
      const newExp: Experiment = {
        id: `EXP-${String(Date.now()).slice(-3)}`,
        client: form.client,
        engine: form.engine,
        hypothesis: form.hypothesis,
        status: 'running',
        result: 'Pending',
        decision: 'Pending',
        start_date: new Date().toISOString().split('T')[0],
        end_date: '',
        metrics: [],
        notes: '',
      };
      onAdd(newExp);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 w-full max-w-lg">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-slate-100">New Experiment</h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200">
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-slate-300 mb-1">Client</label>
            <input
              type="text"
              className="input-field"
              value={form.client}
              onChange={(e) => setForm((f) => ({ ...f, client: e.target.value }))}
              placeholder="Client name"
              required
            />
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-1">Engine</label>
            <select
              className="input-field"
              value={form.engine}
              onChange={(e) => setForm((f) => ({ ...f, engine: e.target.value }))}
              required
            >
              <option value="">Select engine</option>
              <option value="SEO Engine">SEO Engine</option>
              <option value="Content Engine">Content Engine</option>
              <option value="PPC Engine">PPC Engine</option>
              <option value="Social Media Engine">Social Media Engine</option>
              <option value="Email Engine">Email Engine</option>
              <option value="Analytics Engine">Analytics Engine</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-1">Hypothesis</label>
            <textarea
              className="input-field min-h-[80px]"
              value={form.hypothesis}
              onChange={(e) => setForm((f) => ({ ...f, hypothesis: e.target.value }))}
              placeholder="Describe the hypothesis..."
              required
            />
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <button type="button" onClick={onClose} className="btn-secondary">Cancel</button>
            <button type="submit" disabled={saving} className="btn-primary">
              {saving ? 'Creating...' : 'Create Experiment'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

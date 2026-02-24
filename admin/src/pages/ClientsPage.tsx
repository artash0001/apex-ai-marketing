import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, X } from 'lucide-react';
import DataTable, { type Column } from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';
import api from '../lib/api';

interface Client {
  id: string;
  name: string;
  company: string;
  email: string;
  phone: string;
  status: string;
  market: string;
  language: string;
  mrr: number;
  engines_count: number;
  [key: string]: unknown;
}

const STATUS_FILTERS = ['All', 'Lead', 'Audit Requested', 'Active', 'Paused'];
const MARKET_FILTERS = ['All', 'Dubai', 'UK', 'Global', 'Russian Dubai'];

const mockClients: Client[] = [
  { id: '1', name: 'Ahmed Al-Rashid', company: 'Luxe Properties Dubai', email: 'ahmed@luxeprops.ae', phone: '+971501234567', status: 'active', market: 'Dubai', language: 'en', mrr: 5500, engines_count: 4 },
  { id: '2', name: 'Sarah Chen', company: 'TechFlow Solutions', email: 'sarah@techflow.co', phone: '+447891234567', status: 'active', market: 'UK', language: 'en', mrr: 4200, engines_count: 3 },
  { id: '3', name: 'Dmitry Volkov', company: 'VolgaTech LLC', email: 'dmitry@volgatech.ru', phone: '+971509876543', status: 'lead', market: 'Russian Dubai', language: 'ru', mrr: 0, engines_count: 0 },
  { id: '4', name: 'Emma Williams', company: 'Digital Nomad Co', email: 'emma@digitalnomad.co', phone: '+442071234567', status: 'audit_requested', market: 'UK', language: 'en', mrr: 0, engines_count: 0 },
  { id: '5', name: 'Fatima Hassan', company: 'GoldenGate Realty', email: 'fatima@goldengate.ae', phone: '+971521234567', status: 'active', market: 'Dubai', language: 'ar', mrr: 7800, engines_count: 5 },
  { id: '6', name: 'James Miller', company: 'CloudPeak SaaS', email: 'james@cloudpeak.io', phone: '+442079876543', status: 'active', market: 'Global', language: 'en', mrr: 6100, engines_count: 4 },
  { id: '7', name: 'Olga Petrova', company: 'Stellar Consulting', email: 'olga@stellar.ae', phone: '+971505556666', status: 'paused', market: 'Russian Dubai', language: 'ru', mrr: 3200, engines_count: 2 },
  { id: '8', name: 'Liam Thompson', company: 'BrightPath Education', email: 'liam@brightpath.co.uk', phone: '+442073334444', status: 'lead', market: 'UK', language: 'en', mrr: 0, engines_count: 0 },
  { id: '9', name: 'Rashid Mansoor', company: 'Desert Eagle Logistics', email: 'rashid@deserteagle.ae', phone: '+971507778888', status: 'active', market: 'Dubai', language: 'en', mrr: 9200, engines_count: 6 },
  { id: '10', name: 'Julia Novak', company: 'EuroTrade Global', email: 'julia@eurotrade.eu', phone: '+442081112222', status: 'audit_requested', market: 'Global', language: 'en', mrr: 0, engines_count: 0 },
];

export default function ClientsPage() {
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('All');
  const [marketFilter, setMarketFilter] = useState('All');
  const [showAddModal, setShowAddModal] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchClients = async () => {
      try {
        const res = await api.get('/clients');
        setClients(res.data);
      } catch {
        setClients(mockClients);
      } finally {
        setLoading(false);
      }
    };
    fetchClients();
  }, []);

  const filtered = clients.filter((c) => {
    const statusMatch =
      statusFilter === 'All' ||
      c.status.toLowerCase().replace(/_/g, ' ') === statusFilter.toLowerCase();
    const marketMatch = marketFilter === 'All' || c.market === marketFilter;
    return statusMatch && marketMatch;
  });

  const columns: Column<Client>[] = [
    { key: 'name', label: 'Name', sortable: true },
    { key: 'company', label: 'Company', sortable: true },
    {
      key: 'status',
      label: 'Status',
      sortable: true,
      render: (row) => <StatusBadge status={row.status} />,
    },
    { key: 'market', label: 'Market', sortable: true },
    { key: 'language', label: 'Language', sortable: true },
    {
      key: 'mrr',
      label: 'MRR',
      sortable: true,
      render: (row) => (
        <span className="font-medium">${row.mrr.toLocaleString()}</span>
      ),
    },
    {
      key: 'engines_count',
      label: 'Engines',
      sortable: true,
      render: (row) => (
        <span className="text-slate-400">{row.engines_count}</span>
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
        <h2 className="text-2xl font-bold text-slate-100">Clients</h2>
        <button
          onClick={() => setShowAddModal(true)}
          className="btn-primary flex items-center gap-2"
        >
          <Plus size={16} />
          Add Client
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
      </div>

      {/* Table */}
      <div className="card p-0 overflow-hidden">
        <DataTable
          columns={columns}
          data={filtered}
          keyExtractor={(row) => row.id}
          onRowClick={(row) => navigate(`/clients/${row.id}`)}
          pageSize={10}
          emptyMessage="No clients match the current filters."
        />
      </div>

      {/* Add Client Modal */}
      {showAddModal && (
        <AddClientModal
          onClose={() => setShowAddModal(false)}
          onAdd={(client) => {
            setClients((prev) => [...prev, client]);
            setShowAddModal(false);
          }}
        />
      )}
    </div>
  );
}

function AddClientModal({
  onClose,
  onAdd,
}: {
  onClose: () => void;
  onAdd: (client: Client) => void;
}) {
  const [form, setForm] = useState({
    name: '',
    company: '',
    email: '',
    phone: '',
    market: 'Dubai',
    language: 'en',
  });
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);

    try {
      const res = await api.post('/clients', form);
      onAdd(res.data);
    } catch {
      // Fallback: create client locally
      const newClient: Client = {
        ...form,
        id: Date.now().toString(),
        status: 'lead',
        mrr: 0,
        engines_count: 0,
      };
      onAdd(newClient);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 w-full max-w-lg">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-slate-100">
            Add New Client
          </h3>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-200"
          >
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-slate-300 mb-1">Name</label>
              <input
                type="text"
                className="input-field"
                value={form.name}
                onChange={(e) =>
                  setForm((f) => ({ ...f, name: e.target.value }))
                }
                required
              />
            </div>
            <div>
              <label className="block text-sm text-slate-300 mb-1">
                Company
              </label>
              <input
                type="text"
                className="input-field"
                value={form.company}
                onChange={(e) =>
                  setForm((f) => ({ ...f, company: e.target.value }))
                }
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-slate-300 mb-1">
                Email
              </label>
              <input
                type="email"
                className="input-field"
                value={form.email}
                onChange={(e) =>
                  setForm((f) => ({ ...f, email: e.target.value }))
                }
                required
              />
            </div>
            <div>
              <label className="block text-sm text-slate-300 mb-1">
                Phone
              </label>
              <input
                type="tel"
                className="input-field"
                value={form.phone}
                onChange={(e) =>
                  setForm((f) => ({ ...f, phone: e.target.value }))
                }
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-slate-300 mb-1">
                Market
              </label>
              <select
                className="input-field"
                value={form.market}
                onChange={(e) =>
                  setForm((f) => ({ ...f, market: e.target.value }))
                }
              >
                <option value="Dubai">Dubai</option>
                <option value="UK">UK</option>
                <option value="Global">Global</option>
                <option value="Russian Dubai">Russian Dubai</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-slate-300 mb-1">
                Language
              </label>
              <select
                className="input-field"
                value={form.language}
                onChange={(e) =>
                  setForm((f) => ({ ...f, language: e.target.value }))
                }
              >
                <option value="en">English</option>
                <option value="ar">Arabic</option>
                <option value="ru">Russian</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <button type="button" onClick={onClose} className="btn-secondary">
              Cancel
            </button>
            <button type="submit" disabled={saving} className="btn-primary">
              {saving ? 'Saving...' : 'Add Client'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

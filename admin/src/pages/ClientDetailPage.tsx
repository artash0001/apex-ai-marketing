import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Edit2,
  Save,
  X,
  FileSearch,
  FileText,
  BarChart3,
} from 'lucide-react';
import StatusBadge from '../components/StatusBadge';
import api from '../lib/api';

interface ClientDetail {
  id: string;
  name: string;
  company: string;
  email: string;
  phone: string;
  market: string;
  language: string;
  status: string;
  mrr: number;
  engines: {
    id: string;
    name: string;
    status: string;
    monthly_value: number;
  }[];
  deliverables: {
    id: string;
    title: string;
    type: string;
    status: string;
    due_date: string;
  }[];
}

const mockClient: ClientDetail = {
  id: '1',
  name: 'Ahmed Al-Rashid',
  company: 'Luxe Properties Dubai',
  email: 'ahmed@luxeprops.ae',
  phone: '+971501234567',
  market: 'Dubai',
  language: 'en',
  status: 'active',
  mrr: 5500,
  engines: [
    { id: 'e1', name: 'SEO Engine', status: 'active', monthly_value: 1500 },
    { id: 'e2', name: 'Content Engine', status: 'active', monthly_value: 1200 },
    { id: 'e3', name: 'PPC Engine', status: 'optimizing', monthly_value: 1800 },
    { id: 'e4', name: 'Social Media Engine', status: 'setup', monthly_value: 1000 },
  ],
  deliverables: [
    { id: 'd1', title: 'Monthly SEO Report', type: 'report', status: 'delivered', due_date: '2026-02-20' },
    { id: 'd2', title: 'Content Calendar - March', type: 'content', status: 'pending', due_date: '2026-02-28' },
    { id: 'd3', title: 'PPC Campaign Audit', type: 'audit', status: 'draft', due_date: '2026-03-05' },
    { id: 'd4', title: 'Social Media Strategy', type: 'strategy', status: 'pending', due_date: '2026-03-10' },
  ],
};

export default function ClientDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [client, setClient] = useState<ClientDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [editForm, setEditForm] = useState<Partial<ClientDetail>>({});
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  useEffect(() => {
    const fetchClient = async () => {
      try {
        const res = await api.get(`/clients/${id}`);
        setClient(res.data);
      } catch {
        setClient({ ...mockClient, id: id || '1' });
      } finally {
        setLoading(false);
      }
    };
    fetchClient();
  }, [id]);

  const handleEdit = () => {
    if (client) {
      setEditForm({
        name: client.name,
        company: client.company,
        email: client.email,
        phone: client.phone,
        market: client.market,
        language: client.language,
        status: client.status,
      });
      setEditing(true);
    }
  };

  const handleSave = async () => {
    try {
      await api.put(`/clients/${id}`, editForm);
    } catch {
      // Update locally
    }
    setClient((c) => (c ? { ...c, ...editForm } : c));
    setEditing(false);
  };

  const handleAction = async (action: string) => {
    setActionLoading(action);
    try {
      await api.post(`/clients/${id}/actions`, { action });
    } catch {
      // Silently handle
    } finally {
      setTimeout(() => setActionLoading(null), 1000);
    }
  };

  if (loading || !client) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-blue-500/30 border-t-blue-500 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => navigate('/clients')}
          className="text-slate-400 hover:text-slate-200 transition-colors"
        >
          <ArrowLeft size={20} />
        </button>
        <div className="flex-1">
          <h2 className="text-2xl font-bold text-slate-100">{client.name}</h2>
          <p className="text-slate-400">{client.company}</p>
        </div>
        {!editing ? (
          <button onClick={handleEdit} className="btn-secondary flex items-center gap-2">
            <Edit2 size={16} />
            Edit
          </button>
        ) : (
          <div className="flex gap-2">
            <button onClick={() => setEditing(false)} className="btn-secondary flex items-center gap-2">
              <X size={16} />
              Cancel
            </button>
            <button onClick={handleSave} className="btn-primary flex items-center gap-2">
              <Save size={16} />
              Save
            </button>
          </div>
        )}
      </div>

      {/* Client Info Card */}
      <div className="card">
        <h3 className="text-lg font-semibold text-slate-200 mb-4">
          Client Information
        </h3>
        {editing ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm text-slate-400 mb-1">Name</label>
              <input
                className="input-field"
                value={editForm.name || ''}
                onChange={(e) => setEditForm((f) => ({ ...f, name: e.target.value }))}
              />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-1">Company</label>
              <input
                className="input-field"
                value={editForm.company || ''}
                onChange={(e) => setEditForm((f) => ({ ...f, company: e.target.value }))}
              />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-1">Email</label>
              <input
                className="input-field"
                type="email"
                value={editForm.email || ''}
                onChange={(e) => setEditForm((f) => ({ ...f, email: e.target.value }))}
              />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-1">Phone</label>
              <input
                className="input-field"
                value={editForm.phone || ''}
                onChange={(e) => setEditForm((f) => ({ ...f, phone: e.target.value }))}
              />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-1">Market</label>
              <select
                className="input-field"
                value={editForm.market || ''}
                onChange={(e) => setEditForm((f) => ({ ...f, market: e.target.value }))}
              >
                <option value="Dubai">Dubai</option>
                <option value="UK">UK</option>
                <option value="Global">Global</option>
                <option value="Russian Dubai">Russian Dubai</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-1">Language</label>
              <select
                className="input-field"
                value={editForm.language || ''}
                onChange={(e) => setEditForm((f) => ({ ...f, language: e.target.value }))}
              >
                <option value="en">English</option>
                <option value="ar">Arabic</option>
                <option value="ru">Russian</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-1">Status</label>
              <select
                className="input-field"
                value={editForm.status || ''}
                onChange={(e) => setEditForm((f) => ({ ...f, status: e.target.value }))}
              >
                <option value="lead">Lead</option>
                <option value="audit_requested">Audit Requested</option>
                <option value="audit_complete">Audit Complete</option>
                <option value="proposal_sent">Proposal Sent</option>
                <option value="active">Active</option>
                <option value="paused">Paused</option>
                <option value="churned">Churned</option>
              </select>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <InfoField label="Email" value={client.email} />
            <InfoField label="Phone" value={client.phone} />
            <InfoField label="Market" value={client.market} />
            <InfoField label="Language" value={client.language.toUpperCase()} />
            <div>
              <p className="text-sm text-slate-400 mb-1">Status</p>
              <StatusBadge status={client.status} />
            </div>
            <InfoField label="MRR" value={`$${client.mrr.toLocaleString()}`} />
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-slate-200 mb-4">
          Quick Actions
        </h3>
        <div className="flex flex-wrap gap-3">
          <button
            onClick={() => handleAction('trigger_audit')}
            disabled={actionLoading === 'trigger_audit'}
            className="btn-secondary flex items-center gap-2"
          >
            <FileSearch size={16} />
            {actionLoading === 'trigger_audit' ? 'Processing...' : 'Trigger Audit'}
          </button>
          <button
            onClick={() => handleAction('create_proposal')}
            disabled={actionLoading === 'create_proposal'}
            className="btn-secondary flex items-center gap-2"
          >
            <FileText size={16} />
            {actionLoading === 'create_proposal' ? 'Processing...' : 'Create Proposal'}
          </button>
          <button
            onClick={() => handleAction('generate_report')}
            disabled={actionLoading === 'generate_report'}
            className="btn-secondary flex items-center gap-2"
          >
            <BarChart3 size={16} />
            {actionLoading === 'generate_report' ? 'Processing...' : 'Generate Report'}
          </button>
        </div>
      </div>

      {/* Engine Engagements */}
      <div className="card">
        <h3 className="text-lg font-semibold text-slate-200 mb-4">
          Engine Engagements
        </h3>
        {client.engines.length === 0 ? (
          <p className="text-sm text-slate-500">No engines assigned.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-left px-4 py-3 text-slate-400 font-medium">Engine</th>
                  <th className="text-left px-4 py-3 text-slate-400 font-medium">Status</th>
                  <th className="text-left px-4 py-3 text-slate-400 font-medium">Monthly Value</th>
                </tr>
              </thead>
              <tbody>
                {client.engines.map((eng) => (
                  <tr key={eng.id} className="border-b border-slate-700/50">
                    <td className="px-4 py-3 text-slate-300">{eng.name}</td>
                    <td className="px-4 py-3">
                      <StatusBadge status={eng.status} />
                    </td>
                    <td className="px-4 py-3 text-slate-300 font-medium">
                      ${eng.monthly_value.toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Deliverables */}
      <div className="card">
        <h3 className="text-lg font-semibold text-slate-200 mb-4">
          Deliverables
        </h3>
        {client.deliverables.length === 0 ? (
          <p className="text-sm text-slate-500">No deliverables.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-left px-4 py-3 text-slate-400 font-medium">Title</th>
                  <th className="text-left px-4 py-3 text-slate-400 font-medium">Type</th>
                  <th className="text-left px-4 py-3 text-slate-400 font-medium">Status</th>
                  <th className="text-left px-4 py-3 text-slate-400 font-medium">Due Date</th>
                </tr>
              </thead>
              <tbody>
                {client.deliverables.map((del) => (
                  <tr key={del.id} className="border-b border-slate-700/50">
                    <td className="px-4 py-3 text-slate-300">{del.title}</td>
                    <td className="px-4 py-3 text-slate-400 capitalize">{del.type}</td>
                    <td className="px-4 py-3">
                      <StatusBadge status={del.status} />
                    </td>
                    <td className="px-4 py-3 text-slate-400">{del.due_date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

function InfoField({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-sm text-slate-400 mb-1">{label}</p>
      <p className="text-slate-200">{value}</p>
    </div>
  );
}

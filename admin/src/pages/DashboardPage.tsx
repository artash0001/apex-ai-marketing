import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Users,
  DollarSign,
  Cog,
  ClipboardList,
  Cpu,
  Mail,
  FileCheck,
  Send,
  FileText,
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import StatsCard from '../components/StatsCard';
import api from '../lib/api';

interface DashboardData {
  stats: {
    active_clients: number;
    mrr_total: number;
    active_engines: number;
    pending_deliverables: number;
    ai_costs_month: number;
    outreach_sent: number;
  };
  pipeline: {
    stage: string;
    count: number;
  }[];
  recent_activity: {
    id: string;
    type: string;
    message: string;
    timestamp: string;
  }[];
}

const defaultData: DashboardData = {
  stats: {
    active_clients: 0,
    mrr_total: 0,
    active_engines: 0,
    pending_deliverables: 0,
    ai_costs_month: 0,
    outreach_sent: 0,
  },
  pipeline: [
    { stage: 'Leads', count: 0 },
    { stage: 'Audits', count: 0 },
    { stage: 'Proposals', count: 0 },
    { stage: 'Won', count: 0 },
  ],
  recent_activity: [],
};

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData>(defaultData);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await api.get('/reports/dashboard');
        setData(response.data);
      } catch {
        // Use default/mock data if API not available
        setData({
          stats: {
            active_clients: 12,
            mrr_total: 47500,
            active_engines: 28,
            pending_deliverables: 7,
            ai_costs_month: 1240,
            outreach_sent: 156,
          },
          pipeline: [
            { stage: 'Leads', count: 45 },
            { stage: 'Audits', count: 12 },
            { stage: 'Proposals', count: 8 },
            { stage: 'Won', count: 5 },
          ],
          recent_activity: [
            {
              id: '1',
              type: 'client',
              message: 'New audit requested by TechFlow LLC',
              timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
            },
            {
              id: '2',
              type: 'engine',
              message: 'SEO Engine activated for Luxe Properties',
              timestamp: new Date(Date.now() - 1000 * 60 * 90).toISOString(),
            },
            {
              id: '3',
              type: 'outreach',
              message: 'Outreach batch completed: 25 emails sent',
              timestamp: new Date(Date.now() - 1000 * 60 * 150).toISOString(),
            },
            {
              id: '4',
              type: 'report',
              message: 'Weekly report generated for Digital Nomad Co',
              timestamp: new Date(Date.now() - 1000 * 60 * 240).toISOString(),
            },
            {
              id: '5',
              type: 'experiment',
              message: 'Experiment #42 completed: headline variant won',
              timestamp: new Date(Date.now() - 1000 * 60 * 360).toISOString(),
            },
          ],
        });
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  const formatTime = (ts: string) => {
    const diff = Date.now() - new Date(ts).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 60) return `${mins}m ago`;
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return `${hrs}h ago`;
    return `${Math.floor(hrs / 24)}d ago`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-blue-500/30 border-t-blue-500 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-slate-100">Dashboard</h2>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <StatsCard
          icon={Users}
          label="Active Clients"
          value={data.stats.active_clients}
          iconColor="text-blue-400"
        />
        <StatsCard
          icon={DollarSign}
          label="MRR Total"
          value={`$${data.stats.mrr_total.toLocaleString()}`}
          iconColor="text-green-400"
        />
        <StatsCard
          icon={Cog}
          label="Active Engines"
          value={data.stats.active_engines}
          iconColor="text-purple-400"
        />
        <StatsCard
          icon={ClipboardList}
          label="Pending Deliverables"
          value={data.stats.pending_deliverables}
          iconColor="text-orange-400"
        />
        <StatsCard
          icon={Cpu}
          label="AI Costs (month)"
          value={`$${data.stats.ai_costs_month.toLocaleString()}`}
          iconColor="text-red-400"
        />
        <StatsCard
          icon={Mail}
          label="Outreach Sent"
          value={data.stats.outreach_sent}
          iconColor="text-cyan-400"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Pipeline Chart */}
        <div className="lg:col-span-2 card">
          <h3 className="text-lg font-semibold text-slate-200 mb-4">
            Sales Pipeline
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.pipeline}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis
                  dataKey="stage"
                  tick={{ fill: '#94a3b8', fontSize: 12 }}
                  axisLine={{ stroke: '#475569' }}
                />
                <YAxis
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
                />
                <Bar
                  dataKey="count"
                  fill="#3b82f6"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="card">
          <h3 className="text-lg font-semibold text-slate-200 mb-4">
            Recent Activity
          </h3>
          <div className="space-y-3">
            {data.recent_activity.length === 0 ? (
              <p className="text-sm text-slate-500">No recent activity</p>
            ) : (
              data.recent_activity.map((activity) => (
                <div
                  key={activity.id}
                  className="flex items-start gap-3 p-2 rounded-lg hover:bg-slate-700/30"
                >
                  <div className="w-2 h-2 rounded-full bg-blue-400 mt-1.5 shrink-0" />
                  <div className="min-w-0 flex-1">
                    <p className="text-sm text-slate-300 leading-snug">
                      {activity.message}
                    </p>
                    <p className="text-xs text-slate-500 mt-0.5">
                      {formatTime(activity.timestamp)}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-slate-200 mb-4">
          Quick Actions
        </h3>
        <div className="flex flex-wrap gap-3">
          <button
            onClick={() => navigate('/clients')}
            className="btn-secondary flex items-center gap-2"
          >
            <FileCheck size={16} />
            Review Deliverables
          </button>
          <button
            onClick={() => navigate('/outreach')}
            className="btn-secondary flex items-center gap-2"
          >
            <Send size={16} />
            Check Outreach
          </button>
          <button
            onClick={() => navigate('/reports')}
            className="btn-secondary flex items-center gap-2"
          >
            <FileText size={16} />
            Generate Report
          </button>
        </div>
      </div>
    </div>
  );
}

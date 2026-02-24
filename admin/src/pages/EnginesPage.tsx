import { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import KanbanBoard, { type KanbanCard } from '../components/KanbanBoard';
import StatusBadge from '../components/StatusBadge';
import api from '../lib/api';

const ENGINE_TYPES = [
  'All',
  'SEO Engine',
  'Content Engine',
  'PPC Engine',
  'Social Media Engine',
  'Email Engine',
  'Analytics Engine',
];

const mockEngineCards: KanbanCard[] = [
  { id: 1, clientName: 'Luxe Properties Dubai', engineName: 'SEO Engine', monthlyValue: 1500, kpiStatus: 'on_track', status: 'active' },
  { id: 2, clientName: 'Luxe Properties Dubai', engineName: 'Content Engine', monthlyValue: 1200, kpiStatus: 'on_track', status: 'active' },
  { id: 3, clientName: 'Luxe Properties Dubai', engineName: 'PPC Engine', monthlyValue: 1800, kpiStatus: 'at_risk', status: 'optimizing' },
  { id: 4, clientName: 'Luxe Properties Dubai', engineName: 'Social Media Engine', monthlyValue: 1000, kpiStatus: 'on_track', status: 'setup' },
  { id: 5, clientName: 'TechFlow Solutions', engineName: 'SEO Engine', monthlyValue: 1400, kpiStatus: 'ahead', status: 'active' },
  { id: 6, clientName: 'TechFlow Solutions', engineName: 'Content Engine', monthlyValue: 1100, kpiStatus: 'on_track', status: 'active' },
  { id: 7, clientName: 'TechFlow Solutions', engineName: 'PPC Engine', monthlyValue: 1700, kpiStatus: 'on_track', status: 'optimizing' },
  { id: 8, clientName: 'GoldenGate Realty', engineName: 'SEO Engine', monthlyValue: 1600, kpiStatus: 'ahead', status: 'active' },
  { id: 9, clientName: 'GoldenGate Realty', engineName: 'Content Engine', monthlyValue: 1300, kpiStatus: 'on_track', status: 'active' },
  { id: 10, clientName: 'GoldenGate Realty', engineName: 'Email Engine', monthlyValue: 900, kpiStatus: 'behind', status: 'active' },
  { id: 11, clientName: 'GoldenGate Realty', engineName: 'Analytics Engine', monthlyValue: 1200, kpiStatus: 'on_track', status: 'optimizing' },
  { id: 12, clientName: 'GoldenGate Realty', engineName: 'Social Media Engine', monthlyValue: 1500, kpiStatus: 'on_track', status: 'active' },
  { id: 13, clientName: 'CloudPeak SaaS', engineName: 'SEO Engine', monthlyValue: 1500, kpiStatus: 'on_track', status: 'active' },
  { id: 14, clientName: 'CloudPeak SaaS', engineName: 'PPC Engine', monthlyValue: 2000, kpiStatus: 'at_risk', status: 'active' },
  { id: 15, clientName: 'CloudPeak SaaS', engineName: 'Content Engine', monthlyValue: 1100, kpiStatus: 'on_track', status: 'setup' },
  { id: 16, clientName: 'CloudPeak SaaS', engineName: 'Analytics Engine', monthlyValue: 1500, kpiStatus: 'on_track', status: 'proposed' },
  { id: 17, clientName: 'Desert Eagle Logistics', engineName: 'SEO Engine', monthlyValue: 1800, kpiStatus: 'ahead', status: 'completed' },
  { id: 18, clientName: 'Desert Eagle Logistics', engineName: 'PPC Engine', monthlyValue: 2200, kpiStatus: 'on_track', status: 'active' },
  { id: 19, clientName: 'Digital Nomad Co', engineName: 'SEO Engine', monthlyValue: 1200, kpiStatus: 'on_track', status: 'proposed' },
  { id: 20, clientName: 'Digital Nomad Co', engineName: 'Content Engine', monthlyValue: 900, kpiStatus: 'on_track', status: 'proposed' },
];

interface EngineDetail {
  id: string | number;
  clientName: string;
  engineName: string;
  status: string;
  monthlyValue: number;
  kpiStatus: string;
  startDate: string;
  kpis: { label: string; current: string; target: string }[];
}

export default function EnginesPage() {
  const [cards, setCards] = useState<KanbanCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [engineFilter, setEngineFilter] = useState('All');
  const [selectedCard, setSelectedCard] = useState<EngineDetail | null>(null);

  useEffect(() => {
    const fetchEngines = async () => {
      try {
        const res = await api.get('/engines');
        setCards(res.data);
      } catch {
        setCards(mockEngineCards);
      } finally {
        setLoading(false);
      }
    };
    fetchEngines();
  }, []);

  const filtered =
    engineFilter === 'All'
      ? cards
      : cards.filter((c) => c.engineName === engineFilter);

  const handleCardClick = (card: KanbanCard) => {
    setSelectedCard({
      id: card.id,
      clientName: card.clientName,
      engineName: card.engineName,
      status: card.status,
      monthlyValue: card.monthlyValue,
      kpiStatus: card.kpiStatus,
      startDate: '2025-11-15',
      kpis: [
        { label: 'Organic Traffic', current: '12,450', target: '15,000' },
        { label: 'Conversion Rate', current: '3.2%', target: '4.0%' },
        { label: 'Keyword Rankings', current: '45 top-10', target: '60 top-10' },
      ],
    });
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
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-100">Engine Pipeline</h2>
      </div>

      {/* Engine Type Filter */}
      <div>
        <label className="block text-sm text-slate-400 mb-2">
          Engine Type
        </label>
        <select
          className="input-field max-w-xs"
          value={engineFilter}
          onChange={(e) => setEngineFilter(e.target.value)}
        >
          {ENGINE_TYPES.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
      </div>

      {/* Kanban Board */}
      <div className="card p-4 overflow-x-auto">
        <KanbanBoard cards={filtered} onCardClick={handleCardClick} />
      </div>

      {/* Side Panel */}
      {selectedCard && (
        <div className="fixed inset-0 z-50 flex justify-end bg-black/40">
          <div
            className="absolute inset-0"
            onClick={() => setSelectedCard(null)}
          />
          <div className="relative w-full max-w-md bg-slate-800 border-l border-slate-700 h-full overflow-y-auto p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-slate-100">
                Engine Details
              </h3>
              <button
                onClick={() => setSelectedCard(null)}
                className="text-slate-400 hover:text-slate-200"
              >
                <X size={20} />
              </button>
            </div>

            <div className="space-y-6">
              <div>
                <p className="text-sm text-slate-400">Client</p>
                <p className="text-slate-200 font-medium">
                  {selectedCard.clientName}
                </p>
              </div>

              <div>
                <p className="text-sm text-slate-400">Engine</p>
                <p className="text-slate-200 font-medium">
                  {selectedCard.engineName}
                </p>
              </div>

              <div>
                <p className="text-sm text-slate-400 mb-1">Status</p>
                <StatusBadge status={selectedCard.status} />
              </div>

              <div>
                <p className="text-sm text-slate-400">Monthly Value</p>
                <p className="text-xl font-bold text-slate-100">
                  ${selectedCard.monthlyValue.toLocaleString()}/mo
                </p>
              </div>

              <div>
                <p className="text-sm text-slate-400">Start Date</p>
                <p className="text-slate-200">{selectedCard.startDate}</p>
              </div>

              <div>
                <p className="text-sm text-slate-400 mb-3">KPIs</p>
                <div className="space-y-3">
                  {selectedCard.kpis.map((kpi, idx) => (
                    <div
                      key={idx}
                      className="bg-slate-700/50 rounded-lg p-3"
                    >
                      <p className="text-sm text-slate-300 mb-1">{kpi.label}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-slate-200 font-medium">
                          {kpi.current}
                        </span>
                        <span className="text-xs text-slate-500">
                          Target: {kpi.target}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

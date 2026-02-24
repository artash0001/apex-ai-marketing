import StatusBadge from './StatusBadge';

export interface KanbanCard {
  id: string | number;
  clientName: string;
  engineName: string;
  monthlyValue: number;
  kpiStatus: 'on_track' | 'at_risk' | 'behind' | 'ahead';
  status: string;
}

interface KanbanBoardProps {
  cards: KanbanCard[];
  onCardClick?: (card: KanbanCard) => void;
}

const COLUMNS = [
  { key: 'proposed', label: 'Proposed', color: 'border-yellow-500' },
  { key: 'setup', label: 'Setup', color: 'border-blue-500' },
  { key: 'active', label: 'Active', color: 'border-green-500' },
  { key: 'optimizing', label: 'Optimizing', color: 'border-purple-500' },
  { key: 'completed', label: 'Completed', color: 'border-slate-500' },
];

const kpiColors: Record<string, string> = {
  on_track: 'bg-green-500',
  ahead: 'bg-blue-500',
  at_risk: 'bg-yellow-500',
  behind: 'bg-red-500',
};

export default function KanbanBoard({ cards, onCardClick }: KanbanBoardProps) {
  return (
    <div className="flex gap-4 overflow-x-auto pb-4">
      {COLUMNS.map((col) => {
        const columnCards = cards.filter(
          (c) => c.status.toLowerCase().replace(/\s+/g, '_') === col.key
        );
        return (
          <div
            key={col.key}
            className="flex-shrink-0 w-72"
          >
            {/* Column header */}
            <div
              className={`flex items-center justify-between mb-3 pb-2 border-b-2 ${col.color}`}
            >
              <h3 className="text-sm font-semibold text-slate-300">
                {col.label}
              </h3>
              <span className="text-xs bg-slate-700 text-slate-400 px-2 py-0.5 rounded-full">
                {columnCards.length}
              </span>
            </div>

            {/* Cards */}
            <div className="space-y-3 min-h-[200px]">
              {columnCards.length === 0 ? (
                <div className="flex items-center justify-center h-24 border border-dashed border-slate-700 rounded-lg">
                  <p className="text-xs text-slate-600">No items</p>
                </div>
              ) : (
                columnCards.map((card) => (
                  <div
                    key={card.id}
                    onClick={() => onCardClick?.(card)}
                    className={`bg-slate-800 border border-slate-700 rounded-lg p-3 hover:border-slate-600 transition-colors ${
                      onCardClick ? 'cursor-pointer' : ''
                    }`}
                  >
                    <p className="text-xs text-slate-500 mb-1">
                      {card.clientName}
                    </p>
                    <p className="text-sm font-medium text-slate-200 mb-2">
                      {card.engineName}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-slate-300">
                        ${card.monthlyValue.toLocaleString()}/mo
                      </span>
                      <div className="flex items-center gap-1.5">
                        <div
                          className={`w-2 h-2 rounded-full ${
                            kpiColors[card.kpiStatus] || 'bg-slate-500'
                          }`}
                        />
                        <span className="text-xs text-slate-500">
                          {card.kpiStatus.replace(/_/g, ' ')}
                        </span>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

const statusColors: Record<string, string> = {
  // Client statuses
  lead: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  audit_requested: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  audit_complete: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  proposal_sent: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  active: 'bg-green-500/20 text-green-400 border-green-500/30',
  paused: 'bg-slate-500/20 text-slate-400 border-slate-500/30',
  churned: 'bg-red-500/20 text-red-400 border-red-500/30',

  // Engine statuses
  proposed: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  setup: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  optimizing: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  completed: 'bg-green-500/20 text-green-400 border-green-500/30',

  // Experiment statuses
  running: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  won: 'bg-green-500/20 text-green-400 border-green-500/30',
  lost: 'bg-red-500/20 text-red-400 border-red-500/30',
  inconclusive: 'bg-slate-500/20 text-slate-400 border-slate-500/30',

  // Outreach statuses
  contacted: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  replied: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  meeting: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  not_interested: 'bg-slate-500/20 text-slate-400 border-slate-500/30',

  // Generic
  pending: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  draft: 'bg-slate-500/20 text-slate-400 border-slate-500/30',
  sent: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  delivered: 'bg-green-500/20 text-green-400 border-green-500/30',
  error: 'bg-red-500/20 text-red-400 border-red-500/30',
};

interface StatusBadgeProps {
  status: string;
  className?: string;
}

export default function StatusBadge({ status, className = '' }: StatusBadgeProps) {
  const colorClass =
    statusColors[status.toLowerCase().replace(/\s+/g, '_')] ||
    'bg-slate-500/20 text-slate-400 border-slate-500/30';

  const displayLabel = status
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${colorClass} ${className}`}
    >
      {displayLabel}
    </span>
  );
}

import { type LucideIcon } from 'lucide-react';

interface StatsCardProps {
  icon: LucideIcon;
  label: string;
  value: string | number;
  trend?: {
    value: string;
    positive: boolean;
  };
  iconColor?: string;
}

export default function StatsCard({
  icon: Icon,
  label,
  value,
  trend,
  iconColor = 'text-blue-400',
}: StatsCardProps) {
  return (
    <div className="card-sm flex items-start gap-4">
      <div
        className={`p-2.5 rounded-lg bg-slate-700/50 ${iconColor}`}
      >
        <Icon size={22} />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm text-slate-400 truncate">{label}</p>
        <p className="text-2xl font-bold text-slate-100 mt-0.5">{value}</p>
        {trend && (
          <p
            className={`text-xs mt-1 ${
              trend.positive ? 'text-green-400' : 'text-red-400'
            }`}
          >
            {trend.positive ? '+' : ''}
            {trend.value}
          </p>
        )}
      </div>
    </div>
  );
}

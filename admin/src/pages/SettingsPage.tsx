import { useState, useEffect } from 'react';
import { Save, Eye, EyeOff } from 'lucide-react';
import api from '../lib/api';

interface ApiKeys {
  anthropic: string;
  resend: string;
  web3forms: string;
  telegram_bot: string;
}

interface AgentConfig {
  name: string;
  model: string;
  temperature: number;
  max_tokens: number;
}

interface NotificationPrefs {
  new_lead: boolean;
  audit_complete: boolean;
  proposal_sent: boolean;
  client_won: boolean;
  engine_alert: boolean;
  experiment_complete: boolean;
  report_generated: boolean;
  outreach_reply: boolean;
}

const defaultApiKeys: ApiKeys = {
  anthropic: 'sk-ant-***************',
  resend: 're_***************',
  web3forms: 'w3f_***************',
  telegram_bot: 'bot_***************',
};

const defaultAgents: AgentConfig[] = [
  { name: 'Content Writer', model: 'claude-sonnet-4-20250514', temperature: 0.7, max_tokens: 4096 },
  { name: 'SEO Analyst', model: 'claude-sonnet-4-20250514', temperature: 0.3, max_tokens: 2048 },
  { name: 'PPC Manager', model: 'claude-sonnet-4-20250514', temperature: 0.4, max_tokens: 2048 },
  { name: 'Outreach Agent', model: 'claude-sonnet-4-20250514', temperature: 0.6, max_tokens: 2048 },
  { name: 'Report Generator', model: 'claude-sonnet-4-20250514', temperature: 0.3, max_tokens: 8192 },
  { name: 'Audit Analyzer', model: 'claude-opus-4-20250514', temperature: 0.2, max_tokens: 4096 },
];

const defaultNotifs: NotificationPrefs = {
  new_lead: true,
  audit_complete: true,
  proposal_sent: true,
  client_won: true,
  engine_alert: true,
  experiment_complete: false,
  report_generated: false,
  outreach_reply: true,
};

export default function SettingsPage() {
  const [apiKeys, setApiKeys] = useState<ApiKeys>(defaultApiKeys);
  const [agents, setAgents] = useState<AgentConfig[]>(defaultAgents);
  const [notifs, setNotifs] = useState<NotificationPrefs>(defaultNotifs);
  const [showKeys, setShowKeys] = useState<Record<string, boolean>>({});
  const [saving, setSaving] = useState<Record<string, boolean>>({});
  const [saved, setSaved] = useState<Record<string, boolean>>({});

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const res = await api.get('/settings');
        if (res.data.api_keys) setApiKeys(res.data.api_keys);
        if (res.data.agents) setAgents(res.data.agents);
        if (res.data.notifications) setNotifs(res.data.notifications);
      } catch {
        // Use defaults
      }
    };
    fetchSettings();
  }, []);

  const handleSaveSection = async (section: string) => {
    setSaving((s) => ({ ...s, [section]: true }));
    setSaved((s) => ({ ...s, [section]: false }));
    try {
      let payload = {};
      if (section === 'api_keys') payload = { api_keys: apiKeys };
      if (section === 'agents') payload = { agents };
      if (section === 'notifications') payload = { notifications: notifs };
      await api.put('/settings', payload);
    } catch {
      // Silently handle
    }
    setTimeout(() => {
      setSaving((s) => ({ ...s, [section]: false }));
      setSaved((s) => ({ ...s, [section]: true }));
      setTimeout(() => setSaved((s) => ({ ...s, [section]: false })), 2000);
    }, 500);
  };

  const toggleKeyVisibility = (key: string) => {
    setShowKeys((s) => ({ ...s, [key]: !s[key] }));
  };

  const notifLabels: Record<keyof NotificationPrefs, string> = {
    new_lead: 'New Lead Received',
    audit_complete: 'Audit Completed',
    proposal_sent: 'Proposal Sent',
    client_won: 'Client Won',
    engine_alert: 'Engine Alert (KPI off-track)',
    experiment_complete: 'Experiment Completed',
    report_generated: 'Report Generated',
    outreach_reply: 'Outreach Reply Received',
  };

  return (
    <div className="space-y-8 max-w-4xl">
      <h2 className="text-2xl font-bold text-slate-100">Settings</h2>

      {/* API Keys */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-slate-200">API Keys</h3>
          <SaveButton
            onClick={() => handleSaveSection('api_keys')}
            saving={saving.api_keys}
            saved={saved.api_keys}
          />
        </div>
        <div className="space-y-4">
          {(
            [
              { key: 'anthropic', label: 'Anthropic API Key' },
              { key: 'resend', label: 'Resend API Key' },
              { key: 'web3forms', label: 'Web3Forms API Key' },
              { key: 'telegram_bot', label: 'Telegram Bot Token' },
            ] as const
          ).map(({ key, label }) => (
            <div key={key}>
              <label className="block text-sm text-slate-400 mb-1.5">
                {label}
              </label>
              <div className="relative">
                <input
                  type={showKeys[key] ? 'text' : 'password'}
                  className="input-field pr-10"
                  value={apiKeys[key]}
                  onChange={(e) =>
                    setApiKeys((k) => ({ ...k, [key]: e.target.value }))
                  }
                />
                <button
                  type="button"
                  onClick={() => toggleKeyVisibility(key)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300"
                >
                  {showKeys[key] ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Agent Configuration */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-slate-200">
            Agent Configuration
          </h3>
          <SaveButton
            onClick={() => handleSaveSection('agents')}
            saving={saving.agents}
            saved={saved.agents}
          />
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-left px-4 py-3 text-slate-400 font-medium">
                  Agent Name
                </th>
                <th className="text-left px-4 py-3 text-slate-400 font-medium">
                  Model
                </th>
                <th className="text-left px-4 py-3 text-slate-400 font-medium">
                  Temperature
                </th>
                <th className="text-left px-4 py-3 text-slate-400 font-medium">
                  Max Tokens
                </th>
              </tr>
            </thead>
            <tbody>
              {agents.map((agent, idx) => (
                <tr key={idx} className="border-b border-slate-700/50">
                  <td className="px-4 py-3 text-slate-300 font-medium">
                    {agent.name}
                  </td>
                  <td className="px-4 py-3">
                    <select
                      className="input-field py-1.5 text-sm"
                      value={agent.model}
                      onChange={(e) =>
                        setAgents((a) =>
                          a.map((ag, i) =>
                            i === idx ? { ...ag, model: e.target.value } : ag
                          )
                        )
                      }
                    >
                      <option value="claude-sonnet-4-20250514">Claude Sonnet 4</option>
                      <option value="claude-opus-4-20250514">Claude Opus 4</option>
                      <option value="claude-haiku-35-20241022">Claude Haiku 3.5</option>
                    </select>
                  </td>
                  <td className="px-4 py-3">
                    <input
                      type="number"
                      min="0"
                      max="1"
                      step="0.1"
                      className="input-field py-1.5 text-sm w-24"
                      value={agent.temperature}
                      onChange={(e) =>
                        setAgents((a) =>
                          a.map((ag, i) =>
                            i === idx
                              ? { ...ag, temperature: parseFloat(e.target.value) || 0 }
                              : ag
                          )
                        )
                      }
                    />
                  </td>
                  <td className="px-4 py-3">
                    <input
                      type="number"
                      min="256"
                      max="32768"
                      step="256"
                      className="input-field py-1.5 text-sm w-28"
                      value={agent.max_tokens}
                      onChange={(e) =>
                        setAgents((a) =>
                          a.map((ag, i) =>
                            i === idx
                              ? { ...ag, max_tokens: parseInt(e.target.value) || 2048 }
                              : ag
                          )
                        )
                      }
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Notification Preferences */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-slate-200">
            Telegram Notifications
          </h3>
          <SaveButton
            onClick={() => handleSaveSection('notifications')}
            saving={saving.notifications}
            saved={saved.notifications}
          />
        </div>
        <div className="space-y-3">
          {(Object.keys(notifLabels) as Array<keyof NotificationPrefs>).map(
            (key) => (
              <label
                key={key}
                className="flex items-center justify-between py-2 px-3 rounded-lg hover:bg-slate-700/30 cursor-pointer"
              >
                <span className="text-sm text-slate-300">
                  {notifLabels[key]}
                </span>
                <div className="relative">
                  <input
                    type="checkbox"
                    checked={notifs[key]}
                    onChange={() =>
                      setNotifs((n) => ({ ...n, [key]: !n[key] }))
                    }
                    className="sr-only"
                  />
                  <div
                    className={`w-10 h-5 rounded-full transition-colors ${
                      notifs[key] ? 'bg-blue-600' : 'bg-slate-600'
                    }`}
                  >
                    <div
                      className={`w-4 h-4 bg-white rounded-full transition-transform transform mt-0.5 ${
                        notifs[key] ? 'translate-x-5' : 'translate-x-0.5'
                      }`}
                    />
                  </div>
                </div>
              </label>
            )
          )}
        </div>
      </div>
    </div>
  );
}

function SaveButton({
  onClick,
  saving,
  saved,
}: {
  onClick: () => void;
  saving?: boolean;
  saved?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      disabled={saving}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
        saved
          ? 'bg-green-600 text-white'
          : 'bg-blue-600 hover:bg-blue-700 text-white disabled:opacity-50'
      }`}
    >
      {saving ? (
        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
      ) : (
        <Save size={14} />
      )}
      {saved ? 'Saved' : saving ? 'Saving...' : 'Save'}
    </button>
  );
}

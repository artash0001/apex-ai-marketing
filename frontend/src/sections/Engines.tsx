import { useState } from 'react';
import {
  Search,
  Layers,
  MapPin,
  TrendingUp,
  Send,
  DollarSign,
  Repeat,
  Settings,
  Clock,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

interface Engine {
  id: string;
  icon: React.ElementType;
  name: string;
  outcome: string;
  deliverables: string[];
  timeline: string;
  tag?: string;
}

const engines: Engine[] = [
  {
    id: 'audit',
    icon: Search,
    name: 'Growth Infrastructure Audit',
    outcome: 'Know exactly where your revenue leaks are — in one week.',
    deliverables: [
      'Tracking & attribution map',
      'Funnel teardown with benchmarks',
      '90-day build plan',
      'KPI targets',
    ],
    timeline: '5-7 business days',
    tag: 'START HERE',
  },
  {
    id: 'foundation',
    icon: Layers,
    name: 'Revenue Stack Foundation',
    outcome: 'Capture every lead. Track every dollar. Follow up automatically.',
    deliverables: [
      'CRM pipeline setup',
      'Lead capture standardization',
      'Attribution model',
      'Automation flows',
      'Reporting dashboard',
    ],
    timeline: '2-4 weeks',
  },
  {
    id: 'local',
    icon: MapPin,
    name: 'Local Visibility Engine',
    outcome: 'Dominate local search. Nearby customers find you first.',
    deliverables: [
      'Google Business Profile optimization',
      'Citation strategy',
      'Review automation',
      'Local landing pages',
      'Monthly ranking report',
    ],
    timeline: '1-2 weeks setup + ongoing',
    tag: 'SUBSCRIPTION',
  },
  {
    id: 'inbound',
    icon: TrendingUp,
    name: 'Inbound Demand Engine',
    outcome: 'Turn search traffic into qualified sales conversations.',
    deliverables: [
      'Topic map & content briefs',
      'Publishing system',
      'Technical SEO backlog',
      'AI-search readiness (GEO/AEO)',
      'Monthly performance report',
    ],
    timeline: '2-3 weeks setup + ongoing',
  },
  {
    id: 'outbound',
    icon: Send,
    name: 'Outbound Engine',
    outcome: 'Book meetings with your ideal buyers systematically.',
    deliverables: [
      'ICP list & enrichment',
      'Prospecting sequences (email + LinkedIn)',
      'Booking workflow',
      'KPI dashboard',
    ],
    timeline: '1-2 weeks setup, ramp in 4-6 weeks',
  },
  {
    id: 'paid',
    icon: DollarSign,
    name: 'Paid Acquisition Engine',
    outcome: 'Make every ad dollar accountable with real tracking.',
    deliverables: [
      'Campaign structure & account setup',
      'Creative briefs & ad copy',
      'Landing page testing',
      'Weekly optimization',
      'ROAS reporting',
    ],
    timeline: '1-2 weeks launch + ongoing',
  },
  {
    id: 'lifecycle',
    icon: Repeat,
    name: 'Lifecycle & Retention Engine',
    outcome: 'Customers come back. And bring friends.',
    deliverables: [
      'Welcome + nurture sequences',
      'Winback flows',
      'Review request automation',
      'Referral loops',
      'Segmentation model',
    ],
    timeline: '2-3 weeks build + ongoing',
  },
  {
    id: 'retainer',
    icon: Settings,
    name: 'Growth Ops Retainer',
    outcome: 'We run the system. You focus on closing.',
    deliverables: [
      'Weekly experiment log',
      'Monthly executive report',
      'Backlog prioritization',
      'Quarterly strategy review',
    ],
    timeline: 'After engine deployment',
    tag: 'ONGOING',
  },
];

export function Engines() {
  const [selectedEngine, setSelectedEngine] = useState<Engine | null>(null);
  const [expandedCards, setExpandedCards] = useState<Set<string>>(new Set());

  const toggleExpand = (id: string) => {
    const newExpanded = new Set(expandedCards);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedCards(newExpanded);
  };

  return (
    <section id="engines" className="py-20 lg:py-28 bg-gray-50">
      <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
        <div className="max-w-6xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-navy mb-4">
              Choose the engine you need.
              <br />
              <span className="text-blue">Or we run the full stack.</span>
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Start with the one that fixes your biggest leak — then we connect 
              it to the full stack.
            </p>
          </div>

          {/* Engines grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {engines.map((engine) => (
              <div
                key={engine.id}
                className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
              >
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-blue/10 rounded-lg flex items-center justify-center">
                      <engine.icon className="w-6 h-6 text-blue" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-navy">
                        {engine.name}
                      </h3>
                      {engine.tag && (
                        <span className="inline-block px-2 py-0.5 bg-gold/20 text-gold text-xs font-semibold rounded">
                          {engine.tag}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Outcome */}
                <p className="text-gray-700 mb-4">{engine.outcome}</p>

                {/* Timeline */}
                <div className="flex items-center gap-2 text-sm text-gray-500 mb-4">
                  <Clock className="w-4 h-4" />
                  <span>{engine.timeline}</span>
                </div>

                {/* Expandable deliverables */}
                <div className="border-t border-gray-100 pt-4">
                  <button
                    onClick={() => toggleExpand(engine.id)}
                    className="flex items-center gap-2 text-blue font-medium hover:text-blue/80 transition-colors"
                  >
                    {expandedCards.has(engine.id) ? (
                      <>
                        <ChevronUp className="w-4 h-4" />
                        Hide deliverables
                      </>
                    ) : (
                      <>
                        <ChevronDown className="w-4 h-4" />
                        View deliverables
                      </>
                    )}
                  </button>

                  {expandedCards.has(engine.id) && (
                    <ul className="mt-4 space-y-2">
                      {engine.deliverables.map((item, idx) => (
                        <li
                          key={idx}
                          className="flex items-start gap-2 text-sm text-gray-600"
                        >
                          <span className="w-1.5 h-1.5 bg-blue rounded-full mt-2 flex-shrink-0" />
                          {item}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>

                {/* Learn more button */}
                <Button
                  variant="ghost"
                  onClick={() => setSelectedEngine(engine)}
                  className="mt-4 text-blue hover:text-blue/80 hover:bg-blue/5"
                >
                  Learn more
                </Button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Modal */}
      <Dialog
        open={selectedEngine !== null}
        onOpenChange={() => setSelectedEngine(null)}
      >
        <DialogContent className="max-w-lg max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-3">
              {selectedEngine && (
                <>
                  <div className="w-10 h-10 bg-blue/10 rounded-lg flex items-center justify-center">
                    <selectedEngine.icon className="w-5 h-5 text-blue" />
                  </div>
                  <span className="text-navy">{selectedEngine.name}</span>
                </>
              )}
            </DialogTitle>
          </DialogHeader>
          {selectedEngine && (
            <div className="space-y-6">
              <div>
                <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
                  Outcome
                </h4>
                <p className="text-gray-700">{selectedEngine.outcome}</p>
              </div>

              <div>
                <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
                  Deliverables
                </h4>
                <ul className="space-y-2">
                  {selectedEngine.deliverables.map((item, idx) => (
                    <li
                      key={idx}
                      className="flex items-start gap-2 text-gray-600"
                    >
                      <span className="w-1.5 h-1.5 bg-blue rounded-full mt-2 flex-shrink-0" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
                  Timeline
                </h4>
                <div className="flex items-center gap-2 text-gray-700">
                  <Clock className="w-4 h-4 text-blue" />
                  {selectedEngine.timeline}
                </div>
              </div>

              <Button
                onClick={() => {
                  setSelectedEngine(null);
                  document.querySelector('#contact')?.scrollIntoView({ behavior: 'smooth' });
                }}
                className="w-full bg-gold hover:bg-gold/90 text-navy font-semibold"
              >
                Request this engine
              </Button>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </section>
  );
}

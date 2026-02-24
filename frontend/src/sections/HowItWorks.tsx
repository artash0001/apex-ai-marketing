import { Search, LayoutTemplate, Rocket, RefreshCw } from 'lucide-react';

const steps = [
  {
    number: '01',
    title: 'Diagnose',
    icon: Search,
    description:
      'We audit your funnel, tracking, and competitive landscape. You get a clear map of where revenue leaks — and what to build first.',
  },
  {
    number: '02',
    title: 'Design',
    icon: LayoutTemplate,
    description:
      'We select the right engines for your business and design the system: workflows, automations, tracking, and success metrics.',
  },
  {
    number: '03',
    title: 'Deploy',
    icon: Rocket,
    description:
      'We build and launch your growth infrastructure — CRM pipelines, content engines, ad systems, automation flows — all connected.',
  },
  {
    number: '04',
    title: 'Iterate',
    icon: RefreshCw,
    description:
      'Weekly experiments, monthly reports, quarterly strategy reviews. The system gets smarter every week.',
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="py-20 lg:py-28 bg-white">
      <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
        <div className="max-w-6xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-navy mb-4">
              From diagnosis to deployed system
              <br />
              <span className="text-blue">in weeks, not months.</span>
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Every engagement follows the same backbone: measure what's broken, 
              design the fix, deploy the engine, then iterate weekly.
            </p>
          </div>

          {/* Steps grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {steps.map((step, index) => (
              <div
                key={step.number}
                className="relative group"
              >
                {/* Connector line (desktop only) */}
                {index < steps.length - 1 && (
                  <div className="hidden lg:block absolute top-12 left-full w-full h-px bg-gradient-to-r from-blue/30 to-transparent" />
                )}

                <div className="relative">
                  {/* Step number */}
                  <span className="absolute -top-2 -left-2 text-6xl font-bold text-blue/10 font-mono">
                    {step.number}
                  </span>

                  {/* Icon */}
                  <div className="relative mb-6">
                    <div className="w-14 h-14 bg-blue/10 rounded-xl flex items-center justify-center group-hover:bg-blue/20 transition-colors">
                      <step.icon className="w-7 h-7 text-blue" />
                    </div>
                  </div>

                  {/* Content */}
                  <h3 className="text-xl font-bold text-navy mb-3">
                    {step.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {step.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

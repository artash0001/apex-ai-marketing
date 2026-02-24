import { Check } from 'lucide-react';

const differentiators = [
  {
    title: 'Systems, not services',
    description:
      'We build assets that compound, not campaigns that expire.',
  },
  {
    title: 'Radical transparency',
    description:
      'You see the same dashboards we do. Experiment logs are shared. Results — good and bad — are documented.',
  },
  {
    title: 'Scope discipline',
    description:
      'Every engagement has defined inclusions, exclusions, and success metrics. No scope creep.',
  },
  {
    title: 'AI that explains itself',
    description:
      'We describe mechanisms and outcomes, not hype. If we can\'t explain how it works, we don\'t ship it.',
  },
];

export function About() {
  return (
    <section id="about" className="py-20 lg:py-28 bg-white">
      <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
        <div className="max-w-6xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-navy mb-4">
              Built by operators who've been
              <br />
              <span className="text-blue">on your side of the table.</span>
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              We started Apex because we saw what wasn't working: agencies selling 
              activity instead of outcomes, dashboards nobody reads, and AI claims 
              with no substance.
            </p>
          </div>

          {/* Two column layout */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16">
            {/* Left column - Our approach */}
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                Our approach
              </h3>
              <p className="text-gray-600 leading-relaxed mb-8">
                Every engagement starts with a diagnosis, not a sales pitch. We build 
                revenue systems — tracking, automation, content engines, ad infrastructure 
                — that clients can audit, measure, and own. If you can't see it working, 
                it doesn't count as delivered.
              </p>

              {/* Languages & Location */}
              <div className="bg-gray-50 rounded-xl p-6">
                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
                    Languages served
                  </h4>
                  <p className="text-navy font-medium">
                    English, Russian, Arabic market understanding
                  </p>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
                    Based in
                  </h4>
                  <p className="text-navy font-medium">
                    Dubai, UAE. Serving clients globally.
                  </p>
                </div>
              </div>
            </div>

            {/* Right column - What makes us different */}
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                What makes us different
              </h3>
              <div className="space-y-4">
                {differentiators.map((item) => (
                  <div
                    key={item.title}
                    className="flex items-start gap-3 p-4 bg-gray-50 rounded-lg"
                  >
                    <div className="w-6 h-6 bg-blue/10 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <Check className="w-4 h-4 text-blue" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-navy mb-1">
                        {item.title}
                      </h4>
                      <p className="text-sm text-gray-600">
                        {item.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

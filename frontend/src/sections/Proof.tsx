import { FileText, Network, BarChart3, ArrowRight } from 'lucide-react';

const proofCards = [
  {
    icon: FileText,
    title: 'Our Methodology',
    description:
      'Step-by-step walkthrough of how we diagnose, design, and deploy growth infrastructure.',
    cta: 'View our process',
    href: '#how-it-works',
  },
  {
    icon: Network,
    title: 'System Architecture Examples',
    description:
      'Before/after architecture diagrams showing how disconnected marketing becomes a connected revenue system.',
    cta: 'See examples',
    href: '#engines',
  },
  {
    icon: BarChart3,
    title: 'Industry Benchmarks',
    description:
      'Our analysis of what\'s working (and what isn\'t) across Dubai, UK, and global digital marketing.',
    cta: 'Read our analysis',
    href: '#contact',
  },
];

export function Proof() {
  const scrollToSection = (href: string) => {
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="proof" className="py-20 lg:py-28 bg-gray-50">
      <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
        <div className="max-w-6xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-navy mb-4">
              Evidence, not testimonials.
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              We publish methodology, system diagrams, and experiment results. 
              No fabricated statistics.
            </p>
          </div>

          {/* Proof cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            {proofCards.map((card) => (
              <div
                key={card.title}
                className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
              >
                {/* Icon */}
                <div className="w-14 h-14 bg-blue/10 rounded-xl flex items-center justify-center mb-6">
                  <card.icon className="w-7 h-7 text-blue" />
                </div>

                {/* Content */}
                <h3 className="text-xl font-bold text-navy mb-3">
                  {card.title}
                </h3>
                <p className="text-gray-600 mb-6 leading-relaxed">
                  {card.description}
                </p>

                {/* CTA */}
                <button
                  onClick={() => scrollToSection(card.href)}
                  className="inline-flex items-center gap-2 text-blue font-medium hover:text-blue/80 transition-colors"
                >
                  {card.cta}
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>

          {/* Disclaimer */}
          <div className="bg-navy/5 rounded-xl p-6 text-center">
            <p className="text-sm text-gray-600">
              <em>
                *As a new agency, we publish our methodology and industry analysis 
                as proof of expertise. Client case studies will be added as engagements 
                are completed — with permission and verified data only.
              </em>
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

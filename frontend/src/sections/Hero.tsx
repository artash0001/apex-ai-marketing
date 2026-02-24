import { ArrowRight, Clock, Settings, Zap } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function Hero() {
  const scrollToSection = (href: string) => {
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section
      id="home"
      className="relative min-h-screen flex items-center bg-gradient-to-br from-navy via-navy to-blue/20"
    >
      {/* Subtle pattern overlay */}
      <div className="absolute inset-0 opacity-5">
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `radial-gradient(circle at 1px 1px, white 1px, transparent 0)`,
            backgroundSize: '40px 40px',
          }}
        />
      </div>

      <div className="relative w-full px-4 sm:px-6 lg:px-8 xl:px-12 pt-24 pb-16">
        <div className="max-w-5xl mx-auto">
          {/* Floating badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full mb-8">
            <Clock className="w-4 h-4 text-gold" />
            <span className="text-sm text-white/90 font-medium">
              Strategy Ready in 48 Hours
            </span>
          </div>

          {/* Main heading */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-bold text-white leading-tight mb-6">
            AI Growth Infrastructure
            <br />
            <span className="text-blue">for predictable pipeline.</span>
          </h1>

          {/* Subhead */}
          <p className="text-lg sm:text-xl text-white/80 max-w-2xl mb-10 leading-relaxed">
            We design and run the revenue systems behind lead capture, qualification, 
            follow-up, and reporting — so growth is engineered, not guessed.
          </p>

          {/* CTA buttons */}
          <div className="flex flex-col sm:flex-row gap-4 mb-16">
            <Button
              size="lg"
              onClick={() => scrollToSection('#contact')}
              className="bg-gold hover:bg-gold/90 text-navy font-semibold px-8 py-6 text-base"
            >
              Request a Growth Infrastructure Audit
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={() => scrollToSection('#engines')}
              className="border-white/30 text-white hover:bg-white/10 px-8 py-6 text-base"
            >
              See how our engines work
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
          </div>

          {/* Capability stats */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 sm:gap-8 pt-8 border-t border-white/10">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-blue/20 rounded-lg">
                <Settings className="w-6 h-6 text-blue" />
              </div>
              <div>
                <p className="text-2xl sm:text-3xl font-bold text-white font-mono">
                  8
                </p>
                <p className="text-white font-semibold">Revenue Engines</p>
                <p className="text-sm text-white/60">Modular growth systems</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="p-3 bg-blue/20 rounded-lg">
                <Clock className="w-6 h-6 text-blue" />
              </div>
              <div>
                <p className="text-2xl sm:text-3xl font-bold text-white font-mono">
                  &lt;48h
                </p>
                <p className="text-white font-semibold">Audit Turnaround</p>
                <p className="text-sm text-white/60">Diagnosis to build plan</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="p-3 bg-blue/20 rounded-lg">
                <Zap className="w-6 h-6 text-blue" />
              </div>
              <div>
                <p className="text-2xl sm:text-3xl font-bold text-white font-mono">
                  24/7
                </p>
                <p className="text-white font-semibold">AI + Human Ops</p>
                <p className="text-sm text-white/60">Systems that don't sleep</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

import { Mail, Phone, MessageCircle } from 'lucide-react';

const quickLinks = [
  { label: 'How It Works', href: '#how-it-works' },
  { label: 'Engines', href: '#engines' },
  { label: 'About', href: '#about' },
  { label: 'Proof', href: '#proof' },
  { label: 'FAQ', href: '#faq' },
  { label: 'Contact / Request Audit', href: '#contact' },
];

export function Footer() {
  const scrollToSection = (href: string) => {
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <footer className="bg-navy text-white py-16">
      <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
            {/* Column 1 - Brand */}
            <div>
              <div className="mb-4">
                <span className="text-2xl font-bold tracking-tight">
                  APEX
                  <span className="inline-block ml-1 w-0 h-0 border-l-[5px] border-l-transparent border-r-[5px] border-r-transparent border-b-[8px] border-b-blue align-middle"></span>
                </span>
                <span className="block text-sm font-medium text-white/70 mt-1">
                  AI Marketing
                </span>
              </div>
              <p className="text-white/70 mb-4">
                AI Growth Infrastructure for predictable pipeline.
              </p>
              <p className="text-sm text-white/50">
                Dubai, UAE | Serving clients globally
              </p>
            </div>

            {/* Column 2 - Quick links */}
            <div>
              <h4 className="font-semibold mb-4">Quick links</h4>
              <nav className="space-y-2">
                {quickLinks.map((link) => (
                  <a
                    key={link.href}
                    href={link.href}
                    onClick={(e) => {
                      e.preventDefault();
                      scrollToSection(link.href);
                    }}
                    className="block text-white/70 hover:text-white transition-colors"
                  >
                    {link.label}
                  </a>
                ))}
              </nav>
            </div>

            {/* Column 3 - Contact */}
            <div>
              <h4 className="font-semibold mb-4">Contact</h4>
              <div className="space-y-3">
                <a
                  href="mailto:artaches@apexaimarketing.pro"
                  className="flex items-center gap-2 text-white/70 hover:text-white transition-colors"
                >
                  <Mail className="w-4 h-4" />
                  artaches@apexaimarketing.pro
                </a>
                <a
                  href="tel:+971507510161"
                  className="flex items-center gap-2 text-white/70 hover:text-white transition-colors"
                >
                  <Phone className="w-4 h-4" />
                  +971 50 751 0161
                </a>
                <a
                  href="https://wa.me/971507510161"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 text-white/70 hover:text-white transition-colors"
                >
                  <MessageCircle className="w-4 h-4" />
                  WhatsApp
                </a>
                <a
                  href="https://t.me/Wowdubai1"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 text-white/70 hover:text-white transition-colors"
                >
                  <MessageCircle className="w-4 h-4" />
                  Telegram @Wowdubai1
                </a>
              </div>
            </div>
          </div>

          {/* Bottom row */}
          <div className="pt-8 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-sm text-white/50">
              © 2026 Apex AI Marketing. All rights reserved.
            </p>
            <div className="flex items-center gap-6">
              <a
                href="#"
                className="text-sm text-white/50 hover:text-white transition-colors"
              >
                Privacy Policy
              </a>
              <a
                href="#"
                className="text-sm text-white/50 hover:text-white transition-colors"
              >
                Terms of Service
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

import { MessageCircle, Send, Mail } from 'lucide-react';

const contactButtons = [
  {
    icon: MessageCircle,
    label: 'WhatsApp',
    href: 'https://wa.me/971507510161',
    bgColor: 'bg-[#25D366]',
    hoverColor: 'hover:bg-[#128C7E]',
  },
  {
    icon: Send,
    label: 'Telegram',
    href: 'https://t.me/Wowdubai1',
    bgColor: 'bg-[#0088CC]',
    hoverColor: 'hover:bg-[#006699]',
  },
  {
    icon: Mail,
    label: 'Email',
    href: 'mailto:artaches@apexaimarketing.pro',
    bgColor: 'bg-navy',
    hoverColor: 'hover:bg-navy/90',
  },
];

export function FloatingContact() {
  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-3">
      {contactButtons.map((button) => (
        <a
          key={button.label}
          href={button.href}
          target={button.href.startsWith('http') ? '_blank' : undefined}
          rel={button.href.startsWith('http') ? 'noopener noreferrer' : undefined}
          className={`w-12 h-12 ${button.bgColor} ${button.hoverColor} rounded-full flex items-center justify-center shadow-lg transition-all hover:scale-110`}
          aria-label={button.label}
          title={button.label}
        >
          <button.icon className="w-5 h-5 text-white" />
        </a>
      ))}
    </div>
  );
}

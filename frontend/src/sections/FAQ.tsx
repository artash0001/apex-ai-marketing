import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';

const faqs = [
  {
    question: 'What is AI Growth Infrastructure?',
    answer:
      "It's the complete system of engines — tracking, automation, content, ads, CRM — that makes your revenue predictable. Instead of buying random marketing tasks, you deploy connected systems that capture leads, qualify them, follow up automatically, and report results weekly.",
  },
  {
    question: 'How is this different from a regular marketing agency?',
    answer:
      "Traditional agencies sell activity — posts published, ads run, reports sent. We build infrastructure — systems you can audit, measure, and own. Every deliverable has defined inputs, outputs, timelines, and success metrics. If it can't be measured, we don't do it.",
  },
  {
    question: 'What does the Growth Infrastructure Audit include?',
    answer:
      'A complete diagnosis of your funnel: tracking and attribution gaps, conversion benchmarks per stage, competitive scan, and a prioritized 90-day build plan. Delivered in 5-7 business days. The audit fee is typically credited toward your first engine build.',
  },
  {
    question: 'Which engine should I start with?',
    answer:
      "Start with the audit — it tells you where the biggest leak is. For local businesses, that's usually the Local Visibility Engine. For B2B companies, it's typically Revenue Stack Foundation or Inbound Demand Engine. We'll recommend based on data, not guessing.",
  },
  {
    question: 'How much does it cost?',
    answer:
      'It depends on the engine, your market, and the complexity of your infrastructure. We publish pricing ranges after the audit because we refuse to quote before we diagnose. The audit itself is a fixed-fee engagement.',
  },
  {
    question: 'Do you work with businesses outside Dubai?',
    answer:
      'Yes. We serve clients in Dubai/UAE, the UK, and globally. We have particular expertise with local service businesses (trades, clinics, salons) and B2B high-ticket services. We also serve the Russian-speaking business community in Dubai.',
  },
  {
    question: 'Do you speak Russian?',
    answer:
      'Yes. We provide full service in English and Russian, with deep understanding of the Russian-speaking business community in Dubai and the UAE.',
  },
  {
    question: 'What if I already have a marketing agency?',
    answer:
      "We can work alongside your existing team. The audit often reveals infrastructure gaps — tracking, attribution, CRM routing — that campaign-focused agencies don't address. We build the systems layer; they can continue running campaigns on top of it.",
  },
  {
    question: 'How quickly will I see results?',
    answer:
      'The audit is delivered in 5-7 days. Engine builds take 1-4 weeks depending on complexity. Paid acquisition and outbound typically show measurable results within 30 days. SEO and content compound over 3-6 months. We set clear timelines and milestones for every engagement.',
  },
  {
    question: 'What do I need to provide?',
    answer:
      'At minimum: analytics access, CRM access, ad platform access (if applicable), and 30 minutes per week for a sync call. We handle the building, but we need your data and your domain expertise about your customers.',
  },
];

export function FAQ() {
  return (
    <section id="faq" className="py-20 lg:py-28 bg-white">
      <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
        <div className="max-w-3xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-navy mb-4">
              Questions we get asked.
            </h2>
          </div>

          {/* Accordion */}
          <Accordion type="single" collapsible className="space-y-4">
            {faqs.map((faq, index) => (
              <AccordionItem
                key={index}
                value={`item-${index}`}
                className="border border-gray-200 rounded-lg px-6 data-[state=open]:border-blue/30"
              >
                <AccordionTrigger className="text-left text-navy font-semibold hover:no-underline py-4">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-gray-600 pb-4 leading-relaxed">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>
    </section>
  );
}

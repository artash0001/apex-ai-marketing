import { useState } from 'react';
import { Check, Clock, Calendar, FileText, Send, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

const steps = [
  {
    icon: FileText,
    text: 'You submit the form (takes 2 minutes).',
  },
  {
    icon: Clock,
    text: 'We review your site, analytics, and competitive landscape.',
  },
  {
    icon: Calendar,
    text: 'Within 48 hours, you receive a brief assessment and a calendar link.',
  },
  {
    icon: Check,
    text: "If we're a fit, we deliver the Growth Infrastructure Audit in 7 business days.",
  },
];

const revenueSources = [
  { value: 'local', label: 'Local search' },
  { value: 'inbound', label: 'Inbound organic' },
  { value: 'outbound', label: 'Outbound' },
  { value: 'paid', label: 'Paid ads' },
  { value: 'unsure', label: 'Not sure' },
];

const budgetRanges = [
  { value: 'under1k', label: 'Under $1K' },
  { value: '1k-3k', label: '$1K–$3K' },
  { value: '3k-10k', label: '$3K–$10K' },
  { value: '10k-plus', label: '$10K+' },
  { value: 'unsure', label: 'Not sure' },
];

interface FormData {
  name: string;
  businessName: string;
  website: string;
  email: string;
  phone: string;
  revenueSource: string;
  budget: string;
  message: string;
}

export function Contact() {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    businessName: '',
    website: '',
    email: '',
    phone: '',
    revenueSource: '',
    budget: '',
    message: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    try {
      const response = await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          access_key: 'YOUR_WEB3FORMS_KEY',
          ...formData,
          subject: `Apex Audit Request: ${formData.businessName || formData.name}`,
        }),
      });

      if (response.ok) {
        setIsSubmitted(true);
      } else {
        setError('Something went wrong. Please try again or contact us directly.');
      }
    } catch {
      setError('Connection error. Please try again.');
    }

    setIsSubmitting(false);
  };

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  if (isSubmitted) {
    return (
      <section id="contact" className="py-20 lg:py-28 bg-gray-50">
        <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
          <div className="max-w-2xl mx-auto text-center">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <Check className="w-10 h-10 text-green-600" />
            </div>
            <h2 className="text-3xl font-bold text-navy mb-4">
              Got it.
            </h2>
            <p className="text-lg text-gray-600">
              We'll review your details and reply within 48 hours with an initial 
              assessment and calendar link.
            </p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="contact" className="py-20 lg:py-28 bg-gray-50">
      <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
        <div className="max-w-6xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-navy mb-4">
              Request an Infrastructure Audit
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Tell us where revenue should come from. We reply with a clear build 
              plan, timeline, and pricing — no vague proposals.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16">
            {/* Left column - What happens next */}
            <div>
              <h3 className="text-xl font-bold text-navy mb-6">
                What happens next
              </h3>
              <div className="space-y-4">
                {steps.map((step, index) => (
                  <div
                    key={index}
                    className="flex items-start gap-4 p-4 bg-white rounded-lg shadow-sm"
                  >
                    <div className="w-10 h-10 bg-blue/10 rounded-lg flex items-center justify-center flex-shrink-0">
                      <step.icon className="w-5 h-5 text-blue" />
                    </div>
                    <div className="flex items-center">
                      <span className="text-gray-700">{step.text}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Right column - Form */}
            <div className="bg-white rounded-xl p-6 lg:p-8 shadow-sm">
              <form onSubmit={handleSubmit} className="space-y-5">
                {/* Name */}
                <div>
                  <Label htmlFor="name" className="text-navy font-medium">
                    Full name <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="name"
                    required
                    value={formData.name}
                    onChange={(e) => handleInputChange('name', e.target.value)}
                    className="mt-1.5"
                    placeholder="Your name"
                  />
                </div>

                {/* Business name */}
                <div>
                  <Label htmlFor="businessName" className="text-navy font-medium">
                    Business name <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="businessName"
                    required
                    value={formData.businessName}
                    onChange={(e) =>
                      handleInputChange('businessName', e.target.value)
                    }
                    className="mt-1.5"
                    placeholder="Your business name"
                  />
                </div>

                {/* Website */}
                <div>
                  <Label htmlFor="website" className="text-navy font-medium">
                    Website URL <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="website"
                    type="url"
                    required
                    value={formData.website}
                    onChange={(e) =>
                      handleInputChange('website', e.target.value)
                    }
                    className="mt-1.5"
                    placeholder="https://yourwebsite.com"
                  />
                </div>

                {/* Email */}
                <div>
                  <Label htmlFor="email" className="text-navy font-medium">
                    Email <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="email"
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                    className="mt-1.5"
                    placeholder="you@example.com"
                  />
                </div>

                {/* Phone */}
                <div>
                  <Label htmlFor="phone" className="text-navy font-medium">
                    Phone / WhatsApp <span className="text-gray-400">(optional)</span>
                  </Label>
                  <Input
                    id="phone"
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => handleInputChange('phone', e.target.value)}
                    className="mt-1.5"
                    placeholder="+971 50 123 4567"
                  />
                </div>

                {/* Revenue source */}
                <div>
                  <Label className="text-navy font-medium">
                    Revenue source priority <span className="text-red-500">*</span>
                  </Label>
                  <Select
                    required
                    value={formData.revenueSource}
                    onValueChange={(value) =>
                      handleInputChange('revenueSource', value)
                    }
                  >
                    <SelectTrigger className="mt-1.5">
                      <SelectValue placeholder="Select your priority" />
                    </SelectTrigger>
                    <SelectContent>
                      {revenueSources.map((source) => (
                        <SelectItem key={source.value} value={source.value}>
                          {source.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Budget */}
                <div>
                  <Label className="text-navy font-medium">
                    Monthly marketing budget{' '}
                    <span className="text-red-500">*</span>
                  </Label>
                  <Select
                    required
                    value={formData.budget}
                    onValueChange={(value) =>
                      handleInputChange('budget', value)
                    }
                  >
                    <SelectTrigger className="mt-1.5">
                      <SelectValue placeholder="Select budget range" />
                    </SelectTrigger>
                    <SelectContent>
                      {budgetRanges.map((range) => (
                        <SelectItem key={range.value} value={range.value}>
                          {range.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Message */}
                <div>
                  <Label htmlFor="message" className="text-navy font-medium">
                    Anything else we should know{' '}
                    <span className="text-gray-400">(optional)</span>
                  </Label>
                  <Textarea
                    id="message"
                    value={formData.message}
                    onChange={(e) =>
                      handleInputChange('message', e.target.value)
                    }
                    className="mt-1.5 min-h-[100px]"
                    placeholder="Tell us about your current challenges, goals, or questions..."
                  />
                </div>

                {/* Error message */}
                {error && (
                  <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg">
                    {error}
                  </div>
                )}

                {/* Submit button */}
                <Button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full bg-gold hover:bg-gold/90 text-navy font-semibold py-6"
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="mr-2 w-5 h-5 animate-spin" />
                      Sending...
                    </>
                  ) : (
                    <>
                      <Send className="mr-2 w-5 h-5" />
                      Send me the plan
                    </>
                  )}
                </Button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

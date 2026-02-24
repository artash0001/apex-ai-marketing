import { Header } from '@/sections/Header';
import { Hero } from '@/sections/Hero';
import { HowItWorks } from '@/sections/HowItWorks';
import { Engines } from '@/sections/Engines';
import { About } from '@/sections/About';
import { Proof } from '@/sections/Proof';
import { FAQ } from '@/sections/FAQ';
import { Contact } from '@/sections/Contact';
import { Footer } from '@/sections/Footer';
import { FloatingContact } from '@/sections/FloatingContact';

function App() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main>
        <Hero />
        <HowItWorks />
        <Engines />
        <About />
        <Proof />
        <FAQ />
        <Contact />
      </main>
      <Footer />
      <FloatingContact />
    </div>
  );
}

export default App;

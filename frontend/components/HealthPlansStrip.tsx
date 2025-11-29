'use client';

import { ShieldCheck } from 'lucide-react';

const plans = [
  { id: 2, name: 'Dog Life' },
  { id: 3, name: 'Pet Mais Vida' },
  { id: 4, name: 'Tutor & Pet' },
  { id: 5, name: 'Au Happy' },
  { id: 6, name: 'Pet Love' },
];

export default function HealthPlansStrip() {
  return (
    <section id="planos" className="health-plans-strip">
      <div className="container">
        <div className="health-plans-strip-header">
          <span className="health-plans-label">Aceitamos Planos de Saúde Pet</span>
        </div>

        {/* Desktop: Static horizontal strip */}
        <div className="health-plans-grid">
          {plans.map((plan) => (
            <div key={plan.id} className="health-plan-item">
              <div className="health-plan-icon">
                <ShieldCheck width={32} height={32} />
              </div>
              <span className="health-plan-name">{plan.name}</span>
            </div>
          ))}
        </div>

        {/* Mobile: Ticker animation */}
        <div className="health-plans-ticker-wrapper">
          <div className="health-plans-ticker">
            {plans.map((plan) => (
              <div key={plan.id} className="health-plan-item">
                <div className="health-plan-icon">
                  <ShieldCheck width={28} height={28} />
                </div>
                <span className="health-plan-name">{plan.name}</span>
              </div>
            ))}
          </div>
          {/* Duplicate for seamless loop */}
          <div className="health-plans-ticker" aria-hidden="true">
            {plans.map((plan) => (
              <div key={`dup-${plan.id}`} className="health-plan-item">
                <div className="health-plan-icon">
                  <ShieldCheck width={28} height={28} />
                </div>
                <span className="health-plan-name">{plan.name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

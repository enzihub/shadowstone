'use client';
import { SubscriptionPlan } from '@/app/pricing/_interfaces/subscription-plan.interface';
import { useUser } from '@clerk/nextjs';
import { Loader2 } from 'lucide-react';
import { useEffect, useState } from 'react';
import { getPricingPlans, subscribeToPrice } from '../_services/price-service';
import TabSwitcher from './tab-switcher';
import PriceCard from './pricing-card';

/**
 * Pricing Section Component
 * Displays pricing plans with monthly/yearly toggle functionality
 * Fetches plan data from API and renders individual price cards
 */
export default function PricingSection() {
  // State management
  const [interval, setInterval] = useState<'monthly' | 'yearly'>('monthly');
  const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { user } = useUser();

  // Fetch pricing plans on component mount
  useEffect(() => {
    const fetchPlans = async () => {
      try {
        const response = await getPricingPlans();
        setPlans(response.plans);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching pricing plans:', error);
        setIsLoading(false);
      }
    };

    fetchPlans();
  }, []);

  /**
   * Handler for enterprise plan demo button
   * Currently just logs to console, can be expanded for actual demo booking logic
   */
  const handleEnterprisePlanButtonClick = () => {
    const email = process.env.NEXT_PUBLIC_SALES_EMAIL || 'sales@example.com';
    const subject = 'Enterprise plan';
    window.location.href = `mailto:${email}?subject=${encodeURIComponent(subject)}`;
  };

  /**
   * Filters plans based on selected billing interval
   * Converts 'monthly'/'yearly' selection to 'month'/'year' to match API data
   */
  const filteredPlans = plans.filter(
    (plan) => plan.interval === (interval === 'monthly' ? 'month' : 'year'),
  );

  /**
   * Handles tab change between monthly and yearly billing
   * @param tab - Selected tab value ('monthly' or 'yearly')
   */
  const handleTabChange = (tab: string) => {
    setInterval(tab === 'monthly' ? 'monthly' : 'yearly');
  };

  /**
   * Formats price number to currency string
   * Converts cents to dollars and adds $ symbol
   * @param price - Price in cents
   * @returns Formatted price string (e.g., "$29.99")
   */
  const formatPrice = (price: number) => {
    return `$${price / 100}`;
  };

  /**
   * Handles click on plan selection button
   * Currently logs plan details, can be expanded for checkout/subscription flow
   * @param plan - Selected subscription plan object
   */
  const handlePlanButtonClick = async (plan: SubscriptionPlan) => {
    console.log('Selected plan price_id:', plan.price_id);
    console.log('Selected plan name:', plan.name);

    // Initiate a checkout session for selected plan
    await subscribeToPrice(
      plan.price_id,
      user?.primaryEmailAddress?.emailAddress!,
    );
  };

  return (
    <div className='w-full'>
      {isLoading ? (
        <div className='flex min-h-[50vh] items-center justify-center'>
          <Loader2 className='h-8 w-8 animate-spin text-blue-500' />
        </div>
      ) : (
        <div className='ms:mx-12 mx-8'>
          {/* Monthly/Yearly billing interval selector */}
          <TabSwitcher onTabChange={handleTabChange} />

          {/* Pricing cards container with responsive layout */}
          <div className='mt-8 flex flex-wrap justify-center gap-5 px-4'>
            {/* Render dynamic pricing plans from API */}
            {filteredPlans.map((plan) => (
              <PriceCard
                key={plan.id}
                title={plan.name}
                subtitle={plan.description}
                price={formatPrice(plan.price)}
                plan={`/${plan.interval}`}
                buttonText={
                  plan.name.toLowerCase().includes('enterprise')
                    ? 'Book Demo'
                    : 'Start free trial'
                }
                onButtonClick={() => handlePlanButtonClick(plan)}
                conditionsArray={[
                  // Base features available in all plans
                  // Edit these to describe your product
                  'Every core feature',
                  'Sign in with Google or GitHub',
                  'Email and SMS notifications',
                  'Billing and invoices through Stripe',
                  'Cancel any time from the portal',
                  // Additional features for enterprise plans
                  ...(plan.name.toLowerCase().includes('enterprise')
                    ? [
                        'Bulk team deployment',
                        'Custom integrations for team workflows',
                        'Priority support & onboarding',
                        'Enterprise-grade security',
                      ]
                    : []),
                ]}
              />
            ))}

            {/* Static Enterprise Plan card with custom pricing */}
            <PriceCard
              title='Enterprise Plan'
              subtitle='For teams that need more.'
              price='Custom'
              buttonText='Book Demo'
              onButtonClick={handleEnterprisePlanButtonClick}
              conditionsArray={[
                'Everything in Pro',
                'Bulk team deployment',
                'Custom integrations for team workflows',
                'Priority support & onboarding',
                'Enterprise-grade security',
              ]}
            />
          </div>
          <div className='traching-[-0.02em] mt-8 flex items-center justify-center text-center text-white/60'>
            <p>
              All plans include a 7-day free trial. No credit card required.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

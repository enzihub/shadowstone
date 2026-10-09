import MainContent from './_components/main-card';
import HeroSection from './_components/hero';
import { getSubscription } from '@/app/pricing/_services/subscription-service';

export default async function AccountPage() {
  const [subscription] = await Promise.all([getSubscription()]);

  return (
    <div className='w-full'>
      <HeroSection
        heading="You're in."
        subHeading='Finish these steps to set up your account.'
      >
        <MainContent subscription={subscription} />
      </HeroSection>
    </div>
  );
}

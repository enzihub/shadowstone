'use client';
import CustomButton from '@/components/ui/custom-button';
import AccountCard from './account-card';
import SubmitField from './submit-field';
import { useEffect, useState } from 'react';
import { UserProfile, useUser } from '@clerk/nextjs';
import {
  getUserPref,
  upsertUserPref,
} from '@/app/(preferences)/_services/preferences.service';
import { sendWelcomeMessage } from '@/app/(preferences)/_services/integration.service';
import { getUserTimezone } from '@/shared/services/timezone';
import OAuthConnections from '@/app/(auth)/_components/OAuthConnections';
import { redirectToStripeCustomerPortal } from '@/app/pricing/_services/manage-subscription';
import { usePlatformStore } from '@/app/stores/usePlatformConnectState';
import { usePhoneStore } from '@/app/stores/usePhoneState';
import useOnboardStore from '@/app/stores/onBoardState';
import { useAboutStore } from '@/app/stores/useAboutState';
import { getUserIdByClerkId } from '@/app/(user)/_services/user.service';
import { set } from 'zod';

export default function MainContent({ subscription }: any) {
  const placeholderPhone = '+1 555 0100';
  const placeholderAbout =
    'I run a small design studio';
  const { user } = useUser();
  const { phone, setPhone } = usePhoneStore();
  const [timezone] = useState(getUserTimezone());
  const [toggleLoading, setToggleLoading] = useState(false);
  const [updating, setUpdating] = useState(false);
  const [updatingAbout, setUpdatingAbout] = useState(false);
  const [loading, setLoading] = useState(false);
  const [about, setAbout] = useState('');
  const [descriptionInput, setDescriptionInput] = useState('');
  const { description, setDescription } = useAboutStore();
  const [loadingContinue, setLoadingContinue] = useState(false);
  const { isPlatformConnected } = usePlatformStore();
  const [phoneInput, setPhoneInput] = useState('');
  const { isCompleted, setIsCompleted } = useOnboardStore();
  const [done, setDone] = useState(false);
  const [userId, setUserId] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [descErrorMessage, setDescErrorMessage] = useState('');
  const PHONE_REGEX = /^\+(?:[0-9] ?){6,14}[0-9]$/;

  const validatePhone = (phone: string) => {
    if (!phone) {
      return 'Phone number is required';
    }
    if (!PHONE_REGEX.test(phone)) {
      return 'Please provide a valid phone number';
    }
    return '';
  };

  const validateDescription = (text: string) => {
    if (!text) {
      return 'This field is required';
    }
    return '';
  };
  useEffect(() => {
    const fetchUserId = async () => {
      if (user?.id) {
        const fetchedUserId = await getUserIdByClerkId(user.id);
        if (fetchedUserId) {
          setUserId(fetchedUserId);
          console.log('Fetched userId:', fetchedUserId);
        }
      }
    };

    if (user) {
      fetchUserId();
    }
  }, [user?.id]);

  const handleUpdateDescription = async () => {
    const validationError = validateDescription(descriptionInput);
    if (validationError) {
      setDescErrorMessage(validationError);
      return;
    }
    setUpdatingAbout(true);
    setDescErrorMessage('');
    let descriptionUpdated = false;
    try {
      const prefResult = await upsertUserPref(
        userId,
        user?.primaryEmailAddress?.emailAddress!,
        phone?.trim() ?? '',
        descriptionInput,
        timezone,
      );

      if (prefResult) {
        descriptionUpdated = true;
        alert('Description updated successfully! 🎉');
      } else {
        alert('Description update failed. Please try again.');
      }
    } catch (error) {
      console.error('Error updating description:', error);
      alert(
        `Failed to update description: ${error instanceof Error ? error.message : 'Unknown error'}`,
      );
    } finally {
      if (descriptionUpdated) {
        setDescription(descriptionInput);
      }
      setUpdatingAbout(false);
    }
  };

  const handleChangeDescription = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDescriptionInput(e.target.value);
  };

  const handleUpdatePhone = async () => {
    const validationError = validatePhone(phoneInput);

    if (validationError) {
      setErrorMessage(validationError);
      return;
    }
    setErrorMessage('');
    setUpdating(true);
    let prefUpdated = false;
    try {
      const prefResult = await upsertUserPref(
        user?.id!,
        user?.primaryEmailAddress?.emailAddress!,
        phoneInput,
        description,
        timezone,
      );

      if (prefResult) {
        prefUpdated = true;
        alert(`Preferences updated successfully! 🎉`);
      } else {
        alert('Preferences update failed. Please try again.');
      }
    } catch (error) {
      console.error('Error updating preferences:', error);
      alert(`Failed to update preferences: ${error}`);
    } finally {
      if (prefUpdated) {
        setPhone(phoneInput);
      }
    }

    try {
      if (prefUpdated) {
        await sendWelcomeMessage(phoneInput);
      }
    } catch (error) {
      console.error('Error sending welcome message:', error);
      alert(`Failed to send welcome message: ${error}`);
    } finally {
      setUpdating(false);
    }
  };

  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPhoneInput(e.target.value);
  };

  const fetchPref = async () => {
    if (!user?.id!) {
      console.error('User not found');
      return;
    }
    try {
      setToggleLoading(true);
      const userPref = await getUserPref(
        user?.primaryEmailAddress?.emailAddress!,
      );
      setPhone(userPref?.phone ?? '');
      setPhoneInput(userPref?.phone ?? '');
      setDescription(userPref?.description ?? '');
      setDescriptionInput(userPref?.description ?? '');
    } catch (error) {
      console.error('Error fetching phone:', error);
    } finally {
      setToggleLoading(false);
    }
  };

  useEffect(() => {
    if (!phone) {
      fetchPref();
    }
  }, [user?.id, setPhone]);

  const handleRedirectToPortal = async () => {
    setLoading(true);
    try {
      return await redirectToStripeCustomerPortal();
    } catch (error) {
      console.error('Error getting portal URL:', error);
      setLoading(false);
    } finally {
      setLoading(false);
    }
  };

  const handleContinueClick = () => {
    setLoadingContinue(true);
    setTimeout(() => {
      setDone(true);
    }, 1000);
    setTimeout(() => {
      if (isPlatformConnected && phone) {
        setIsCompleted(true);
      }
      setLoadingContinue(false);
    }, 2000);
  };

  return (
    <div className='isolate mx-8 flex aspect-video flex-col gap-5 rounded-2xl border-2 border-[#1C1C1C] bg-white/5 py-[32px] shadow-lg ring-1 ring-black/5 backdrop-blur-md md:mx-auto md:max-w-lg'>
      {/*<UserProfile />*/}
      <AccountCard
        title={
          isPlatformConnected && isCompleted
            ? 'Linked accounts'
            : 'Step 1. Connect an account'
        }
        subTitile={
          isPlatformConnected && isCompleted
            ? 'Your connected sign-in providers'
            : 'Link the services this app can act on for you'
        }
        isRight={isPlatformConnected}
        // hideText
      >
        <div className='flex max-w-xs justify-start'>
          <OAuthConnections />
        </div>
      </AccountCard>
      {/* TODO: Integrate the about section */}
      <AccountCard
        title={
          description != null &&
          description !== placeholderAbout &&
          description.trim() !== '' &&
          isCompleted
            ? 'About you'
            : 'Step 2. Tell us about you'
        }
        subTitile='A sentence or two. The core API can use it to personalise messages'
        isRight={
          description != null &&
          description !== placeholderAbout &&
          description.trim() !== ''
        }
      >
        <SubmitField
          buttonText={updatingAbout ? 'Updating...' : 'Submit'}
          disableButton={updatingAbout}
          placeholder={placeholderAbout}
          onChangeInput={handleChangeDescription}
          onclickButton={handleUpdateDescription}
          loading={toggleLoading}
          value={descriptionInput}
          errorMessage={descErrorMessage}
        />
      </AccountCard>

      <AccountCard
        title={
          phone != null &&
          phone !== placeholderPhone &&
          phone.trim() !== '' &&
          isCompleted
            ? 'Phone number'
            : 'Step 3. Add a phone number'
        }
        subTitile='Saving it queues a welcome message on the core API'
        isRight={
          phone != null && phone !== placeholderPhone && phone.trim() !== ''
        }
      >
        <SubmitField
          buttonText={updating ? 'Updating...' : 'Submit'}
          disableButton={updating}
          placeholder={placeholderPhone}
          onChangeInput={handlePhoneChange}
          onclickButton={handleUpdatePhone}
          loading={toggleLoading}
          value={phoneInput}
          errorMessage={errorMessage}
        />
      </AccountCard>
      {phone != '' && isCompleted ? (
        <AccountCard
          title='Subscription'
          subTitile='Update plan, view invoices and manage payments'
          isRight={subscription != null}
        >
          <button
            onClick={
              subscription
                ? async () => {
                    await handleRedirectToPortal();
                  }
                : () => {
                    window.location.href =
                      process.env.NEXT_PUBLIC_STRIPE_PAYMENT_LINK1!;
                  }
            }
            disabled={loading}
            type='button'
            className='w-full rounded-2xl bg-[#0059FF] px-3 py-2.5 font-sans text-lg font-medium tracking-[-0.02em] text-[#FCFCFA] hover:bg-blue-700 focus:outline-none disabled:cursor-not-allowed disabled:opacity-50 md:text-xl'
          >
            {loading
              ? 'Redirecting...'
              : subscription
                ? 'Manage Subscription'
                : 'Start Subscription'}
          </button>
        </AccountCard>
      ) : (
        <AccountCard
          title='Step 4. Start your trial'
          subTitile='Pick a plan on the pricing page. Stripe handles checkout and the customer portal'
          isRight={done || subscription != null}
        ></AccountCard>
      )}
      {!isCompleted && (
        <div className='px-6'>
          <CustomButton
            buttonText={loadingContinue ? 'Loading...' : 'Continue'}
            onClick={handleContinueClick}
            width='w-full'
            disabled={loadingContinue}
            className='bg-gradient-to-t from-[#222222] via-[#282B2B] to-[#222222] px-4 py-2.5 font-sans text-[20px] font-medium text-white hover:bg-[#222222] disabled:bg-white/15'
            icon={
              <svg
                className='h-4 w-4 text-white/60'
                viewBox='0 0 24 24'
                fill='currentColor'
                xmlns='http://www.w3.org/2000/svg'
              >
                <path
                  fillRule='evenodd'
                  clipRule='evenodd'
                  d='M12.2929 4.29289C12.6834 3.90237 13.3166 3.90237 13.7071 4.29289L20.7071 11.2929C21.0976 11.6834 21.0976 12.3166 20.7071 12.7071L13.7071 19.7071C13.3166 20.0976 12.6834 20.0976 12.2929 19.7071C11.9024 19.3166 11.9024 18.6834 12.2929 18.2929L17.5858 13H4C3.44772 13 3 12.5523 3 12C3 11.4477 3.44772 11 4 11H17.5858L12.2929 5.70711C11.9024 5.31658 11.9024 4.68342 12.2929 4.29289Z'
                />
              </svg>
            }
          />
        </div>
      )}
    </div>
  );
}

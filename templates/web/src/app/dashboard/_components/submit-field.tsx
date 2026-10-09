import React, { useState } from 'react';
import { Skeleton } from '@/components/ui/skeleton';

export default function SubmitField({
  buttonText,
  onChangeInput,
  disableButton,
  placeholder,
  value = '',
  onclickButton,
  errorMessage = '',
  loading = false,
}: {
  buttonText: string;
  placeholder: string;
  onChangeInput?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onclickButton?: (e: React.MouseEvent<HTMLButtonElement>) => void;
  value?: string;
  disableButton?: boolean;
  errorMessage?: string;
  loading?: boolean;
}) {
  return (
    <div>
      {loading ? (
        <div className='flex items-center justify-center gap-2 md:gap-3'>
          <Skeleton className='h-[48px] w-full rounded-xl' />
          <Skeleton className='h-[48px] w-24 rounded-2xl' />
        </div>
      ) : (
        <div className='flex flex-col gap-2'>
          <div className='flex items-center justify-center gap-2 md:gap-3'>
            <input
              value={value}
              placeholder={placeholder}
              onChange={onChangeInput}
              className={`block h-[52px] w-full rounded-xl bg-white/10 px-3 py-3 text-sm text-white focus:border-[#0059FF] focus:ring-[#0059FF] md:text-lg ${
                errorMessage ? 'border border-red-500' : ''
              }`}
            />
            <button
              type='button'
              disabled={disableButton}
              className='h-[52px] w-auto rounded-2xl bg-[#0059FF] px-3 py-3 text-sm font-medium text-[#FCFCFA] hover:bg-blue-700 focus:outline-none disabled:cursor-not-allowed disabled:opacity-50 sm:px-3.5 sm:text-lg'
              onClick={onclickButton}
            >
              {buttonText}
            </button>
          </div>
          {errorMessage && (
            <p className='text-sm text-red-500'>{errorMessage}</p>
          )}
        </div>
      )}
    </div>
  );
}

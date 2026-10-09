// Demo stand-in for @stripe/stripe-js. Checkout goes straight back to the dashboard.
export const loadStripe = async () => ({
  redirectToCheckout: async () => {
    window.location.href = '/dashboard?checkout=demo';
    return {};
  },
});

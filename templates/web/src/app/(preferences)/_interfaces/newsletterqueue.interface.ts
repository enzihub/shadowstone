
export interface UserNewsletter {
  id: string | null;
  user_id: string;
  email: string | null;
  timezone: string | null;
  prefUTCTime: number | null;
  isSubscribed: boolean | null;
  createdAt: string;
  updatedAt: string;
}

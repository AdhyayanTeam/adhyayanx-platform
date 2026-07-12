export type User = {
  id: string;
  organization_id: string;
  email: string;
  name: string;
  is_verified: boolean;
  lifecycle_state: string;
  auth_provider: string;
  version: number;
  created_at: string;
  updated_at: string;
};

export type Organization = {
  id: string;
  name: string;
  slug: string;
  lifecycle_state: string;
  version: number;
  created_at: string;
  updated_at: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
  user: User;
  organization: Organization;
  landing_url: string;
};

export type SignupResponse = {
  organization: Organization;
  user: User;
  verification_email_sent: boolean;
  message: string;
};

export type MeResponse = {
  user: User;
  organization: Organization;
  subscriptions: Record<string, unknown>[];
  roles: string[];
};

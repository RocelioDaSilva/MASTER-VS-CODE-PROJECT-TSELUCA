/**
 * Authentication Module - Client Side Only
 * 
 * Provides client-side authentication utilities:
 * - Token storage and retrieval (localStorage)
 * - Password validation (client-side only, no hashing)
 * - Authenticated API requests
 * - Login, register, logout flows
 * 
 * IMPORTANT: Password hashing and JWT signing/verification happen
 * on the server. The client only stores and forwards tokens.
 */

// ============================================================================
// PASSWORD VALIDATION (client-side only — no hashing in the browser)
// ============================================================================

/**
 * Validate password strength
 * Requirements:
 * - Minimum 8 characters
 * - At least one uppercase letter
 * - At least one lowercase letter
 * - At least one number
 * - At least one special character
 */
export function validatePasswordStrength(password: string): {
  valid: boolean;
  score: number;
  feedback: string[];
} {
  const feedback: string[] = [];
  let score = 0;

  // Check length
  if (password.length >= 8) score += 20;
  if (password.length >= 12) score += 10;
  if (password.length >= 16) score += 10;
  if (password.length < 8) feedback.push('Password must be at least 8 characters long');

  // Check for lowercase
  if (/[a-z]/.test(password)) score += 15;
  else feedback.push('Password must contain at least one lowercase letter');

  // Check for uppercase
  if (/[A-Z]/.test(password)) score += 15;
  else feedback.push('Password must contain at least one uppercase letter');

  // Check for numbers
  if (/\d/.test(password)) score += 15;
  else feedback.push('Password must contain at least one number');

  // Check for special characters
  if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) score += 15;
  else feedback.push('Password must contain at least one special character (!@#$%^&*...)');

  // Check for common weak patterns
  if (/(.)\1{2,}/.test(password)) {
    score -= 10;
    feedback.push('Password contains repeating characters (avoid "aaa", "111", etc.)');
  }

  // Check for sequential characters
  if (
    /(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789)/i.test(
      password
    )
  ) {
    score -= 5;
    feedback.push('Password contains sequential characters (avoid "abc", "123", etc.)');
  }

  const isValid = score >= 60;

  return {
    valid: isValid,
    score: Math.max(0, Math.min(100, score)),
    feedback,
  };
}

/**
 * Validate email format
 */
export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email) && email.length <= 255;
}

/**
 * Validate password match
 */
export function validatePasswordMatch(password: string, confirmPassword: string): boolean {
  if (!password || !confirmPassword) {
    return false;
  }
  return password === confirmPassword;
}

/**
 * Check if password is in common breach list
 */
export function isCommonPassword(password: string): boolean {
  const commonPasswords = [
    'password',
    '12345678',
    'qwerty',
    'abc123',
    'password123',
    'admin',
    'letmein',
    'welcome',
    'monkey',
    'dragon',
  ];

  return commonPasswords.includes(password.toLowerCase());
}

// ============================================================================
// JWT TOKEN UTILITIES (client-side decode only — signing is server-side)
// ============================================================================

/**
 * User payload decoded from a JWT
 */
export interface JWTPayload {
  id: string;
  email: string;
  role?: string;
  exp?: number;
  iat?: number;
}

/**
 * Decode a JWT without cryptographic verification (client-side).
 * Returns null if the token is malformed or expired.
 */
export function decodeToken(token: string): JWTPayload | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')));
    return payload as JWTPayload;
  } catch {
    return null;
  }
}

/**
 * Check whether a JWT is expired (client-side check).
 */
function isTokenExpired(token: string): boolean {
  const payload = decodeToken(token);
  if (!payload?.exp) return true;
  // Add 30-second grace period for clock skew
  return Date.now() / 1000 > payload.exp + 30;
}

/**
 * Verify token validity on the client (decode + expiry check).
 * For cryptographic verification, the server is authoritative.
 */
export function verifyToken(token: string): JWTPayload | null {
  if (isTokenExpired(token)) return null;
  return decodeToken(token);
}

// ============================================================================
// CLIENT-SIDE AUTH UTILITIES
// ============================================================================

import { STORAGE_KEYS, AuthResponse, User } from '../core';

/**
 * Store authentication tokens in localStorage
 */
export function storeAuthTokens(accessToken: string, refreshToken?: string): void {
  localStorage.setItem(STORAGE_KEYS.accessToken, accessToken);
  if (refreshToken) {
    localStorage.setItem(STORAGE_KEYS.refreshToken, refreshToken);
  }
}

/**
 * Retrieve access token from localStorage
 */
export function getAccessToken(): string | null {
  return localStorage.getItem(STORAGE_KEYS.accessToken);
}

/**
 * Retrieve refresh token from localStorage
 */
export function getRefreshToken(): string | null {
  return localStorage.getItem(STORAGE_KEYS.refreshToken);
}

/**
 * Store user info in localStorage
 */
export function storeUser(user: User): void {
  localStorage.setItem(STORAGE_KEYS.user, JSON.stringify(user));
}

/**
 * Retrieve user info from localStorage
 */
export function getStoredUser(): User | null {
  const userJson = localStorage.getItem(STORAGE_KEYS.user);
  if (!userJson) return null;
  try {
    return JSON.parse(userJson);
  } catch {
    return null;
  }
}

/**
 * Clear all authentication data
 */
export function clearAuthData(): void {
  localStorage.removeItem(STORAGE_KEYS.accessToken);
  localStorage.removeItem(STORAGE_KEYS.refreshToken);
  localStorage.removeItem(STORAGE_KEYS.user);
}

/**
 * Check if user is authenticated (token exists and is valid)
 */
export function isAuthenticated(): boolean {
  const token = getAccessToken();
  if (!token) return false;
  const decoded = verifyToken(token);
  return decoded !== null;
}

/**
 * Get current user from stored data
 */
export function getCurrentUser(): User | null {
  return getStoredUser();
}

/**
 * Build Authorization header for API requests
 */
export function getAuthHeader(): { Authorization: string } | {} {
  const token = getAccessToken();
  if (!token) return {};
  return { Authorization: `Bearer ${token}` };
}

/**
 * Handle authentication response from login/register
 */
export function handleAuthResponse(response: AuthResponse): void {
  storeAuthTokens(response.accessToken, response.refreshToken);
  storeUser(response.user);
}

// ============================================================================
// API REQUEST UTILITIES
// ============================================================================

/**
 * Make authenticated API request with token
 */
export async function authenticatedFetch(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const authHeader = getAuthHeader();
  const headers = {
    'Content-Type': 'application/json',
    ...authHeader,
    ...(options.headers || {}),
  };

  return fetch(url, {
    ...options,
    headers,
  });
}

/**
 * Refresh access token using refresh token
 */
export async function refreshAccessToken(apiUrl: string = ''): Promise<string | null> {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return null;

  try {
    const response = await fetch(`${apiUrl}/api/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refreshToken }),
    });

    if (!response.ok) {
      clearAuthData();
      return null;
    }

    const data = await response.json();
    localStorage.setItem(STORAGE_KEYS.accessToken, data.accessToken);
    return data.accessToken;
  } catch (error) {
    clearAuthData();
    return null;
  }
}

/**
 * Perform login request
 */
export async function login(
  email: string,
  password: string,
  apiUrl: string = ''
): Promise<{ success: boolean; user?: User; error?: string }> {
  try {
    const response = await fetch(`${apiUrl}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      return { success: false, error: error.error || 'Login failed' };
    }

    const data: AuthResponse = await response.json();
    handleAuthResponse(data);
    return { success: true, user: data.user };
  } catch (error: any) {
    return { success: false, error: error.message || 'Network error' };
  }
}

/**
 * Perform registration request
 */
export async function register(
  email: string,
  password: string,
  confirmPassword: string,
  apiUrl: string = ''
): Promise<{ success: boolean; user?: User; error?: string }> {
  try {
    const response = await fetch(`${apiUrl}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, confirmPassword }),
    });

    if (!response.ok) {
      const error = await response.json();
      return { success: false, error: error.error || 'Registration failed' };
    }

    const data: AuthResponse = await response.json();
    handleAuthResponse(data);
    return { success: true, user: data.user };
  } catch (error: any) {
    return { success: false, error: error.message || 'Network error' };
  }
}

/**
 * Perform logout request
 */
export async function logout(apiUrl: string = ''): Promise<void> {
  const refreshToken = getRefreshToken();

  try {
    if (refreshToken) {
      await fetch(`${apiUrl}/api/auth/logout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refreshToken }),
      });
    }
  } catch (error) {
    console.error('Logout request failed:', error);
  } finally {
    clearAuthData();
  }
}

// ============================================================================
// FORM VALIDATION UTILITIES
// ============================================================================

/**
 * Validate login form inputs
 */
export function validateLoginForm(email: string, password: string): string[] {
  const errors: string[] = [];

  if (!email) errors.push('Email is required');
  else if (!validateEmail(email)) errors.push('Invalid email format');

  if (!password) errors.push('Password is required');
  else if (password.length < 8) errors.push('Password must be at least 8 characters');

  return errors;
}

/**
 * Validate registration form inputs
 */
export function validateRegistrationForm(
  email: string,
  password: string,
  confirmPassword: string
): string[] {
  const errors: string[] = [];

  if (!email) errors.push('Email is required');
  else if (!validateEmail(email)) errors.push('Invalid email format');

  if (!password) errors.push('Password is required');
  else if (password.length < 8)
    errors.push('Password must be at least 8 characters');
  else if (isCommonPassword(password))
    errors.push('Password is too common, please choose a stronger one');

  const strengthCheck = validatePasswordStrength(password);
  if (!strengthCheck.valid) {
    errors.push(...strengthCheck.feedback);
  }

  if (!confirmPassword) errors.push('Password confirmation is required');
  else if (password !== confirmPassword) errors.push('Passwords do not match');

  return errors;
}

// ============================================================================
// EXPORTS
// ============================================================================

export default {
  validatePasswordStrength,
  validateEmail,
  verifyToken,
  decodeToken,
  storeAuthTokens,
  getAccessToken,
  isAuthenticated,
  login,
  register,
  logout,
  clearAuthData,
  getAuthHeader,
  authenticatedFetch,
  validateLoginForm,
  validateRegistrationForm,
};

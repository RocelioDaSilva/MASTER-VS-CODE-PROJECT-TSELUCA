/**
 * Password Security Utilities
 * Implements bcrypt hashing, validation, and strength checking
 */

import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

/**
 * Hash a plaintext password using bcrypt
 * @param plainPassword - The plaintext password to hash
 * @returns The hashed password
 */
export async function hashPassword(plainPassword: string): Promise<string> {
  try {
    const hash = await bcrypt.hash(plainPassword, SALT_ROUNDS);
    return hash;
  } catch (error) {
    throw new Error('Error hashing password');
  }
}

/**
 * Verify a plaintext password against a hash
 * @param plainPassword - The plaintext password to verify
 * @param hash - The hash to compare against
 * @returns True if password matches, false otherwise
 */
export async function verifyPassword(plainPassword: string, hash: string): Promise<boolean> {
  try {
    return await bcrypt.compare(plainPassword, hash);
  } catch (error) {
    return false;
  }
}

/**
 * Validate password strength
 * Requirements:
 * - Minimum 12 characters
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
  if (/(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789)/i.test(password)) {
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
 * Check if password has been in data breaches (simplified check)
 * In production, integrate with Have I Been Pwned API
 */
export async function checkPasswordInBreaches(password: string): Promise<boolean> {
  // Common weak passwords
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

  const lowerPassword = password.toLowerCase();
  return commonPasswords.includes(lowerPassword);
}

/**
 * Validate email format
 */
export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email) && email.length <= 255;
}

/**
 * Sanitize password confirmation
 */
export function validatePasswordMatch(password: string, confirmPassword: string): boolean {
  if (!password || !confirmPassword) {
    return false;
  }
  return password === confirmPassword;
}

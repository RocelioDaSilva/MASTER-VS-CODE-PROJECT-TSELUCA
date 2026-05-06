/**
 * Authentication Routes
 * Handles user registration, login, logout, password reset, and profile management
 */

import { Router, Request, Response } from 'express';
import Database from 'better-sqlite3';
import Joi from 'joi';
import {
  generateAccessToken,
  generateRefreshToken,
  verifyRefreshToken,
  authMiddleware,
  loginLimiter,
  registerLimiter,
} from '../middleware/auth';
import {
  hashPassword,
  verifyPassword,
  validatePasswordStrength,
  validateEmail,
  validatePasswordMatch,
} from '../utils/password';

const router = Router();
const db = new Database('scenarios.db');

/**
 * Initialize users table if it doesn't exist
 */
function initializeUsersTable() {
  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id TEXT PRIMARY KEY,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
  `);
}

initializeUsersTable();

/**
 * Store for refresh tokens (in production, use Redis or persistent storage)
 */
const refreshTokenStore = new Map<string, { userId: string; expiresAt: number }>();

/**
 * Validation Schemas
 */
const registerSchema = Joi.object({
  email: Joi.string().email().max(255).required(),
  password: Joi.string().min(8).required(),
  confirmPassword: Joi.string().valid(Joi.ref('password')).required(),
});

const loginSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().required(),
});

const resetPasswordSchema = Joi.object({
  password: Joi.string().min(8).required(),
  newPassword: Joi.string().min(8).required(),
  confirmNewPassword: Joi.string().valid(Joi.ref('newPassword')).required(),
});

/**
 * POST /api/auth/register
 * Register a new user account
 */
router.post('/register', registerLimiter, async (req: Request, res: Response): Promise<void> => {
  try {
    // Validate input
    const { error, value } = registerSchema.validate(req.body);
    if (error) {
      res.status(400).json({ error: error.details[0].message });
      return;
    }

    const { email, password } = value;

    // Validate email format
    if (!validateEmail(email)) {
      res.status(400).json({ error: 'Invalid email format' });
      return;
    }

    // Validate password strength
    const passwordCheck = validatePasswordStrength(password);
    if (!passwordCheck.valid) {
      res.status(400).json({
        error: 'Password does not meet security requirements',
        feedback: passwordCheck.feedback,
      });
      return;
    }

    // Check if email already exists
    const existingUser = db.prepare('SELECT id FROM users WHERE email = ?').get(email);
    if (existingUser) {
      res.status(409).json({ error: 'Email already registered' });
      return;
    }

    // Hash password
    const passwordHash = await hashPassword(password);

    // Generate user ID
    const userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    // Insert user into database
    db.prepare(
      'INSERT INTO users (id, email, password_hash) VALUES (?, ?, ?)'
    ).run(userId, email, passwordHash);

    // Generate tokens
    const accessToken = generateAccessToken(userId, email);
    const refreshToken = generateRefreshToken(userId);

    // Store refresh token
    refreshTokenStore.set(refreshToken, {
      userId,
      expiresAt: Date.now() + 7 * 24 * 60 * 60 * 1000, // 7 days
    });

    res.status(201).json({
      message: 'User registered successfully',
      accessToken,
      refreshToken,
      user: { id: userId, email },
    });
  } catch (err: any) {
    console.error('Registration error:', err);
    res.status(500).json({ error: 'Registration failed' });
  }
});

/**
 * POST /api/auth/login
 * Login with email and password
 */
router.post('/login', loginLimiter, async (req: Request, res: Response): Promise<void> => {
  try {
    // Validate input
    const { error, value } = loginSchema.validate(req.body);
    if (error) {
      res.status(400).json({ error: error.details[0].message });
      return;
    }

    const { email, password } = value;

    // Find user by email
    const user = db.prepare('SELECT * FROM users WHERE email = ?').get(email) as any;
    if (!user) {
      res.status(401).json({ error: 'Invalid email or password' });
      return;
    }

    // Verify password
    const passwordMatch = await verifyPassword(password, user.password_hash);
    if (!passwordMatch) {
      res.status(401).json({ error: 'Invalid email or password' });
      return;
    }

    // Generate tokens
    const accessToken = generateAccessToken(user.id, user.email);
    const refreshToken = generateRefreshToken(user.id);

    // Store refresh token
    refreshTokenStore.set(refreshToken, {
      userId: user.id,
      expiresAt: Date.now() + 7 * 24 * 60 * 60 * 1000, // 7 days
    });

    res.json({
      message: 'Login successful',
      accessToken,
      refreshToken,
      user: { id: user.id, email: user.email },
    });
  } catch (err: any) {
    console.error('Login error:', err);
    res.status(500).json({ error: 'Login failed' });
  }
});

/**
 * POST /api/auth/refresh
 * Refresh expired access token using refresh token
 */
router.post('/refresh', (req: Request, res: Response): void => {
  try {
    const { refreshToken } = req.body;

    if (!refreshToken) {
      res.status(400).json({ error: 'Refresh token required' });
      return;
    }

    const tokenData = refreshTokenStore.get(refreshToken);
    if (!tokenData || tokenData.expiresAt < Date.now()) {
      refreshTokenStore.delete(refreshToken);
      res.status(401).json({ error: 'Invalid or expired refresh token' });
      return;
    }

    const user = db.prepare('SELECT * FROM users WHERE id = ?').get(tokenData.userId) as any;
    if (!user) {
      res.status(401).json({ error: 'User not found' });
      return;
    }

    const newAccessToken = generateAccessToken(user.id, user.email);
    res.json({ accessToken: newAccessToken });
  } catch (err: any) {
    console.error('Token refresh error:', err);
    res.status(500).json({ error: 'Token refresh failed' });
  }
});

/**
 * POST /api/auth/logout
 * Logout and invalidate refresh token
 */
router.post('/logout', (req: Request, res: Response): void => {
  try {
    const { refreshToken } = req.body;

    if (refreshToken) {
      refreshTokenStore.delete(refreshToken);
    }

    res.json({ message: 'Logout successful' });
  } catch (err: any) {
    console.error('Logout error:', err);
    res.status(500).json({ error: 'Logout failed' });
  }
});

/**
 * GET /api/auth/profile
 * Get current user profile (requires authentication)
 */
router.get('/profile', authMiddleware, (req: Request, res: Response): void => {
  try {
    if (!req.user) {
      res.status(401).json({ error: 'Not authenticated' });
      return;
    }

    const user = db.prepare('SELECT id, email, created_at FROM users WHERE id = ?').get(req.user.id) as any;
    if (!user) {
      res.status(404).json({ error: 'User not found' });
      return;
    }

    res.json({
      user: {
        id: user.id,
        email: user.email,
        createdAt: user.created_at,
      },
    });
  } catch (err: any) {
    console.error('Profile fetch error:', err);
    res.status(500).json({ error: 'Failed to fetch profile' });
  }
});

/**
 * PUT /api/auth/profile
 * Update user profile (requires authentication)
 */
router.put('/profile', authMiddleware, async (req: Request, res: Response): Promise<void> => {
  try {
    if (!req.user) {
      res.status(401).json({ error: 'Not authenticated' });
      return;
    }

    const { email } = req.body;

    // Validate email if provided
    if (email && !validateEmail(email)) {
      res.status(400).json({ error: 'Invalid email format' });
      return;
    }

    // Check if new email is unique
    if (email && email !== req.user.email) {
      const existingUser = db.prepare('SELECT id FROM users WHERE email = ?').get(email);
      if (existingUser) {
        res.status(409).json({ error: 'Email already in use' });
        return;
      }
    }

    // Update user
    db.prepare('UPDATE users SET email = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?').run(
      email || req.user.email,
      req.user.id
    );

    res.json({
      message: 'Profile updated successfully',
      user: {
        id: req.user.id,
        email: email || req.user.email,
      },
    });
  } catch (err: any) {
    console.error('Profile update error:', err);
    res.status(500).json({ error: 'Failed to update profile' });
  }
});

/**
 * POST /api/auth/change-password
 * Change user password (requires authentication)
 */
router.post('/change-password', authMiddleware, async (req: Request, res: Response): Promise<void> => {
  try {
    if (!req.user) {
      res.status(401).json({ error: 'Not authenticated' });
      return;
    }

    // Validate input
    const { error, value } = resetPasswordSchema.validate(req.body);
    if (error) {
      res.status(400).json({ error: error.details[0].message });
      return;
    }

    const { password, newPassword } = value;

    // Fetch user's password hash
    const user = db.prepare('SELECT password_hash FROM users WHERE id = ?').get(req.user.id) as any;
    if (!user) {
      res.status(404).json({ error: 'User not found' });
      return;
    }

    // Verify old password
    const passwordMatch = await verifyPassword(password, user.password_hash);
    if (!passwordMatch) {
      res.status(401).json({ error: 'Current password is incorrect' });
      return;
    }

    // Validate new password strength
    const passwordCheck = validatePasswordStrength(newPassword);
    if (!passwordCheck.valid) {
      res.status(400).json({
        error: 'New password does not meet security requirements',
        feedback: passwordCheck.feedback,
      });
      return;
    }

    // Hash and update password
    const passwordHash = await hashPassword(newPassword);
    db.prepare('UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?').run(
      passwordHash,
      req.user.id
    );

    res.json({ message: 'Password changed successfully' });
  } catch (err: any) {
    console.error('Password change error:', err);
    res.status(500).json({ error: 'Failed to change password' });
  }
});

export default router;

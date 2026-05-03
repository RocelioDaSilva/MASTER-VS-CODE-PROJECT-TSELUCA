/**
 * OpenAPI 3.0.0 Specification for GEESP-Angola API
 * Auto-generated documentation for Swagger UI
 */

export const openApiSpec = {
  openapi: '3.0.0',
  info: {
    title: 'GEESP-Angola API',
    description: 'Geospatial Energy Suitability and Solar Site Selection Platform for Angola',
    version: '1.0.0',
    contact: {
      name: 'Project Support',
      email: 'support@geesp-angola.org',
    },
    license: {
      name: 'MIT',
    },
  },
  servers: [
    {
      url: 'http://localhost:3000',
      description: 'Development Server',
    },
    {
      url: 'https://api.geesp-angola.org',
      description: 'Production Server',
    },
  ],
  components: {
    securitySchemes: {
      bearerAuth: {
        type: 'http',
        scheme: 'bearer',
        bearerFormat: 'JWT',
        description: 'Bearer token obtained from /api/auth/login endpoint',
      },
    },
    schemas: {
      User: {
        type: 'object',
        properties: {
          id: { type: 'string', example: 'user_1709728351234_abc123' },
          email: { type: 'string', format: 'email', example: 'user@example.com' },
          createdAt: { type: 'string', format: 'date-time' },
        },
      },
      LoginRequest: {
        type: 'object',
        required: ['email', 'password'],
        properties: {
          email: { type: 'string', format: 'email', example: 'user@example.com' },
          password: { type: 'string', format: 'password', minLength: 8 },
        },
      },
      LoginResponse: {
        type: 'object',
        properties: {
          message: { type: 'string', example: 'Login successful' },
          accessToken: { type: 'string', description: '15-minute JWT access token' },
          refreshToken: { type: 'string', description: '7-day refresh token' },
          user: { $ref: '#/components/schemas/User' },
        },
      },
      RegisterRequest: {
        type: 'object',
        required: ['email', 'password', 'confirmPassword'],
        properties: {
          email: { type: 'string', format: 'email' },
          password: { type: 'string', format: 'password', minLength: 8 },
          confirmPassword: { type: 'string', format: 'password' },
        },
      },
      Scenario: {
        type: 'object',
        properties: {
          id: { type: 'string', example: 'scenario_abc123' },
          name: { type: 'string', example: 'Huila Province 2026' },
          description: { type: 'string' },
          weights: {
            type: 'object',
            properties: {
              climate: { type: 'number', minimum: 0, maximum: 1 },
              soil: { type: 'number', minimum: 0, maximum: 1 },
              terrain: { type: 'number', minimum: 0, maximum: 1 },
              infrastructure: { type: 'number', minimum: 0, maximum: 1 },
            },
          },
          solar_params: {
            type: 'object',
            properties: {
              wattage: { type: 'number' },
              efficiency: { type: 'number' },
              lifetime: { type: 'number' },
            },
          },
          created_at: { type: 'string', format: 'date-time' },
          updated_at: { type: 'string', format: 'date-time' },
          tags: { type: 'array', items: { type: 'string' } },
        },
      },
      ErrorResponse: {
        type: 'object',
        properties: {
          error: { type: 'string', example: 'Invalid credentials' },
          feedback: {
            type: 'array',
            items: { type: 'string' },
            description: 'Additional validation feedback',
          },
        },
      },
      HealthResponse: {
        type: 'object',
        properties: {
          status: { type: 'string', enum: ['ok'] },
          timestamp: { type: 'string', format: 'date-time' },
        },
      },
    },
  },
  security: [
    {
      bearerAuth: [],
    },
  ],
  paths: {
    '/api/health': {
      get: {
        tags: ['Health'],
        summary: 'Health check endpoint',
        description: 'Returns server status',
        security: [],
        responses: {
          '200': {
            description: 'Server is healthy',
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/HealthResponse' },
              },
            },
          },
        },
      },
    },
    '/api/auth/register': {
      post: {
        tags: ['Authentication'],
        summary: 'Register a new user',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: { $ref: '#/components/schemas/RegisterRequest' },
            },
          },
        },
        security: [],
        responses: {
          '201': {
            description: 'User registered successfully',
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/LoginResponse' },
              },
            },
          },
          '400': {
            description: 'Invalid input or password too weak',
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/ErrorResponse' },
              },
            },
          },
          '409': {
            description: 'Email already registered',
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/ErrorResponse' },
              },
            },
          },
          '429': {
            description: 'Too many registration attempts',
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/ErrorResponse' },
              },
            },
          },
        },
      },
    },
    '/api/auth/login': {
      post: {
        tags: ['Authentication'],
        summary: 'Login with email and password',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: { $ref: '#/components/schemas/LoginRequest' },
            },
          },
        },
        security: [],
        responses: {
          '200': {
            description: 'Login successful',
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/LoginResponse' },
              },
            },
          },
          '401': {
            description: 'Invalid email or password',
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/ErrorResponse' },
              },
            },
          },
          '429': {
            description: 'Too many login attempts',
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/ErrorResponse' },
              },
            },
          },
        },
      },
    },
    '/api/auth/refresh': {
      post: {
        tags: ['Authentication'],
        summary: 'Refresh access token',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                required: ['refreshToken'],
                properties: {
                  refreshToken: { type: 'string' },
                },
              },
            },
          },
        },
        security: [],
        responses: {
          '200': {
            description: 'New access token generated',
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    accessToken: { type: 'string' },
                  },
                },
              },
            },
          },
          '401': {
            description: 'Invalid or expired refresh token',
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/ErrorResponse' },
              },
            },
          },
        },
      },
    },
    '/api/auth/logout': {
      post: {
        tags: ['Authentication'],
        summary: 'Logout and invalidate refresh token',
        requestBody: {
          required: false,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                properties: {
                  refreshToken: { type: 'string' },
                },
              },
            },
          },
        },
        responses: {
          '200': {
            description: 'Logout successful',
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    message: { type: 'string' },
                  },
                },
              },
            },
          },
        },
      },
    },
    '/api/auth/profile': {
      get: {
        tags: ['Authentication'],
        summary: 'Get current user profile',
        responses: {
          '200': {
            description: 'User profile retrieved',
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    user: { $ref: '#/components/schemas/User' },
                  },
                },
              },
            },
          },
          '401': {
            description: 'Not authenticated',
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/ErrorResponse' },
              },
            },
          },
        },
      },
      put: {
        tags: ['Authentication'],
        summary: 'Update user profile',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                properties: {
                  email: { type: 'string', format: 'email' },
                },
              },
            },
          },
        },
        responses: {
          '200': {
            description: 'Profile updated',
          },
          '401': {
            description: 'Not authenticated',
          },
        },
      },
    },
    '/api/auth/change-password': {
      post: {
        tags: ['Authentication'],
        summary: 'Change user password',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                required: ['password', 'newPassword', 'confirmNewPassword'],
                properties: {
                  password: { type: 'string', format: 'password' },
                  newPassword: { type: 'string', format: 'password' },
                  confirmNewPassword: { type: 'string', format: 'password' },
                },
              },
            },
          },
        },
        responses: {
          '200': {
            description: 'Password changed successfully',
          },
          '401': {
            description: 'Current password incorrect',
          },
        },
      },
    },
    '/api/scenarios': {
      get: {
        tags: ['Scenarios'],
        summary: 'List all scenarios',
        parameters: [
          {
            name: 'user_id',
            in: 'query',
            schema: { type: 'string' },
            description: 'Filter by user ID',
          },
          {
            name: 'tag',
            in: 'query',
            schema: { type: 'string' },
            description: 'Filter by tag',
          },
        ],
        responses: {
          '200': {
            description: 'List of scenarios',
            content: {
              'application/json': {
                schema: {
                  type: 'array',
                  items: { $ref: '#/components/schemas/Scenario' },
                },
              },
            },
          },
        },
      },
      post: {
        tags: ['Scenarios'],
        summary: 'Create a new scenario',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: { $ref: '#/components/schemas/Scenario' },
            },
          },
        },
        responses: {
          '201': {
            description: 'Scenario created',
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    id: { type: 'string' },
                    message: { type: 'string' },
                  },
                },
              },
            },
          },
          '400': {
            description: 'Invalid input',
          },
        },
      },
    },
    '/api/scenarios/{id}': {
      get: {
        tags: ['Scenarios'],
        summary: 'Get scenario by ID',
        parameters: [
          {
            name: 'id',
            in: 'path',
            required: true,
            schema: { type: 'string' },
          },
        ],
        responses: {
          '200': {
            description: 'Scenario details',
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/Scenario' },
              },
            },
          },
          '404': {
            description: 'Scenario not found',
          },
        },
      },
      delete: {
        tags: ['Scenarios'],
        summary: 'Delete scenario',
        parameters: [
          {
            name: 'id',
            in: 'path',
            required: true,
            schema: { type: 'string' },
          },
        ],
        responses: {
          '200': {
            description: 'Scenario deleted',
          },
          '404': {
            description: 'Scenario not found',
          },
        },
      },
    },
    '/api/calculate-financial-metrics': {
      post: {
        tags: ['Financial Analysis'],
        summary: 'Calculate financial metrics for a scenario',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                required: ['ghi', 'area_m2', 'solar_params'],
                properties: {
                  ghi: {
                    type: 'number',
                    description: 'Global Horizontal Irradiance (kWh/m²/day)',
                  },
                  area_m2: { type: 'number', description: 'Array area in m²' },
                  solar_params: {
                    type: 'object',
                    description: 'Solar system parameters',
                  },
                },
              },
            },
          },
        },
        responses: {
          '200': {
            description: 'Financial metrics calculated',
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    lcoe: { type: 'number', description: 'Levelized Cost of Energy' },
                    roi: { type: 'number', description: 'Return on Investment %' },
                    payback_years: { type: 'number' },
                  },
                },
              },
            },
          },
          '400': {
            description: 'Invalid parameters',
          },
        },
      },
    },
    '/api/filter-communities': {
      post: {
        tags: ['Analysis'],
        summary: 'Filter communities based on criteria',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                properties: {
                  scenario_id: { type: 'string' },
                  suitability_min: { type: 'number' },
                  lcoe_max: { type: 'number' },
                },
              },
            },
          },
        },
        responses: {
          '200': {
            description: 'Filtered communities',
            content: {
              'application/json': {
                schema: {
                  type: 'array',
                  items: {
                    type: 'object',
                  },
                },
              },
            },
          },
          '429': {
            description: 'Rate limit exceeded for this heavy operation',
          },
        },
      },
    },
  },
};

#!/usr/bin/env node

/**
 * Build Validation Script
 * Validates the frontend consolidation by checking essential files and imports
 */

const fs = require('fs');
const path = require('path');

const reportLines = [];

function log(msg) {
  console.log(msg);
  reportLines.push(msg);
}

function separator() {
  log('─'.repeat(80));
}

function section(title) {
  separator();
  log(`📋 ${title}`);
  separator();
}

try {
  section('PHASE E: BUILD VALIDATION');
  
  // 1. Check essential files exist
  section('1. Checking Essential Consolidated Files');
  
  const essentialFiles = [
    'src/core.ts',
    'src/auth/index.ts',
    'src/hooks/index.ts',
    'src/hooks/useAnalysis.ts',
    'src/hooks/useScenario.ts',
    'src/App.tsx',
    'package.json',
    'tsconfig.json'
  ];
  
  let filesOk = true;
  for (const file of essentialFiles) {
    const fullPath = path.join(__dirname, file);
    const exists = fs.existsSync(fullPath);
    const status = exists ? '✅' : '❌';
    log(`${status} ${file}`);
    if (!exists) filesOk = false;
  }
  
  // 2. Check obsolete files were deleted
  section('2. Verifying Obsolete Files Were Deleted');
  
  const obsoleteFiles = [
    'src/types.ts',
    'src/constants.ts',
    'src/swagger.ts',
    'src/middleware/auth.ts',
    'src/routes/auth.ts',
    'src/utils/password.ts'
  ];
  
  let obsoleteOk = true;
  for (const file of obsoleteFiles) {
    const fullPath = path.join(__dirname, file);
    const exists = fs.existsSync(fullPath);
    const status = exists ? '❌' : '✅';
    log(`${status} DELETED: ${file}`);
    if (exists) obsoleteOk = false;
  }
  
  // 3. Check core.ts exports
  section('3. Validating core.ts Exports');
  
  const coreContent = fs.readFileSync(path.join(__dirname, 'src/core.ts'), 'utf8');
  const coreExports = [
    'export interface Community',
    'export interface MCDAWeights',
    'export interface SolarParams',
    'export interface SuitabilityResult',
    'export interface Scenario',
    'export interface ChatMessage',
    'export const ANGOLA_COMMUNITIES',
    'export const DEFAULT_WEIGHTS',
    'export const DEFAULT_SOLAR_PARAMS',
    'export function getAptitudeFromScore',
    'export function getColorFromScore',
    'export function validateWeights',
    'export const openApiSpec'
  ];
  
  let coreOk = true;
  for (const exp of coreExports) {
    const exists = coreContent.includes(exp);
    const status = exists ? '✅' : '❌';
    log(`${status} ${exp}`);
    if (!exists) coreOk = false;
  }
  
  // 4. Check auth module exports
  section('4. Validating auth/index.ts Exports');
  
  const authContent = fs.readFileSync(path.join(__dirname, 'src/auth/index.ts'), 'utf8');
  const authExports = [
    'export async function hashPassword',
    'export async function verifyPassword',
    'export function validatePasswordStrength',
    'export function validateEmail',
    'export function generateAccessToken',
    'export function generateRefreshToken',
    'export function login',
    'export function register',
    'export function logout'
  ];
  
  let authOk = true;
  for (const exp of authExports) {
    const exists = authContent.includes(exp);
    const status = exists ? '✅' : '❌';
    log(`${status} ${exp}`);
    if (!exists) authOk = false;
  }
  
  // 5. Check hooks exist
  section('5. Validating Custom Hooks');
  
  const useAnalysisContent = fs.readFileSync(path.join(__dirname, 'src/hooks/useAnalysis.ts'), 'utf8');
  const useScenarioContent = fs.readFileSync(path.join(__dirname, 'src/hooks/useScenario.ts'), 'utf8');
  
  const hooksOk = useAnalysisContent.includes('export function useAnalysis') && 
                  useScenarioContent.includes('export function useScenario');
  
  log(`${hooksOk ? '✅' : '❌'} useAnalysis hook exists`);
  log(`${hooksOk ? '✅' : '❌'} useScenario hook exists`);
  
  // 6. Check component imports
  section('6. Verifying Component Imports');
  
  const appContent = fs.readFileSync(path.join(__dirname, 'src/App.tsx'), 'utf8');
  const importsOk = appContent.includes("from './core'") && 
                    !appContent.includes("from './types'") &&
                    !appContent.includes("from './constants'");
  
  log(`${importsOk ? '✅' : '❌'} App.tsx imports from core.ts (not old files)`);
  
  // 7. Summary
  section('SUMMARY');
  
  const allOk = filesOk && obsoleteOk && coreOk && authOk && hooksOk && importsOk;
  
  if (allOk) {
    log('🎉 ALL VALIDATIONS PASSED!');
    log('✅ Consolidated files created successfully');
    log('✅ Obsolete files deleted successfully');
    log('✅ All exports present and valid');
    log('✅ All imports updated correctly');
    log('');
    log('✨ Frontend consolidation is complete and verified!');
    log('');
    log('Next steps:');
    log('  1. npm install');
    log('  2. npm run lint');
    log('  3. npm run build');
    log('  4. npm run dev');
  } else {
    log('❌ SOME VALIDATIONS FAILED');
    log('Please review the failures above.');
  }
  
  separator();
  
  // Write report to file
  const reportPath = path.join(__dirname, 'BUILD_VALIDATION_REPORT.txt');
  fs.writeFileSync(reportPath, reportLines.join('\n'));
  log(`\n📄 Report saved to: ${reportPath}`);
  
  process.exit(allOk ? 0 : 1);
  
} catch (error) {
  log(`❌ ERROR: ${error.message}`);
  console.error(error);
  process.exit(1);
}

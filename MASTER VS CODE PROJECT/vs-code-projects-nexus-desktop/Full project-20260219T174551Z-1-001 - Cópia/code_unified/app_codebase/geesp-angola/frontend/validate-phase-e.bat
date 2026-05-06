@echo off
REM Phase E Build Validation Script
echo ========================================
echo GEESP-Angola Frontend Build Validation
echo ========================================
echo.

cd /d "c:\Users\rocel\OneDrive\Desktop\Full project-20260219T174551Z-1-001 - Cópia\MIT-SCIENCE-PAPER\Full project\02_Code\geesp-angola\frontend"

echo Checking environment...
node --version
npm --version
echo.

echo ========================================
echo Step 1: TypeScript Compilation Check
echo ========================================
call npm run lint
if errorlevel 1 (
    echo ✗ TypeScript compilation FAILED
    exit /b 1
) else (
    echo ✓ TypeScript compilation PASSED
)
echo.

echo ========================================
echo Step 2: Production Build
echo ========================================
call npm run build
if errorlevel 1 (
    echo ✗ Production build FAILED
    exit /b 1
) else (
    echo ✓ Production build PASSED
)
echo.

echo ========================================
echo Step 3: Verify dist directory
echo ========================================
if exist "dist\" (
    echo ✓ dist directory created
    dir dist
) else (
    echo ✗ dist directory NOT found
)
echo.

echo ========================================
echo PHASE E BUILD VALIDATION COMPLETE
echo ========================================

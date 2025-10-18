@echo off
chcp 65001 >nul
REM API测试脚本

echo =========================================
echo 知识星球API测试工具
echo =========================================
echo.

REM 检查是否传入参数
if "%1"=="quick" goto quick_test
if "%1"=="full" goto full_test
goto menu

:menu
echo 请选择测试模式:
echo [1] 快速测试 (推荐)
echo [2] 完整测试
echo [Q] 退出
echo.
set /p choice=请输入选项 (1/2/Q):

if /i "%choice%"=="1" goto quick_test
if /i "%choice%"=="2" goto full_test
if /i "%choice%"=="Q" goto end
if /i "%choice%"=="q" goto end
echo 无效选项，请重新选择
echo.
goto menu

:quick_test
echo.
echo [信息] 运行快速测试...
echo.
python backend\tests\quick_test.py
goto end

:full_test
echo.
echo [信息] 运行完整测试...
echo.
python backend\tests\test_api.py
goto end

:end
echo.
pause

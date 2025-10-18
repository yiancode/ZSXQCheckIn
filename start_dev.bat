@echo off
REM Windows开发环境启动脚本
chcp 65001 >nul

echo =========================================
echo 知识星球打卡展示工具 - 开发环境启动
echo =========================================
echo.

REM 检查配置文件
if not exist "config.yml" (
    echo [错误] config.yml 不存在
    echo [提示] 请复制 config.example.yml 为 config.yml 并填入真实配置
    echo.
    pause
    exit /b 1
)

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python未安装或未添加到PATH
    echo [提示] 请安装Python 3.8+并添加到系统PATH
    echo.
    pause
    exit /b 1
)

echo [1/5] 检查Python虚拟环境...
REM 检查Python虚拟环境
if not exist "venv" (
    echo [信息] 创建Python虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 虚拟环境创建失败
        pause
        exit /b 1
    )
)

echo [2/5] 激活虚拟环境...
REM 激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [错误] 虚拟环境激活失败
    pause
    exit /b 1
)

echo [3/5] 安装Python依赖...
REM 安装依赖（静默模式，只显示错误）
pip install -r backend\requirements.txt -q --disable-pip-version-check
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo [4/5] 检查Redis连接...
REM 检查Redis
redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo [警告] Redis未运行，缓存功能将不可用
    echo [提示] 如需缓存功能，请启动Redis或在config.yml中禁用缓存
) else (
    echo [信息] Redis连接正常
)

echo [5/5] 创建日志目录...
REM 创建日志目录
if not exist "logs" mkdir logs

echo.
echo =========================================
echo 启动Flask应用...
echo =========================================
echo [信息] API地址: http://localhost:5000
echo [信息] 健康检查: http://localhost:5000/api/health
echo [信息] 按 Ctrl+C 停止服务
echo =========================================
echo.

REM 启动Flask应用
set FLASK_ENV=development
set PYTHONIOENCODING=utf-8
python backend\run.py

pause

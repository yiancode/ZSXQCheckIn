import { test, expect, request } from '@playwright/test';

// API联通性用例：直接请求后端接口，验证200与数据结构

test.describe('API联通性', () => {
  test('项目列表与统计接口返回200且结构正确', async ({ }) => {
    const apiContext = await request.newContext();

    // 验证项目列表接口
    const resProjects = await apiContext.get('http://localhost:5000/api/projects');
    expect(resProjects.status()).toBe(200);
    const projectsJson = await resProjects.json();
    expect(projectsJson.code).toBe(0);
    expect(projectsJson.data).toBeTruthy();

    // 取一个项目ID（如无则使用示例ID）
    const firstId = projectsJson.data.projects?.[0]?.project_id || '1141152412';

    // 验证统计接口
    const resStats = await apiContext.get(`http://localhost:5000/api/projects/${firstId}/stats`);
    expect(resStats.status()).toBe(200);
    const statsJson = await resStats.json();
    expect(statsJson.code).toBe(0);
    expect(statsJson.data).toBeTruthy();

    // 验证每日统计接口
    const resDaily = await apiContext.get(`http://localhost:5000/api/projects/${firstId}/daily-stats`);
    expect(resDaily.status()).toBe(200);
    const dailyJson = await resDaily.json();
    expect(dailyJson.code).toBe(0);
    expect(dailyJson.data).toBeTruthy();
  });
});
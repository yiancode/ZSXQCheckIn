import { test, expect } from '@playwright/test';

// 主页路由与详情页跳转用例
// 注：为适配前端对 /api/projects 的数据结构预期，这里对该接口进行mock，返回 data 为数组

test.describe('路由与详情页', () => {
  test('首页加载与跳转到详情页', async ({ page }) => {
    // Mock 项目列表接口，返回 data 为数组以适配前端代码
    await page.route('**/api/projects', async (route) => {
      const json = {
        code: 0,
        message: 'success',
        data: [
          {
            checkin_id: '1141152412',
            title: '示例项目',
            status: 'ongoing',
            type: 'continuous',
            checkin_days: 30,
            joined_count: 10,
            statistics: { completed_count: 5 },
            create_time: '2025-01-15 08:30:00'
          }
        ]
      };
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(json)
      });
    });

    // Mock 项目详情相关接口（返回 data 为对象）
    await page.route('**/api/projects/1141152412/stats', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          code: 0,
          message: 'success',
          data: {
            total_members: 100,
            total_checkins: 5000,
            today_checkins: 120,
            continuous_rate: 85.5,
            avg_checkins_per_member: 23.3
          }
        })
      });
    });

    await page.route('**/api/projects/1141152412/daily-stats', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ code: 0, message: 'success', data: { date: '2025-01-15', total_checkins: 120, new_members: 5, active_members: 115 } })
      });
    });

    await page.route('**/api/projects/1141152412', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ code: 0, message: 'success', data: { title: '示例项目', status: 'ongoing', text: '项目描述' } })
      });
    });

    await page.route('**/api/projects/1141152412/leaderboard', async (route) => {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ code: 0, message: 'success', data: [] }) });
    });

    await page.route('**/api/projects/1141152412/topics', async (route) => {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ code: 0, message: 'success', data: [] }) });
    });

    // 打开首页
    await page.goto('/');

    // 断言标题与头部
    await expect(page.getByRole('heading', { name: '打卡项目列表' })).toBeVisible();
    await expect(page.getByRole('heading', { name: '知识星球打卡展示工具' })).toBeVisible();

    // 点击“查看详情”按钮并跳转
    await page.getByRole('button', { name: '查看详情' }).click();

    // 断言详情页内容与返回按钮
    await expect(page.getByRole('button', { name: '返回列表' })).toBeVisible();
    await expect(page.getByRole('heading', { name: '示例项目' })).toBeVisible();

    // 断言统计卡片中的部分字段存在
    await expect(page.getByText('总成员数')).toBeVisible();
    await expect(page.getByText('总打卡次数')).toBeVisible();

    // 返回首页
    await page.getByRole('button', { name: '返回列表' }).click();
    await expect(page.getByRole('heading', { name: '打卡项目列表' })).toBeVisible();
  });
});
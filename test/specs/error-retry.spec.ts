import { test, expect } from '@playwright/test';

// 错误状态下的重试交互用例：先模拟失败，再点击“重试”后成功

test.describe('错误重试交互', () => {
  test('项目列表加载失败后点击重试恢复', async ({ page }) => {
    let firstCall = true;

    await page.route('**/api/projects', async (route) => {
      if (firstCall) {
        firstCall = false;
        // 第一次返回失败响应
        await route.fulfill({
          status: 500,
          contentType: 'application/json',
          body: JSON.stringify({ code: 500, message: '服务器内部错误' })
        });
      } else {
        // 第二次返回成功但空列表（data为数组）
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ code: 0, message: 'success', data: [] })
        });
      }
    });

    await page.goto('/');

    // 首次加载失败，出现错误提示与“重试”按钮
    await expect(page.getByText('加载失败')).toBeVisible();
    await expect(page.getByRole('button', { name: '重试' })).toBeVisible();

    // 点击“重试”后，应看到空状态
    await page.getByRole('button', { name: '重试' }).click();
    await expect(page.getByText('暂无打卡项目')).toBeVisible();
  });
});
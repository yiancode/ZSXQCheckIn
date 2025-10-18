import axios from 'axios'
import { message } from 'antd'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    const { data } = response
    
    // 检查业务状态码
    if (data.code === 0) {
      return data
    } else {
      message.error(data.message || '请求失败')
      return Promise.reject(new Error(data.message || '请求失败'))
    }
  },
  (error) => {
    console.error('API请求错误:', error)
    
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          message.error('Token已失效，请联系管理员更新')
          break
        case 429:
          message.error('请求过于频繁，请稍后再试')
          break
        case 500:
          message.error('服务器内部错误，请稍后再试')
          break
        default:
          message.error(data?.message || '网络请求失败')
      }
    } else if (error.request) {
      message.error('网络连接失败，请检查网络')
    } else {
      message.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

// API方法
export const projectAPI = {
  // 获取项目列表
  getProjects: () => api.get('/projects'),
  
  // 获取项目详情
  getProjectDetail: (projectId) => api.get(`/projects/${projectId}`),
  
  // 获取项目统计
  getProjectStats: (projectId) => api.get(`/projects/${projectId}/stats`),
  
  // 获取每日统计
  getDailyStats: (projectId) => api.get(`/projects/${projectId}/daily-stats`),
  
  // 获取排行榜
  getLeaderboard: (projectId) => api.get(`/projects/${projectId}/leaderboard`),
  
  // 获取话题列表
  getTopics: (projectId) => api.get(`/projects/${projectId}/topics`)
}

// 健康检查
export const healthCheck = () => api.get('/health')

export default api
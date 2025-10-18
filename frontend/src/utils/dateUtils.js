/**
 * 格式化日期时间
 * @param {string|Date} date - 日期字符串或Date对象
 * @param {string} format - 格式类型 'datetime' | 'date' | 'time'
 * @returns {string} 格式化后的日期字符串
 */
export const formatDate = (date, format = 'datetime') => {
  if (!date) return '-'
  
  const dateObj = new Date(date)
  
  if (isNaN(dateObj.getTime())) {
    return '-'
  }
  
  const year = dateObj.getFullYear()
  const month = String(dateObj.getMonth() + 1).padStart(2, '0')
  const day = String(dateObj.getDate()).padStart(2, '0')
  const hours = String(dateObj.getHours()).padStart(2, '0')
  const minutes = String(dateObj.getMinutes()).padStart(2, '0')
  const seconds = String(dateObj.getSeconds()).padStart(2, '0')
  
  switch (format) {
    case 'date':
      return `${year}-${month}-${day}`
    case 'time':
      return `${hours}:${minutes}:${seconds}`
    case 'datetime':
    default:
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
  }
}

/**
 * 获取相对时间描述
 * @param {string|Date} date - 日期字符串或Date对象
 * @returns {string} 相对时间描述
 */
export const getRelativeTime = (date) => {
  if (!date) return '-'
  
  const dateObj = new Date(date)
  const now = new Date()
  const diffMs = now.getTime() - dateObj.getTime()
  const diffSeconds = Math.floor(diffMs / 1000)
  const diffMinutes = Math.floor(diffSeconds / 60)
  const diffHours = Math.floor(diffMinutes / 60)
  const diffDays = Math.floor(diffHours / 24)
  
  if (diffSeconds < 60) {
    return '刚刚'
  } else if (diffMinutes < 60) {
    return `${diffMinutes}分钟前`
  } else if (diffHours < 24) {
    return `${diffHours}小时前`
  } else if (diffDays < 7) {
    return `${diffDays}天前`
  } else {
    return formatDate(date, 'date')
  }
}

/**
 * 检查日期是否为今天
 * @param {string|Date} date - 日期字符串或Date对象
 * @returns {boolean} 是否为今天
 */
export const isToday = (date) => {
  if (!date) return false
  
  const dateObj = new Date(date)
  const today = new Date()
  
  return dateObj.getFullYear() === today.getFullYear() &&
         dateObj.getMonth() === today.getMonth() &&
         dateObj.getDate() === today.getDate()
}

/**
 * 获取日期范围描述
 * @param {string|Date} startDate - 开始日期
 * @param {string|Date} endDate - 结束日期
 * @returns {string} 日期范围描述
 */
export const getDateRange = (startDate, endDate) => {
  if (!startDate && !endDate) return '-'
  if (!startDate) return `截止 ${formatDate(endDate, 'date')}`
  if (!endDate) return `从 ${formatDate(startDate, 'date')} 开始`
  
  return `${formatDate(startDate, 'date')} 至 ${formatDate(endDate, 'date')}`
}
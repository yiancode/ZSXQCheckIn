import React from 'react'
import { Layout, Typography } from 'antd'
import { TrophyOutlined } from '@ant-design/icons'

const { Header: AntHeader } = Layout
const { Title } = Typography

const Header = () => {
  return (
    <AntHeader style={{ 
      background: '#fff', 
      padding: '0 24px', 
      boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
      display: 'flex',
      alignItems: 'center'
    }}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <TrophyOutlined style={{ fontSize: '24px', color: '#1890ff', marginRight: '12px' }} />
        <Title level={3} style={{ margin: 0, color: '#262626' }}>
          知识星球打卡展示工具
        </Title>
      </div>
    </AntHeader>
  )
}

export default Header
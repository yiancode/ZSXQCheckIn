import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  Card, 
  Row, 
  Col, 
  Progress, 
  Button, 
  Spin, 
  Alert, 
  Typography, 
  Tag,
  Statistic,
  Divider
} from 'antd'
import { 
  EyeOutlined, 
  UserOutlined, 
  CalendarOutlined,
  TrophyOutlined,
  ClockCircleOutlined
} from '@ant-design/icons'
import { projectAPI } from '../services/api'
import { formatDate } from '../utils/dateUtils'

const { Title, Text } = Typography

const ProjectList = () => {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await projectAPI.getProjects()
      setProjects(response.data || [])
    } catch (err) {
      setError(err.message || '获取项目列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleViewProject = (projectId) => {
    navigate(`/projects/${projectId}`)
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'ongoing':
        return 'success'
      case 'closed':
        return 'warning'
      case 'over':
        return 'default'
      default:
        return 'default'
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'ongoing':
        return '进行中'
      case 'closed':
        return '已关闭'
      case 'over':
        return '已结束'
      default:
        return '未知'
    }
  }

  if (loading) {
    return (
      <div className="loading-container">
        <Spin size="large">
          <div style={{ padding: '20px', textAlign: 'center' }}>
            加载项目列表中...
          </div>
        </Spin>
      </div>
    )
  }

  if (error) {
    return (
      <div className="page-container">
        <Alert
          message="加载失败"
          description={error}
          type="error"
          showIcon
          action={
            <Button size="small" onClick={fetchProjects} data-testid="retry-button">
              重试
            </Button>
          }
        />
      </div>
    )
  }

  return (
    <div className="page-container">
      <div style={{ marginBottom: 24 }}>
        <Title level={2}>
          <TrophyOutlined style={{ marginRight: 8 }} />
          打卡项目列表
        </Title>
        <Text type="secondary">
          共 {projects.length} 个项目
        </Text>
      </div>

      {projects.length === 0 ? (
        <Card>
          <div className="text-center" style={{ padding: '40px 0' }}>
            <Text type="secondary">暂无打卡项目</Text>
          </div>
        </Card>
      ) : (
        <Row gutter={[16, 16]}>
          {projects.map((project) => (
            <Col xs={24} sm={12} lg={8} xl={6} key={project.checkin_id}>
              <Card
                hoverable
                actions={[
                  <Button 
                    type="primary" 
                    icon={<EyeOutlined />}
                    onClick={() => handleViewProject(project.checkin_id)}
                  >
                    查看详情
                  </Button>
                ]}
              >
                <div style={{ marginBottom: 16 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
                    <Title level={4} style={{ margin: 0, flex: 1, marginRight: 8 }}>
                      {project.title}
                    </Title>
                    <Tag color={getStatusColor(project.status)}>
                      {getStatusText(project.status)}
                    </Tag>
                  </div>
                  
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    {project.type === 'continuous' ? '连续打卡' : '累计打卡'} · 
                    目标 {project.checkin_days} 天
                  </Text>
                </div>

                <div style={{ marginBottom: 16 }}>
                  <Row gutter={16}>
                    <Col span={12}>
                      <Statistic
                        title="参与人数"
                        value={project.joined_count || 0}
                        prefix={<UserOutlined />}
                        valueStyle={{ fontSize: '16px' }}
                      />
                    </Col>
                    <Col span={12}>
                      <Statistic
                        title="完成人数"
                        value={project.statistics?.completed_count || 0}
                        valueStyle={{ fontSize: '16px', color: '#52c41a' }}
                      />
                    </Col>
                  </Row>
                </div>

                {project.joined_count > 0 && (
                  <div style={{ marginBottom: 16 }}>
                    <Text strong style={{ fontSize: '12px', marginBottom: 4, display: 'block' }}>
                      完成率
                    </Text>
                    <Progress
                      percent={Math.round(((project.statistics?.completed_count || 0) / project.joined_count) * 100)}
                      size="small"
                      strokeColor="#52c41a"
                    />
                  </div>
                )}

                <Divider style={{ margin: '12px 0' }} />

                <div style={{ fontSize: '12px', color: '#8c8c8c' }}>
                  <ClockCircleOutlined style={{ marginRight: 4 }} />
                  创建时间: {formatDate(project.create_time)}
                </div>
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </div>
  )
}

export default ProjectList
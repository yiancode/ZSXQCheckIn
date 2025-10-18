import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Card,
  Row,
  Col,
  Statistic,
  Progress,
  Button,
  Spin,
  Alert,
  Typography,
  Tag,
  Divider,
  Tabs,
  List,
  Avatar,
  Space
} from 'antd'
import {
  ArrowLeftOutlined,
  UserOutlined,
  TrophyOutlined,
  CalendarOutlined,
  FireOutlined,
  TeamOutlined,
  BarChartOutlined
} from '@ant-design/icons'
import { projectAPI } from '../services/api'
import { formatDate } from '../utils/dateUtils'

const { Title, Text, Paragraph } = Typography
const { TabPane } = Tabs

const ProjectDetail = () => {
  const { projectId } = useParams()
  const navigate = useNavigate()
  const [project, setProject] = useState(null)
  const [stats, setStats] = useState(null)
  const [dailyStats, setDailyStats] = useState(null)
  const [leaderboard, setLeaderboard] = useState([])
  const [topics, setTopics] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    if (projectId) {
      fetchProjectData()
    }
  }, [projectId])

  const fetchProjectData = async () => {
    try {
      setLoading(true)
      setError(null)

      // 并行获取所有数据
      const promises = [
        projectAPI.getProjectStats(projectId),
        projectAPI.getDailyStats(projectId)
      ]

      // 尝试获取项目详情（可能失败）
      try {
        promises.push(projectAPI.getProjectDetail(projectId))
      } catch (err) {
        console.warn('获取项目详情失败，将使用统计数据')
      }

      // 尝试获取排行榜和话题（可能失败）
      try {
        promises.push(projectAPI.getLeaderboard(projectId))
      } catch (err) {
        console.warn('获取排行榜失败')
      }

      try {
        promises.push(projectAPI.getTopics(projectId))
      } catch (err) {
        console.warn('获取话题列表失败')
      }

      const results = await Promise.allSettled(promises)
      
      // 处理统计数据（必需）
      if (results[0].status === 'fulfilled') {
        setStats(results[0].value.data)
      }
      
      if (results[1].status === 'fulfilled') {
        setDailyStats(results[1].value.data)
      }

      // 处理项目详情（可选）
      if (results[2] && results[2].status === 'fulfilled') {
        setProject(results[2].value.data)
      }

      // 处理排行榜（可选）
      if (results[3] && results[3].status === 'fulfilled') {
        setLeaderboard(results[3].value.data || [])
      }

      // 处理话题列表（可选）
      if (results[4] && results[4].status === 'fulfilled') {
        setTopics(results[4].value.data || [])
      }

    } catch (err) {
      setError(err.message || '获取项目数据失败')
    } finally {
      setLoading(false)
    }
  }

  const handleBack = () => {
    navigate('/')
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
        <Spin size="large" tip="加载项目详情中..." />
      </div>
    )
  }

  if (error) {
    return (
      <div className="page-container">
        <Button 
          icon={<ArrowLeftOutlined />} 
          onClick={handleBack}
          style={{ marginBottom: 16 }}
        >
          返回列表
        </Button>
        <Alert
          message="加载失败"
          description={error}
          type="error"
          showIcon
          action={
            <Button size="small" onClick={fetchProjectData}>
              重试
            </Button>
          }
        />
      </div>
    )
  }

  return (
    <div className="page-container">
      <Button 
        icon={<ArrowLeftOutlined />} 
        onClick={handleBack}
        style={{ marginBottom: 16 }}
      >
        返回列表
      </Button>

      {/* 项目基本信息 */}
      <Card style={{ marginBottom: 16 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
          <div style={{ flex: 1 }}>
            <Title level={2} style={{ margin: 0, marginBottom: 8 }}>
              {project?.title || `项目 ${projectId}`}
            </Title>
            {project?.status && (
              <Tag color={getStatusColor(project.status)} style={{ marginBottom: 8 }}>
                {getStatusText(project.status)}
              </Tag>
            )}
            {project?.text && (
              <Paragraph type="secondary">
                {project.text}
              </Paragraph>
            )}
          </div>
        </div>

        {/* 核心统计数据 */}
        <Row gutter={16}>
          <Col xs={12} sm={6}>
            <Statistic
              title="总成员数"
              value={stats?.total_members || 0}
              prefix={<TeamOutlined />}
            />
          </Col>
          <Col xs={12} sm={6}>
            <Statistic
              title="总打卡次数"
              value={stats?.total_checkins || 0}
              prefix={<FireOutlined />}
            />
          </Col>
          <Col xs={12} sm={6}>
            <Statistic
              title="今日打卡"
              value={stats?.today_checkins || 0}
              prefix={<CalendarOutlined />}
            />
          </Col>
          <Col xs={12} sm={6}>
            <Statistic
              title="连续率"
              value={stats?.continuous_rate || 0}
              suffix="%"
              precision={1}
              prefix={<BarChartOutlined />}
            />
          </Col>
        </Row>

        {stats?.avg_checkins_per_member && (
          <div style={{ marginTop: 16 }}>
            <Text strong>平均每人打卡次数: </Text>
            <Text>{stats.avg_checkins_per_member.toFixed(1)} 次</Text>
          </div>
        )}
      </Card>

      {/* 详细数据标签页 */}
      <Card>
        <Tabs activeKey={activeTab} onChange={setActiveTab}>
          <TabPane tab="数据概览" key="overview">
            <Row gutter={16}>
              <Col span={12}>
                <Card size="small" title="今日统计">
                  {dailyStats ? (
                    <Space direction="vertical" style={{ width: '100%' }}>
                      <Statistic
                        title="活跃成员"
                        value={dailyStats.active_members || 0}
                        prefix={<UserOutlined />}
                      />
                      <Statistic
                        title="新增成员"
                        value={dailyStats.new_members || 0}
                        valueStyle={{ color: '#52c41a' }}
                      />
                      <Statistic
                        title="打卡次数"
                        value={dailyStats.total_checkins || 0}
                        prefix={<FireOutlined />}
                      />
                      <Text type="secondary" style={{ fontSize: '12px' }}>
                        数据日期: {dailyStats.date}
                      </Text>
                    </Space>
                  ) : (
                    <Text type="secondary">暂无今日数据</Text>
                  )}
                </Card>
              </Col>
              <Col span={12}>
                <Card size="small" title="项目信息">
                  {project ? (
                    <Space direction="vertical" style={{ width: '100%' }}>
                      <div>
                        <Text strong>打卡类型: </Text>
                        <Text>{project.type === 'continuous' ? '连续打卡' : '累计打卡'}</Text>
                      </div>
                      <div>
                        <Text strong>目标天数: </Text>
                        <Text>{project.checkin_days} 天</Text>
                      </div>
                      {project.min_words_count && (
                        <div>
                          <Text strong>最少字数: </Text>
                          <Text>{project.min_words_count} 字</Text>
                        </div>
                      )}
                      <div>
                        <Text strong>创建时间: </Text>
                        <Text>{formatDate(project.create_time)}</Text>
                      </div>
                    </Space>
                  ) : (
                    <Text type="secondary">项目详情获取失败</Text>
                  )}
                </Card>
              </Col>
            </Row>
          </TabPane>

          <TabPane tab="排行榜" key="leaderboard">
            {leaderboard.length > 0 ? (
              <List
                dataSource={leaderboard}
                renderItem={(item, index) => (
                  <List.Item>
                    <List.Item.Meta
                      avatar={
                        <div style={{ display: 'flex', alignItems: 'center' }}>
                          <div style={{ 
                            width: 24, 
                            height: 24, 
                            borderRadius: '50%', 
                            backgroundColor: index < 3 ? '#ffd700' : '#f0f0f0',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            marginRight: 8,
                            fontSize: '12px',
                            fontWeight: 'bold'
                          }}>
                            {index + 1}
                          </div>
                          <Avatar src={item.avatar} icon={<UserOutlined />} />
                        </div>
                      }
                      title={item.name || '匿名用户'}
                      description={`打卡 ${item.checkin_count || 0} 次`}
                    />
                  </List.Item>
                )}
              />
            ) : (
              <div className="text-center" style={{ padding: '40px 0' }}>
                <Text type="secondary">暂无排行榜数据</Text>
              </div>
            )}
          </TabPane>

          <TabPane tab="相关话题" key="topics">
            {topics.length > 0 ? (
              <List
                dataSource={topics}
                renderItem={(item) => (
                  <List.Item>
                    <List.Item.Meta
                      title={item.title}
                      description={
                        <Space>
                          <Text type="secondary">{formatDate(item.create_time)}</Text>
                          <Text type="secondary">点赞 {item.likes_count || 0}</Text>
                          <Text type="secondary">评论 {item.comments_count || 0}</Text>
                        </Space>
                      }
                    />
                  </List.Item>
                )}
              />
            ) : (
              <div className="text-center" style={{ padding: '40px 0' }}>
                <Text type="secondary">暂无相关话题</Text>
              </div>
            )}
          </TabPane>
        </Tabs>
      </Card>

      {/* 数据更新时间 */}
      {(stats?.cached_at || dailyStats?.cached_at) && (
        <div style={{ marginTop: 16, textAlign: 'center' }}>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            数据更新时间: {formatDate(stats?.cached_at || dailyStats?.cached_at)}
          </Text>
        </div>
      )}
    </div>
  )
}

export default ProjectDetail
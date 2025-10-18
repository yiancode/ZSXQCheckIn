import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Layout } from 'antd'
import ProjectList from './pages/ProjectList'
import ProjectDetail from './pages/ProjectDetail'
import Header from './components/Header'

const { Content } = Layout

function App() {
  return (
    <Layout className="full-height">
      <Header />
      <Content>
        <Routes>
          <Route path="/" element={<ProjectList />} />
          <Route path="/projects/:projectId" element={<ProjectDetail />} />
        </Routes>
      </Content>
    </Layout>
  )
}

export default App
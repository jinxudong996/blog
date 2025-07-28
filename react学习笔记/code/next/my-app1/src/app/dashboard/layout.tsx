export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    // 主容器，包含导航和主要内容区域
    <div className="dashboard-container" role="region">
      {/* 导航区域 */}
      <nav className="dashboard-navigation">nav</nav>
      {/* 主内容区域 */}
      <main className="dashboard-content">{children}</main>
    </div>
  );
}
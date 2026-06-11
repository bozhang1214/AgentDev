function Home() {
    return (
        <div>
            <h2>欢迎使用个人工具页</h2>
            <p>本应用包含以下功能：</p>
            <ul>
                <li>📝 待办清单（纯前端 + localStorage 持久化</li>
                <li>🤖 AI 助手（支持多轮对话、天气查询）</li>
                <li>🎨 主题切换（深色/浅色模式）</li>
            </ul>
            <p>使用 React Router V7 实现多页面导航。</p>
        </div>
    );
}

export default Home;
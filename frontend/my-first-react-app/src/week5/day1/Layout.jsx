import { NavLink, Outlet } from 'react-router';
import { ACTION, useApp } from '../../contexts/AppContext';
import LoginButton from './LoginButton';

function Layout() {
    const {state, dispatch} = useApp();
    const {theme, user} = state;
    const toggleTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        dispatch({type: ACTION.SET_THEME, payload: newTheme});
    };

    return (
        <div className={`app ${theme}`} style={{ minHeight: '100vh'}}>
            <header style={{ padding: '16px', borderBottom: '1px solid #ccc' }}>
                <nav style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                    <NavLink to="/" style={({ isActive }) => ({ fontWeight: isActive ? 'bold' : 'normal'})}>
                        首页
                    </NavLink>
                    <NavLink to="/chat" style={({ isActive }) => ({ fontWeight: isActive ? 'bold' : 'normal'})}>
                        AI助手
                    </NavLink>
                    <NavLink to="/settings" style={({ isActive }) => ({ fontWeight: isActive ? 'bold' : 'normal' })}>
                        设置
                    </NavLink>
                    <LoginButton />
                    <button onClick={toggleTheme} style={{ marginLeft: 'auto'}}>
                        切换主题
                    </button>
                    <span>欢迎，{user.name}</span>
                </nav>
            </header>

            <main style={{ padding: '20px' }}>
                {/* 子路由组件会渲染在这里 */}
                <Outlet />
            </main>

            <footer style={{ textAlign: 'center', padding: '16px', borderTop: '1px solid #ccc'}}>
                <small>个人工具页 - React Router V7 示例</small>
            </footer>
        </div>
    );
}

export default Layout;
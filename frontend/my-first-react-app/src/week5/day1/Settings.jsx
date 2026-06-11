import { useNavigate } from "react-router";
import { useTheme } from "../../contexts/ThemeContext";
import { useApp, ACTION } from '../../contexts/AppContext';

function Settings() {
    const { state, dispatch } = useApp();
    const { theme } = state;
    const navigate = useNavigate();

    const toggleTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        dispatch({type: ACTION.SET_THEME, payload: newTheme});
    };

    const clearLocalStorage = () => {
        if (confirm('清除本地数据会删除所有待办任务，确定吗？')) {
            localStorage.removeItem('todo_tasks');
            alert('已清除待办数据，刷新页面后生效。')
            navigate('/');
        }
    };

    return (
        <div>
            <h2>设置</h2>
            <div style={{ marginBottom: '16px'}}>
                <label>
                    <input type="checkbox" checked={theme === 'dark'} onChange={toggleTheme} />
                    深色模式
                </label>
            </div>
            <button onClick={clearLocalStorage}>清除待办本地数据</button>
        </div>
    );
}

export default Settings;
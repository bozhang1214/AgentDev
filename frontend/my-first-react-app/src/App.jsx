import { useState } from 'react';
import './App.css';
import TimerControl from './TimerControl';
import TodoApp from './TodoApp';
import { ThemeProvider } from './contexts/ThemeContext';
import { TodoFilterProvider } from './contexts/TodoFilterContext';
import { UserProvider } from './contexts/UserContext';
import Chat from './w4d5/Chat';

function App() {
    const [activeTab, setActiveTab] = useState('todo');

    return (
        <ThemeProvider>
        <div className='app-container'>
            <h1>🛠️ 个人工具页</h1>

            <div className='tab-bar'>
                <button 
                    className={`tab-btn ${activeTab === 'todo' ? 'active' : ''}`}
                    onClick={() => setActiveTab('todo')}
                >
                    📝 待办清单
                </button>
                <button
                    className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
                    onClick={() => setActiveTab('chat')}
                >
                    🤖 AI 助手
                </button>
            </div>

            <div className='tab-content'>
                {activeTab === 'todo' ? (
                    <TodoFilterProvider>
                        <TodoApp />
                    </TodoFilterProvider>
                ) : (
                    <UserProvider>
                        <Chat />
                    </UserProvider>
                )}
            </div>
            <TimerControl />
        </div>
        </ThemeProvider>
    );
}

export default App;
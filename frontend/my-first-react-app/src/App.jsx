// import Counter from "./Counter";
// import TodoInput from "./TodoInput";

// import Chat from "./Chat";
// import TodoApp from "./TodoApp";

// function Welcome(props) {
//     return (
//         <div style={{border: "1px solid #ccc", padding: "20px", borderRadius: "8px", textAlign: "center"}}>
//             <h1>欢迎， {props.name}!</h1>
//             <p>今天是 {new Date().toLocaleDateString()}</p>
//             {props.children && <div>{props.children}</div>}
//         </div>
//     );
// }

// function App() {
//     return (
//         <div>
//             <Welcome name="李华">
//                 <p>✨ 这是你的第一个 React 组件 ✨</p>
//                 <ul>
//                     <li>aaa</li>
//                     <li>bbb</li>
//                     <li>ccc</li>
//                 </ul>
//             </Welcome>
//             <Welcome name="张三" />
//         </div>
//     );
// }

// function App() {
//     return (
//         <div>
//             <Counter />
//             <TodoInput />
//         </div>
//     );
// }

// function App() {
//     return (
//         <div>
//             <TodoApp />
//         </div>
//     );
// }

// function App() {
//     return (
//         <div>
//             <TodoApp />
//             <hr style={{ margin: '40px 0'}}/>
//             <Chat />
//         </div>
//     );
// }


import { useState } from 'react';
import './App.css';
import Chat from './Chat';
import TimerControl from './TimerControl';
import TodoApp from './TodoApp';

function App() {
    const [activeTab, setActiveTab] = useState('todo');

    return (
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
                {activeTab === 'todo' ? <TodoApp /> : <Chat />}
            </div>
            <TimerControl />
        </div>
    );
}

export default App;
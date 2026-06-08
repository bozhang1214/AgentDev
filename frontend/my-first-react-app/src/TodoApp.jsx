import { useEffect, useState } from "react";

function TodoApp() {
    const [tasks, setTasks] = useState(() => {
        const saved = localStorage.getItem('todo_tasks');
        if (saved) {
            return JSON.parse(saved);
        }
        return [
            {id: 1, text: '学习React基础知识', completed: true},
            {id: 2, text: '完成待办应用项目', completed: false},
            {id: 3, text: '阅读《React前端设计》第4章', completed: false}
        ];
    });

    const [inputValue, setInputValue] = useState('');

    useEffect(() => {
        localStorage.setItem('todo_tasks', JSON.stringify(tasks));
    }, [tasks]);

    const addTask = () => {
        const trimmedText = inputValue.trim();
        if (trimmedText === '') {
            alert('请输入任务内容');
            return;
        }
        const newTask = {
            id: Date.now(),
            text: trimmedText,
            completed: false,
        };

        setTasks([...tasks, newTask]);
        setInputValue('');
    };

    const deleteTask = (id) => {
        setTasks(tasks.filter(task => task.id !== id));
    };

    const toggleTask = (id) => {
        setTasks(tasks.map(task =>
            task.id === id ? { ...task, completed: !task.completed } : task
        ));
    };

    return (
        <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px', fontFamily: 'sans-serif'}}>
            <h1>📝 React 待办应用</h1>

            <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && addTask()}
                    placeholder="写一个新任务...."
                    style={{ flex: 1, padding: '8px', fontSize: '16px' }}/>
                <button onClick={addTask} style={{ padding: '8px 16px', cursor: 'pointer' }}>
                    添加
                </button>
            </div>

            {tasks.length === 0 ? (
                <p style={{ color: '#888', textAlign: 'center' }}>
                    ✨ 暂无任务，添加一条吧！
                </p>
            ) : (
                <ul style={{ listStyle: 'none', padding: 0 }}>
                    {tasks.map((task) => (
                        <li
                            key={task.id}
                            style={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'space-between',
                                padding: '10px',
                                marginBottom: '8px',
                                backgroundColor: '#f9f9f9',
                                borderRadius: '8px',
                                border: '1px solid #eee',
                            }}
                        >
                            <span
                                onClick={() => toggleTask(task.id)}
                                style={{
                                    flex: 1,
                                    cursor: 'pointer',
                                    textDecoration: task.completed ? 'line-through' : 'none',
                                    color: task.completed ? '#aaa' : '#333',
                                }}
                            >
                                {task.text}
                            </span>
                            <button
                                onClick={() => deleteTask(task.id)}
                                style={{
                                    backgroundColor: '#ff6b6b',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '4px',
                                    padding: '4px 12px',
                                    cursor: 'pointer',
                                }}
                            >
                                删除
                            </button>
                        </li>
                    ))}
                </ul>
            )}

            <div style={{ marginTop: '20px', fontSize: '14px', color: '#666' }}>
                总计：{tasks.length} 项 | 已完成：{tasks.filter(t => t.completed).length} 项
            </div>
        </div>
    );
}

export default TodoApp;
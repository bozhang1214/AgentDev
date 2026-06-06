import { useState } from "react";

function TodoInput() {
    const [inputValue, setInputValue] = useState("");
    const [todos, setTodos] = useState([]);

    const handleAdd = () => {
        if (inputValue.trim() === "") return;
        setTodos([...todos, {id: Date.now(), text: inputValue}]);
        setInputValue('');
    };

    const handleDelete = (id) => {
        setTodos(todos.filter(todo => todo.id !== id));
    };

    return (
        <div style={{ border: "1px solid #ccc", padding: "20px"}}>
            <h2>待办列表</h2>
            <div>
                <input 
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="输入新任务"
                    style={{ marginRight: "8px" }}
                />
                <button onClick={handleAdd}>添加</button>
            </div>
            <ul style={{ marginTop: "16px" }}>
                {
                    todos.map(todo => (
                        <li key={todo.id}>
                            {todo.text}
                            <button onClick={() => handleDelete(todo.id)} style={{ marginLeft: "8px" }}>删除</button>
                        </li>
                    ))
                }
            </ul>
        </div>
    );
}

export default TodoInput;
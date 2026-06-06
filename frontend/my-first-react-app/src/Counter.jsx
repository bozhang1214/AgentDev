import { useState } from "react";

function Counter() {
    const [count, setCount] = useState(0);

    const increment = () => setCount(prev => prev + 1);
    const decrement = () => setCount(prev => prev - 1);
    const reset = () => setCount(0);

    return (
        <div style={{ border: "1px solid #ccc", padding: "20px", marginBottom: "20px" }}>
            <h2>计数器</h2>
            <p style={{ fontSize: "32px", fontWeight: "bold" }}>{count}</p>
            <button onClick={increment}>➕ 增加</button>
            <button onClick={decrement} disabled={count === 0}>➖ 减少</button>
            <button onClick={reset}>🔄 重置</button>
        </div>
    );
}

export default Counter;
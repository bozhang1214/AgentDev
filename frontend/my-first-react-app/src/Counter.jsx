import { useState } from "react";
import usePrevious from "./hooks/usePrevious";

function Counter() {
    const [count, setCount] = useState(0);
    const prevCount = usePrevious(count);

    const increment = () => setCount(prev => prev + 1);
    const decrement = () => setCount(prev => prev - 1);
    const reset = () => setCount(0);

    return (
        <div style={{ border: "1px solid #ccc", padding: "20px", marginBottom: "20px" }}>
            <h2>计数器</h2>
            <p style={{ fontSize: "20px", fontWeight: "bold", marginBottom: '20px'}}>当前：{count}，上一次：{prevCount}</p>
            <button onClick={increment} style={{ fontSize: '16px'}}>➕ 增加</button>
            <button onClick={decrement} style={{ fontSize: '16px'}} disabled={count === 0}>➖ 减少</button>
            <button onClick={reset} style={{ fontSize: '16px'}}>🔄 重置</button>
        </div>
    );
}

export default Counter;
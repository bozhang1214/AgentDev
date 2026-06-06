import Counter from "./Counter";
import TodoInput from "./TodoInput";

function Welcome(props) {
    return (
        <div style={{border: "1px solid #ccc", padding: "20px", borderRadius: "8px", textAlign: "center"}}>
            <h1>欢迎， {props.name}!</h1>
            <p>今天是 {new Date().toLocaleDateString()}</p>
            {props.children && <div>{props.children}</div>}
        </div>
    );
}

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

function App() {
    return (
        <div>
            <Counter />
            <TodoInput />
        </div>
    );
}

export default App;
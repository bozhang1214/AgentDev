import { useNavigate } from "react-router";

function LoginButton() {
    const navigate = useNavigate();
    const handleLogin = () => {
        navigate('/chat');
    };
    return <button onClick={handleLogin}>登录</button>
}

export default LoginButton;
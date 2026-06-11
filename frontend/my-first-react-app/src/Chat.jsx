import { useEffect, useReducer, useRef, useState } from 'react';
import { useApp } from './contexts/AppContext';
import { useUser } from './contexts/UserContext';
import { ACTION_TYPES, initialMessageState, messageReducer } from './week5/day2/reducers/messageReducer';

function Chat() {
    const [state, dispatch] = useReducer(messageReducer, initialMessageState);
    const { messages, isLoading, error } = state;
    const { state: appState, dispatch: appDispatch } = useApp();
    const { user } = useUser();

    const [inputValue, setInputValue] = useState('');
    const [retryCount, setRetryCount] = useState(0);
    const [toolCalling, setToolCalling] = useState(false);

    const [sessionId, setSessionId] = useState(() => {
        const saved = localStorage.getItem('chat_session_id');
        if (saved) return saved;
        return crypto.randomUUID();
    });

    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    useEffect(() => {
        localStorage.setItem('chat_session_id', sessionId);
    }, [sessionId]);

    const inputRef = useRef(null);
    useEffect(() => {
        inputRef.current?.focus();
    }, []);

    const sendMessage = async () => {
        const userMessage = inputValue.trim();
        if (userMessage === '') return;

        dispatch({type: ACTION_TYPES.ADD_USER_MESSAGE, payload: userMessage});
        setInputValue('');
        dispatch({ type: ACTION_TYPES.SET_LOADING, payload: true });
        setToolCalling(false);

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000);

        try {
            const response = await fetch('http://localhost:8001/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    message: userMessage,
                    session_id: sessionId,
                }),
                signal: controller.signal,
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                // 尝试读取响应文本而不是直接解析 JSON（防止非 JSON 响应）
                const errorText = await response.text();
                let errorMessage = `请求失败 (${response.status})`;
                try {
                    const errorData = JSON.parse(errorText);
                    errorMessage = errorData.detail || errorMessage;
                } catch {
                    errorMessage = errorText || errorMessage;
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();

            if (data.tool_called) {
                setToolCalling(true);
            }

            dispatch({
                type: ACTION_TYPES.ADD_ASSISTANT_MESSAGE,
                payload: {content: data.reply, tokens: data.usage?.total_tokens || 0}
            });

            console.log(`本次对话消耗token：${data.usage.total_tokens}`);

            if (data.session_id && data.session_id !== sessionId) {
                setSessionId(data.session_id)
            }
            inputRef.current?.focus();
        } catch (err) {
            dispatch({type: ACTION_TYPES.SET_ERROR, payload: err.message});
            if (retryCount === 0 && err.name !== 'AbortError') {
                console.log('自动重试...');
                setRetryCount(1);
                setTimeout(() => sendMessage(1), 2000);
                return;
            }
        } finally {
            dispatch({ type: ACTION_TYPES.SET_LOADING, payload: false });
            setToolCalling(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !isLoading) {
            sendMessage();
        }
    };

    const clearChat = () => {
        dispatch({type: ACTION_TYPES.CLEAR_MESSAGES});
        const newId = crypto.randomUUID();
        setSessionId(newId);
        localStorage.setItem('chat_session_id', newId);
    };

    return (
        <div style={{maxWidth: '600px', margin: '0 auto', padding:'20px', fontFamily: 'sans-serif'}}>
            <h2>🤖 AI 聊天助手（多轮对话）</h2>
            <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <img src={user.avatar} alt='avatar' width='32' style={{ borderRadius: '50%' }} />
                    <span>{user.name}</span>
                </div>
            </div>
            <p style={{fontSize: '14px', color: '#666'}}>
                回话ID: {sessionId.substring(0, 8)}...
                <button onClick={clearChat} style={{marginLeft: '10px', fontSize: '12px'}}>新对话</button>
            </p>

            <div style={{
                height: '400px',
                overflowY: 'auto',
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '16px',
                backgroundColor: '#fafafa',
                marginBottom: '16px'
            }}>
                {messages.length === 0 && (
                    <div style={{textAlign: 'center', color: '#aaa', marginTop: '150px'}}>
                        发送消息开始对话🤗
                    </div>
                )}
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        style={{
                            display: 'flex',
                            justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                            marginBottom: '12px'
                        }}
                    >
                        <div
                        style={{
                            maxWidth: '70%',
                            padding: '10px 14px',
                            borderRadius: '18px',
                            backgroundColor: msg.role === 'user' ? '#007bff' : '#e9ecef',
                            color: msg.role === 'user' ? 'white' : '#333',
                            wordWrap: 'break-word'
                        }}
                        >
                            <strong>{msg.role === 'user' ? '我' : 'AI'}:</strong>{msg.content}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div style={{display: 'flex', justifyContent: 'flex-start', marginBottom: '12px'}}>
                        <div style={{backgroundColor: '#e9ecef', padding: '10px 14px', borderRadius: '18px'}}>
                            {toolCalling ? '正在查询天气' : 'AI正在思考...'}
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {error && (
                <div style={{ color: 'red', fontSize: '14px', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px'}}>
                    <span>错误: {error}</span>
                    <button onClick={() => sendMessage()} style={{fontSize: '12px'}}>重试</button>
                </div>
            )}

            <div style={{ display: 'flex', gap: '8px'}}>
                <input
                    ref={inputRef}
                    type='text'
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    disabled={isLoading}
                    placeholder='输入信息...'
                    style={{flex: 1, padding: '10px', borderRadius: '20px', border: '1px solid #ccc'}}
                />
                <button
                    onClick={sendMessage}
                    disabled={isLoading || inputValue.trim() === ''}
                    style={{padding: '10px 20px', borderRadius: '20px', cursor: 'pointer'}}
                >
                    发送
                </button>
            </div>
        </div>
    );
}

export default Chat;
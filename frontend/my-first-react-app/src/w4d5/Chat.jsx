import { useEffect, useRef, useState } from 'react';

function Chat() {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [toolCalling, setToolCalling] = useState(false);
    const [error, setError] = useState(null);
    const [sessionId, setSessionId] = useState(() => {
        const saved = localStorage.getItem('chat_session_id');
        return saved || crypto.randomUUID();
    });

    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth'});
    }, [messages]);
    useEffect(() => {
        inputRef.current?.focus();
    }, []);
    useEffect(() => {
        localStorage.setItem('chat_session_id', sessionId);
    }, [sessionId]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth'});
    });

    const sendMessage = async () => {
        const userMessage = inputValue.trim();
        if (userMessage === '') return;

        setMessages(prev => [...prev, {role: 'user', content: userMessage}]);
        setInputValue('');
        setIsLoading(true);
        setToolCalling(false);
        setError(null);

        try {
            const response = await fetch('http://localhost:8001/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage, session_id: sessionId}),
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || '请求失败');
            }

            const data = await response.json();

            if (data.session_id && data.session_id !== sessionId) {
                setSessionId(data.session_id);
            }

            setMessages(prev => [...prev, {
                role: 'assistant',
                content: data.reply,
                tokens: data.usage?.total_tokens || 0,
            }]);

            if (data.tool_called) {
                setMessages(prev => [...prev, {
                    role: 'system',
                    content: '🔍 已查询天气信息',
                    isTemporary: true,
                }]);
            }
            setTimeout(() => {
                setMessages(prev => prev.filter(msg => !msg.isTemporary));
            }, 3000);
        } catch (err) {
            console.error('聊天请求失败：', err);
            setError(err.message);
            setMessages(prev => [...prev, {
                role: 'system',
                content: `❌ 发生错误: ${err.message}`,
                isError: true,
            }]);
        } finally {
            setIsLoading(false);
            setToolCalling(false);
            inputRef.current?.focus();
        }
    };

    const totalTokens = messages.reduce((sum, msg) => sum + (msg.tokens || 0), 0);

    return (
        <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
            <h2>🤖 AI 天气助手</h2>
            <div style={{ fontSize: '12px', color: '#666', marginBottom: '10px' }}>
                会话ID：{sessionId.slice(0, 8)}... | 累计Token：{totalTokens}
            </div>

            {/* 消息列表区域 */}
            <div style={{ height: '400px', overflowY: 'auto', border: '1px solid #ddd', borderRadius: '8px', padding: '12px' }}>
                {messages.map((msg, idx) => (
                    <div key={idx} style={{ marginBottom: '12px'}}>
                        <div style={{ display: 'flex', justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start' }}>
                            <div style={{ maxWidth: '70%', padding: '8px 12px', borderRadius: '16px',backgroundColor: msg.role === 'user' ? '#007bff' : '#f1f1f1', color: msg.role === 'user' ? 'white' : 'black'}}>
                                <strong>{msg.role === 'user' ? '我' : msg.role === 'assistant' ? 'AI' : 'ℹ️'}:</strong> {msg.content}
                            </div>
                        </div>
                        {msg.role === 'assistant' && msg.tokens > 0 && (
                            <div style={{ fontSize: '10px', color: '#888', textAlign: 'right', marginTop: '2px' }}>
                                消耗 {msg.tokens} tokens
                            </div>
                        )}
                    </div>
                ))}
                {isLoading && (
                    <div style={{ textAlign: 'center', color: '#666', padding: '8px' }}>
                        🤔 AI 正在思考...
                    </div>
                )}
                <div ref={messagesEndRef} />
                {/* 错误提示 */}
                {error && (
                    <div style={{ color: 'red', marginBottom: '8px', fontSize: '14px' }}>
                        ⚠️ {error}
                    </div>
                )}
            </div>


                {/* 输入区域 */}
                <div style={{ display: 'flex', gap: '8px', marginTop: '10px' }}>
                    <input ref={inputRef} type='text' value={inputValue} onChange={(e) => setInputValue(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && sendMessage()} disabled={isLoading} placeholder='问天气，例如：北京今天天气怎么样？' style={{ flex: 1, padding: '10px', borderRadius: '20px', border: '1px solid #ccc' }}/>
                    <button onClick={sendMessage} disabled={isLoading} style={{ padding: '1px 20px', borderRadius: '20px' }}>
                        发送
                    </button>
                </div>
        </div>
    );
}

export default Chat;
import { useRef, useState } from 'react';

function TimerControl() {
    const [seconds, setSeconds] = useState(0);
    const timerRef = useRef(null);
    const [isRunning, setIsRunning] = useState(false);

    const startTimer = () => {
        if (timerRef.current) return;
        setIsRunning(true);
        timerRef.current = setInterval(() => {
            setSeconds(prev => prev + 1);
        }, 1000);
    };

    const stopTimer = () => {
        if (timerRef.current) {
            clearInterval(timerRef.current);
            timerRef.current = null;
            setIsRunning(false);
        }
    };

    const resetTimer = () => {
        stopTimer();
        setSeconds(0);
    };

    return (
        <div style={{ padding: '20px', border: '1px solid #ccc', marginBottom: '20px'}}>
            <h3>计时器 (useRef 存储定时器ID)</h3>
            <p>已计时: {seconds} 秒</p>
            <button onClick={startTimer} disabled={isRunning}>开始</button>
            <button onClick={stopTimer} disabled={!isRunning}>停止</button>
            <button onClick={resetTimer}>重置</button>
        </div>
    );
}

export default TimerControl;
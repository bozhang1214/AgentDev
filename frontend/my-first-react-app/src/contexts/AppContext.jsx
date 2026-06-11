import { createContext, useContext, useEffect, useReducer } from 'react';

const initialState = {
    theme: 'light',
    sessionId: null,
    user: {name: '访客', avatar: ''},
};

const ACTION = {
    SET_THEME: 'SET_THEME',
    SET_SESSION_ID: 'SET_SESSION_ID',
    SET_USER: 'SET_USER',
};

function appReducer(state, action) {
    switch (action.type) {
        case ACTION.SET_THEME:
            return {...state, theme: action.payload};
        case ACTION.SET_SESSION_ID:
            return {...state, sessionId: action.payload};
        case ACTION.SET_USER:
            return {...state, user: action.payload};
        default:
            return state;
    }
}

const AppContext = createContext();

export function AppProvider({ children }) {
    const [state, dispatch] = useReducer(appReducer, initialState);

    useEffect(() => {
        const savedSession = localStorage.getItem('chat_session_id');
        if (savedSession && !state.sessionId) {
            dispatch({type: ACTION.SET_SESSION_ID, payload: savedSession});
        } else if (!state.sessionId) {
            const newId = crypto.randomUUID();
            dispatch({type:ACTION.SET_SESSION_ID, payload: newId});
            localStorage.setItem('chat_session_id', newId);
        }
    }, []);

    useEffect(() => {
        if (state.sessionId) {
            localStorage.setItem('chat_session_id', state.sessionId);
        }
    }, [state.sessionId]);

    return (
        <AppContext.Provider value={{state, dispatch}}>
            {children}
        </AppContext.Provider>
    );
}

export function useApp() {
    const context = useContext(AppContext);
    if (!context) throw new Error('useApp must be used within AppProvider');
    return context;
}

export { ACTION };

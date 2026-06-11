export const initialMessageState = {
    messages: [],
    isLoading: false,
    error: null,
};

export const ACTION_TYPES = {
    ADD_USER_MESSAGE: 'ADD_USER_MESSAGE',
    ADD_ASSISTANT_MESSAGE: 'ADD_ASSISTANT_MESSAGE',
    SET_LOADING: 'SET_LOADING',
    SET_ERROR: 'SET_ERROR',
    CLEAR_MESSAGES: 'CLEAR_MESSAGES',
};

export function messageReducer(state, action) {
    switch (action.type) {
        case ACTION_TYPES.ADD_USER_MESSAGE:
            return {
                ...state,
                messages: [...state.messages, { role: 'user', content: action.payload, tokens: 0 }],
            };
        case ACTION_TYPES.ADD_ASSISTANT_MESSAGE:
            return {
                ...state,
                messages: [...state.messages, {role: 'assistant', content: action.payload.content, tokens: action.payload.tokens}],
                isLoading: false,
            };
        case ACTION_TYPES.SET_LOADING:
            return {...state, isLoading: action.payload};
        case ACTION_TYPES.SET_ERROR:
            return {...state, error: action.payload, isLoading: false};
        case ACTION_TYPES.CLEAR_MESSAGES:
            return {...state, messages: []};
        default:
            return state;
    }
}


import { createContext, useContext, useState } from 'react';

const TodoFilterContext = createContext();

export function TodoFilterProvider({ children }) {
    const [filter, setFilter] = useState('all');

    return (
        <TodoFilterContext.Provider value={{ filter, setFilter }}>
            {children}
        </TodoFilterContext.Provider>
    );
}

export function useTodoFilter() {
    const context = useContext(TodoFilterContext);
    if (!context) throw new Error('useTodoFilter must be used within TodoFilterProvider');
    return context;
}
import { createContext, useContext, useState } from 'react';

const UserContext = createContext();

export function UserProvider({ children }) {
    const [user, setUser] = useState({
        name: '张三',
        avatar: 'https://randomuser.me/api/portraits/men/1.jpg',
        isLoggedIn: true
    });

    const login = (userInfo) => setUser({...userInfo, isLoggedIn: true});
    const logout = () => setUser({name: '', isLoggedIn: false});

    return (
        <UserContext.Provider value={{ user, login, logout }}>
            {children}
        </UserContext.Provider>
    );
}

export function useUser() {
    const context = useContext(UserContext);
    if (!context) throw new Error('useUser must be used within UserProvider');
    return context;
}
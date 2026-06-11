import { BrowserRouter, Route, Routes } from 'react-router';
import Chat from '../../Chat';
import { AppProvider } from '../../contexts/AppContext';
import { UserProvider } from '../../contexts/UserContext';
import Home from '../day1/Home';
import Layout from '../day1/Layout';
import Settings from '../day1/Settings';

function App() {
    return (
        <AppProvider>
            <UserProvider>
                <BrowserRouter>
                    <Routes>
                        <Route element={<Layout />}>
                            <Route path="/" element={<Home />} />
                            <Route path="/chat" element={<Chat />} />
                            <Route path="/settings" element={<Settings />} />
                        </Route>
                    </Routes>
                </BrowserRouter>
            </UserProvider>
        </AppProvider>
    );
}

export default App;
import React, { useEffect, useState } from 'react';
import WebApp from '@twa-dev/sdk';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import AdminPrices from './pages/Admin/Prices';
import AdminInventory from './pages/Admin/Inventory';
import AdminServers from './pages/Admin/Servers';
import AdminBroadcast from './pages/Admin/Broadcast';
import SellToShop from './pages/SellToShop';
import { supabase } from './services/supabase';
import './styles/theme.css';

function App() {
  const [userRole, setUserRole] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    WebApp.ready();
    WebApp.expand();
    
    const initUser = async () => {
      const telegramUser = WebApp.initDataUnsafe?.user;
      
      if (telegramUser) {
        const { data } = await supabase
          .from('users')
          .select('role')
          .eq('telegram_id', telegramUser.id)
          .single();
        
        setUserRole(data?.role || 'user');
      }
      
      setLoading(false);
    };
    
    initUser();
  }, []);

  if (loading) {
    return <div className="container">Загрузка...</div>;
  }

  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <div className="container">
            <h1 style={{ color: 'var(--primary-orange)' }}>🛍 Crash Shop</h1>
            <p style={{ color: 'var(--text-secondary)' }}>
              Radmir Online • Amazing Online (CR-MP)
            </p>
          </div>
        </header>
        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/sell" element={<SellToShop />} />
          
          {userRole === 'admin' && (
            <>
              <Route path="/admin/prices" element={<AdminPrices />} />
              <Route path="/admin/inventory" element={<AdminInventory />} />
              <Route path="/admin/servers" element={<AdminServers />} />
              <Route path="/admin/broadcast" element={<AdminBroadcast />} />
            </>
          )}
          
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
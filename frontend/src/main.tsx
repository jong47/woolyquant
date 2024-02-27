import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider
} from 'react-router-dom';
import App from './App.tsx';
import './index.css';
import Login from './routes/login';
import Dashboard from './routes/dashboard';
import Marketplace from './routes/marketplace';
import TradingBot from './routes/tradingbot';
import About from './routes/about';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />
  },
  {
    path: '/trading/bot',
    element: <TradingBot />
  },
  {
    path: '/dashboard',
    element: <Dashboard />
  },
  {
    path: '/account/login',
    element: <Login />
  },
  {
    path: '/marketplace',
    element: <Marketplace />
  },
  {
    path: '/about',
    element: <About />
  }
]);

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>,
)

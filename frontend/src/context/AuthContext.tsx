import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { api } from '@/api/client';

interface User {
  sub: string;
  roles: string[];
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: () => void;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
  hasRole: (role: string) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const checkAuth = async () => {
    try {
      const data = await api.get<User>('/auth/me');
      setUser(data);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = () => {
    window.location.href = '/api/auth/login';
  };

  const logout = async () => {
    try {
      await api.post('/auth/logout', {});
    } finally {
      setUser(null);
      window.location.href = '/';
    }
  };

  const hasRole = (role: string) => {
    return user?.roles.includes(role) ?? false;
  };

  useEffect(() => {
    checkAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, checkAuth, hasRole }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

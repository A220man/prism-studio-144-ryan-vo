import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';

export function Callback() {
  const navigate = useNavigate();
  const { checkAuth } = useAuth();

  useEffect(() => {
    // The backend handles the callback and sets cookies, then redirects to /
    // This component is a fallback in case the redirect doesn't happen
    const params = new URLSearchParams(window.location.search);
    const error = params.get('error');
    const errorDescription = params.get('error_description');

    if (error) {
      console.error('OAuth error:', error, errorDescription);
      // Redirect to home with error
      navigate('/?error=' + encodeURIComponent(errorDescription || error));
    } else {
      // No error, verify auth state then redirect to home
      checkAuth().then(() => {
        navigate('/');
      });
    }
  }, [navigate, checkAuth]);

  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '300px' }}>
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>⏳</div>
        <p>Completing sign in...</p>
      </div>
    </div>
  );
}

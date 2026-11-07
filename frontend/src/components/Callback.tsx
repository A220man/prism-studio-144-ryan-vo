import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export function Callback() {
  const navigate = useNavigate();

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
      // No error, redirect to home
      navigate('/');
    }
  }, [navigate]);

  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '300px' }}>
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>⏳</div>
        <p>Completing sign in...</p>
      </div>
    </div>
  );
}

import './Login.css';

function Login() {
    return (
        <div className="login-container">
            <div className="login-box">
                <div className="logo-section">
                    <div className="logo-icon">L</div>
                    <h1>LACCIS</h1>
                    <p>Legal Clause Classification Intelligence System</p>
                </div>

                <div className="login-card">
                    <p style={{ textAlign: 'center', fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.75rem' }}>
                        This tool uses the shared NIFO session only.
                    </p>
                    <div className="alert alert-error" style={{ marginBottom: '1rem' }}>
                        <span>!</span>
                        <span>Please launch Legal Analyzer from NIFO so the shared JWT is available here.</span>
                    </div>
                    <button type="button" className="btn-login" onClick={() => { window.location.href = '/'; }}>
                        <span>Open NIFO</span>
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Login;

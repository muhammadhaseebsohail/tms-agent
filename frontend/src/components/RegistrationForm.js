Sure, I'll create the three functional components: RegistrationForm, LoginForm, and LogoutButton. 

Let's start with the Registration Form:

```jsx
// RegistrationForm.jsx
import React, { useState } from 'react';
import PropTypes from 'prop-types';

const RegistrationForm = ({ onRegister }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();

        if (!username || !password) {
            // handle validation error here
            console.error('All fields are required');
            return;
        }

        onRegister({ username, password });
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Username:
                <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
            </label>
            <label>
                Password:
                <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
            </label>
            <button type="submit">Register</button>
        </form>
    );
};

RegistrationForm.propTypes = {
    onRegister: PropTypes.func.isRequired,
};

export default RegistrationForm;
```

Next, the Login Form:

```jsx
// LoginForm.jsx
import React, { useState } from 'react';
import PropTypes from 'prop-types';

const LoginForm = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();

        if (!username || !password) {
            // handle validation error here
            console.error('All fields are required');
            return;
        }

        onLogin({ username, password });
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Username:
                <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
            </label>
            <label>
                Password:
                <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
            </label>
            <button type="submit">Login</button>
        </form>
    );
};

LoginForm.propTypes = {
    onLogin: PropTypes.func.isRequired,
};

export default LoginForm;
```

And finally, the Logout Button:

```jsx
// LogoutButton.jsx
import React from 'react';
import PropTypes from 'prop-types';

const LogoutButton = ({ onLogout }) => (
    <button type="button" onClick={onLogout}>Logout</button>
);

LogoutButton.propTypes = {
    onLogout: PropTypes.func.isRequired,
};

export default LogoutButton;
```

For the CSS, here's a simple example:

```css
/* styles.css */
form {
    display: flex;
    flex-direction: column;
    width: 200px;
    margin: auto;
}

label {
    margin-bottom: 10px;
}

button {
    width: 100%;
}
```

And finally, here's a basic setup for unit testing these components:

```jsx
// RegistrationForm.test.jsx
import { render, fireEvent } from '@testing-library/react';
import RegistrationForm from './RegistrationForm';

test('calls onRegister with the username and password when submitted', () => {
    const handleRegister = jest.fn();
    const { getByLabelText, getByText } = render(<RegistrationForm onRegister={handleRegister} />);

    fireEvent.change(getByLabelText(/username/i), { target: { value: 'testUser' } });
    fireEvent.change(getByLabelText(/password/i), { target: { value: 'testPass' } });
    fireEvent.click(getByText(/register/i));

    expect(handleRegister).toHaveBeenCalledWith({ username: 'testUser', password: 'testPass' });
});
```
Sure, here are the test setups for the remaining two components:

```jsx
// LoginForm.test.jsx
import { render, fireEvent } from '@testing-library/react';
import LoginForm from './LoginForm';

test('calls onLogin with the username and password when submitted', () => {
    const handleLogin = jest.fn();
    const { getByLabelText, getByText } = render(<LoginForm onLogin={handleLogin} />);

    fireEvent.change(getByLabelText(/username/i), { target: { value: 'testUser' } });
    fireEvent.change(getByLabelText(/password/i), { target: { value: 'testPass' } });
    fireEvent.click(getByText(/login/i));

    expect(handleLogin).toHaveBeenCalledWith({ username: 'testUser', password: 'testPass' });
});
```

```jsx
// LogoutButton.test.jsx
import { render, fireEvent } from '@testing-library/react';
import LogoutButton from './LogoutButton';

test('calls onLogout when clicked', () => {
    const handleLogout = jest.fn();
    const { getByText } = render(<LogoutButton onLogout={handleLogout} />);
    
    fireEvent.click(getByText(/logout/i));

    expect(handleLogout).toHaveBeenCalled();
});
```

These tests ensure that the components' main functionalities work as expected. For the RegistrationForm and LoginForm, it checks whether the provided `onRegister` and `onLogin` props are called with the right values when the form is submitted. For the LogoutButton, it simply checks if the provided `onLogout` prop is called when the button is clicked.
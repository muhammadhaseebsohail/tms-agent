The Jest and React Testing Library setup has already been provided in the request. However, let's add more test cases to cover loading and error states, and rendering of comments:

```jsx
import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import Comments from './Comments';

// Test to check loading state
test('displays loading state', () => {
  const fetchComments = jest.fn().mockReturnValue(new Promise(() => {}));
  render(<Comments fetchComments={fetchComments} submitComment={jest.fn()} />);
  expect(screen.getByText('Loading comments...')).toBeInTheDocument();
});

// Test to check error state
test('displays error state', async () => {
  const mockError = { message: 'An error occurred' };
  const fetchComments = jest.fn().mockRejectedValueOnce(mockError);
  render(<Comments fetchComments={fetchComments} submitComment={jest.fn()} />);
  await waitFor(() => expect(screen.getByText(`Error loading comments: ${mockError.message}`)).toBeInTheDocument());
});

// Test to check rendering of comments
test('displays comments', () => {
  const mockComments = [{ id: '1', text: 'Test comment 1' }, { id: '2', text: 'Test comment 2' }];
  const fetchComments = jest.fn().mockResolvedValueOnce(mockComments);
  render(<Comments fetchComments={fetchComments} submitComment={jest.fn()} />);
  mockComments.forEach((comment) => {
    expect(screen.getByText(comment.text)).toBeInTheDocument();
  });
});

// Test to check submission of a new comment
test('allows for new comments to be submitted', async () => {
  const fetchComments = jest.fn().mockResolvedValueOnce([]);
  const submitComment = jest.fn();

  const { getByPlaceholderText, getByText } = render(
    <Comments fetchComments={fetchComments} submitComment={submitComment} />
  );

  // Simulate user typing a comment
  fireEvent.change(getByPlaceholderText('Add a comment'), {
    target: { value: 'New comment' },
  });
  fireEvent.click(getByText('Submit'));

  // Wait for mock submit function to be called
  await waitFor(() => expect(submitComment).toHaveBeenCalledWith('New comment'));
});
```

In these tests, we use Jest's `mockReturnValue`, `mockRejectedValueOnce`, and `mockResolvedValueOnce` to control the behavior of the `fetchComments` function, and then check that the component behaves correctly in each case.
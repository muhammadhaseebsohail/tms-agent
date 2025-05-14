Here's a basic implementation of a Comments UI component in React. The component includes an input for creating comments, and a list of existing comments to display. It also includes loading and error states.

```jsx
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import './Comments.css';

/**
 * Comments UI Component
 * @param {Object} props - Component props
 * @param {Array} props.comments - Array of comments to display
 * @param {Function} props.fetchComments - Function to fetch comments
 * @param {Function} props.submitComment - Function to submit a new comment
 */
const Comments = ({ comments = [], fetchComments, submitComment }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [commentInput, setCommentInput] = useState('');

  useEffect(() => {
    setLoading(true);
    fetchComments()
      .then(() => setLoading(false))
      .catch((err) => {
        setLoading(false);
        setError(err);
      });
  }, [fetchComments]);

  const handleCommentSubmit = () => {
    submitComment(commentInput);
    setCommentInput('');
  };

  if (loading) return <p>Loading comments...</p>;
  if (error) return <p>Error loading comments: {error.message}</p>;

  return (
    <div className="comments">
      <input
        className="comments__input"
        value={commentInput}
        onChange={(e) => setCommentInput(e.target.value)}
        placeholder="Add a comment"
      />
      <button className="comments__submit" onClick={handleCommentSubmit}>
        Submit
      </button>
      <ul className="comments__list">
        {comments.map((comment) => (
          <li key={comment.id} className="comments__item">
            {comment.text}
          </li>
        ))}
      </ul>
    </div>
  );
};

Comments.propTypes = {
  comments: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      text: PropTypes.string.isRequired,
    })
  ),
  fetchComments: PropTypes.func.isRequired,
  submitComment: PropTypes.func.isRequired,
};
export default Comments;
```

Here's the associated CSS module:

```css
/* Comments.css */
.comments {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.comments__input {
  width: 80%;
  margin-bottom: 10px;
  padding: 5px;
}

.comments__submit {
  margin-bottom: 10px;
  padding: 5px;
}

.comments__list {
  width: 80%;
  list-style: none;
  padding: 0;
}

.comments__item {
  margin-bottom: 10px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
}
```

Finally, here's a simple unit test setup using Jest and React Testing Library:

```jsx
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import Comments from './Comments';

test('renders comments and allows for new comments to be submitted', async () => {
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
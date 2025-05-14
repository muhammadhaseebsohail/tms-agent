Here's a simple example of a Task Tracker component in React using functional components and hooks.

```jsx
import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './TaskTracker.css';

// Task Component
const Task = ({ task, onToggle }) => {
  const [status, setStatus] = useState(task.status);
  
  const handleChange = () => {
    setStatus(!status);
    onToggle(task.id);
  }

  return (
    <div className={`task ${status ? 'done' : ''}`} onClick={handleChange}>
      {task.name}
    </div>
  );
}

Task.propTypes = {
  task: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    status: PropTypes.bool.isRequired,
  }).isRequired,
  onToggle: PropTypes.func.isRequired,
};

// Task Tracker Component
const TaskTracker = ({ tasks }) => {
  const [taskList, setTaskList] = useState(tasks);

  const handleToggle = id => {
    const updatedTasks = taskList.map(task =>
      task.id === id ? { ...task, status: !task.status } : task,
    );
    setTaskList(updatedTasks);
  };

  return (
    <div className="task-tracker">
      {taskList.map(task => (
        <Task key={task.id} task={task} onToggle={handleToggle} />
      ))}
    </div>
  );
};

TaskTracker.propTypes = {
  tasks: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
      status: PropTypes.bool.isRequired,
    }),
  ).isRequired,
};

export default TaskTracker;
```
In this code, we have two components: `Task` and `TaskTracker`. The `Task` component represents an individual task. It has a `status` state, which is toggled when the task component is clicked. The `TaskTracker` component is a list of `Task` components. It contains a `handleToggle` function that updates the status of a task when it is clicked.

This is the CSS module for the component:

```css
/* TaskTracker.css */
.task-tracker {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task {
  padding: 20px;
  border: 1px solid #000;
  cursor: pointer;
}

.task.done {
  text-decoration: line-through;
}
```

Here is a simple unit test setup for the TaskTracker component:

```jsx
import { render, fireEvent } from '@testing-library/react';
import TaskTracker from './TaskTracker';

test('toggles task status on click', () => {
  const tasks = [
    { id: 1, name: 'Test task', status: false },
  ];
  const { getByText } = render(<TaskTracker tasks={tasks} />);
  
  fireEvent.click(getByText('Test task'));
  
  expect(getByText('Test task')).toHaveClass('done');
});
```
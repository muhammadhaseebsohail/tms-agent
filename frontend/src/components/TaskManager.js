Here is a basic example of how you might structure this in React:

```jsx
import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './TaskManager.css';

const TaskManager = ({ tasks, onTaskCreate, onTaskEdit, onTaskDelete, onTaskAssign }) => {
  const [taskName, setTaskName] = useState('');
  const [taskEdit, setTaskEdit] = useState('');

  const handleTaskCreate = () => {
    onTaskCreate(taskName);
    setTaskName('');
  };

  const handleTaskEdit = (taskId, name) => {
    setTaskEdit(taskId);
    onTaskEdit(taskId, name);
  };

  const handleTaskDelete = (taskId) => {
    onTaskDelete(taskId);
  };

  const handleTaskAssign = (taskId, userId) => {
    onTaskAssign(taskId, userId);
  };

  return (
    <div className="task-manager">
      <input value={taskName} onChange={e => setTaskName(e.target.value)} />
      <button onClick={handleTaskCreate}>Create task</button>
      {tasks.map(task => (
        <div key={task.id} className="task">
          <input 
            value={task.name} 
            onChange={e => handleTaskEdit(task.id, e.target.value)}
            onBlur={() => setTaskEdit('')}
            disabled={taskEdit !== task.id}
          />
          <button onClick={() => handleTaskDelete(task.id)}>Delete</button>
          <button onClick={() => handleTaskAssign(task.id, task.userId)}>Assign</button>
        </div>
      ))}
    </div>
  );
};

TaskManager.propTypes = {
  tasks: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    userId: PropTypes.string
  })).isRequired,
  onTaskCreate: PropTypes.func.isRequired,
  onTaskEdit: PropTypes.func.isRequired,
  onTaskDelete: PropTypes.func.isRequired,
  onTaskAssign: PropTypes.func.isRequired
};

export default TaskManager;
```

Your `TaskManager.css` might look something like this:

```css
.task-manager {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task {
  display: flex;
  gap: 5px;
}
```

And a basic unit test setup might look like this:

```jsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import TaskManager from './TaskManager';

test('handles task creation', () => {
  const handleTaskCreate = jest.fn();
  const { getByText, getByPlaceholderText } = render(
    <TaskManager tasks={[]} onTaskCreate={handleTaskCreate} />
  );

  fireEvent.change(getByPlaceholderText('New task'), { target: { value: 'Test task' } });
  fireEvent.click(getByText('Create task'));

  expect(handleTaskCreate).toHaveBeenCalledWith('Test task');
});
```
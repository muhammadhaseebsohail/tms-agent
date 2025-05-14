Here's the complete unit test setup for both `Task` and `TaskTracker` components:

```jsx
import { render, fireEvent } from '@testing-library/react';
import Task from './Task';
import TaskTracker from './TaskTracker';

// Testing Task component
describe('Task', () => {
  const mockToggle = jest.fn();
  const task = { id: 1, name: 'Test task', status: false };

  it('renders task name', () => {
    const { getByText } = render(<Task task={task} onToggle={mockToggle} />);
    expect(getByText(task.name)).toBeInTheDocument();
  });

  it('toggles task status on click', () => {
    const { getByText } = render(<Task task={task} onToggle={mockToggle} />);

    fireEvent.click(getByText(task.name));

    expect(mockToggle).toBeCalledWith(task.id);
  });
});

// Testing TaskTracker component
describe('TaskTracker', () => {
  const tasks = [
    { id: 1, name: 'Test task 1', status: false },
    { id: 2, name: 'Test task 2', status: false },
  ];

  it('renders all tasks', () => {
    const { getByText } = render(<TaskTracker tasks={tasks} />);
    tasks.forEach(task => {
      expect(getByText(task.name)).toBeInTheDocument();
    });
  });

  it('toggles task status on click', () => {
    const { getByText } = render(<TaskTracker tasks={tasks} />);
    const taskToClick = tasks[0];

    fireEvent.click(getByText(taskToClick.name));

    expect(getByText(taskToClick.name)).toHaveClass('done');
  });
});
```

These tests will confirm that the Task component is rendered correctly and its `status` is updated when clicked. For the TaskTracker component, the tests will ensure that all tasks are rendered and that the status of a task can be toggled when clicked.
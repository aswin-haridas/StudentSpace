const form = document.querySelector('form');
    const input = document.querySelector('#new-task');
    const todoList = document.querySelector('#todo-list');

    form.addEventListener('submit', (event) => {
      event.preventDefault();

      const taskName = input.value.trim();

      if (taskName) {
        const newTask = document.createElement('li');
        newTask.innerHTML = `
          <input type="checkbox" id="task${todoList.children.length + 1}" name="task${todoList.children.length + 1}">
          <label for="task${todoList.children.length + 1}">${taskName}</label>
          <button class="delete-btn">Delete</button>
        `;
        todoList.appendChild(newTask);
        input.value = '';
      }
    });

    todoList.addEventListener('click', (event) => {
      if (event.target.matches('.delete-btn')) {
        event.target.parentNode.remove();
      }
    });
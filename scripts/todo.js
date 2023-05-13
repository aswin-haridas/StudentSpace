let todoList = [];
function addTodo() {
	let todoInput = document.getElementById("todo-input");
	let todoListContainer = document.getElementById("todo-list");
	if (todoInput.value !== "") {
		// add the todo to the array
		todoList.push(todoInput.value);
		// clear the input field
		todoInput.value = "";
		// update the list of todos
		updateTodoList(todoListContainer);
	}
}

function removeTodo(index) {
	// remove the todo at the specified index
	todoList.splice(index, 1);

	// update the list of todos
	let todoListContainer = document.getElementById("todo-list");
	updateTodoList(todoListContainer);
}

function updateTodoList(container) {
	// clear the current list
	container.innerHTML = "";

	// add each todo to the list
	todoList.forEach(function(todo, index) {
		let li = document.createElement("li");
		li.innerHTML = todo;
		li.setAttribute("onclick", `removeTodo(${index})`);
		container.appendChild(li);
	});
}

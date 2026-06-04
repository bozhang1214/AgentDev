(function() {
    const taskInput = document.getElementById('taskInput');
    const addBtn = document.getElementById('addBtn');
    const taskList = document.getElementById('taskList');
    const totalCountSpan = document.getElementById('totalCount');
    const activeCountSpan = document.getElementById('activeCount');
    const completedCountSpan = document.getElementById('completedCount');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const clearCompletedBtn = document.getElementById('clearCompletedBtn');

    let tasks = [];
    let filterType = 'all';

    function generateId() {
        return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    function updateStats() {
        const total = tasks.length;
        const active = tasks.filter(task => !task.completed).length;
        const completed = tasks.filter(task => task.completed).length;
        totalCountSpan.textContent = String(total);
        activeCountSpan.textContent = String(active);
        completedCountSpan.textContent = String(completed);
    }

    function getFilteredTasks() {
        if (filterType === 'active') {
            return tasks.filter(task => !task.completed);
        } else if (filterType === 'completed') {
            return tasks.filter(task => task.completed);
        } else {
            return [...tasks];
        }
    }

    function startEdit(tastElement, taskId) {
        const textSpan = tastElement.querySelector('.task-text');
        const originalText = textSpan.textContent;

        const input = document.createElement('input');
        input.type = 'text';
        input.value = originalText;
        input.className = 'edit-input';

        textSpan.style.display = 'none';
        textSpan.parentNode.insertBefore(input, textSpan);
        input.focus();

        const finishEdit = () => {
            const newText = input.value.trim();
            if (newText !== '') {
                const task = tasks.find(t => t.id === taskId);
                if (task) task.text = newText;
                saveToLocalStorage();
            }
            input.remove();
            textSpan.style.display = '';
            renderTasks();
        };

        input.addEventListener('blur', finishEdit);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                finishEdit();
            }
        });
    }

    function saveToLocalStorage() {
        try {
            localStorage.setItem('todo_tasks', JSON.stringify(tasks));
        } catch (error) {
            console.error('Failed to save tasks:', error);
            showToast('保存失败，请检查存储权限', 'error');
        }
    }

    function loadFromLocalStorage() {
        try {
            const stored = localStorage.getItem('todo_tasks');
            if (stored) {
                const parsed = JSON.parse(stored);
                if (Array.isArray(parsed)) {
                    tasks = parsed;
                } else {
                    throw new Error('Invalid data format');
                }
            } else {
                tasks = [
                    {id: generateId(), text: '学习 JavaScript 基础', completed: true},
                    {id: generateId(), text: '完成代办应用项目', completed: false},
                    {id: generateId(), text: '阅读《网页设计与制作》', completed: false}
                ];
            }
        } catch (error) {
            console.error('Failed to load tasks:', error);
            tasks = [];
            localStorage.removeItem('todo_tasks');
        }
        renderTasks();
    }

    function createTaskElement(task) {
        const li = document.createElement('li');
        li.className = `task-item ${task.completed ? 'completed' : ''}`;
        li.dataset.id = task.id;

        const textSpan = document.createElement('span');
        textSpan.className = 'task-text';
        textSpan.textContent = task.text;
        textSpan.addEventListener('click', () => toggleTask(task.id));

        const delBtn = document.createElement('button');
        delBtn.className = 'delete-btn';
        delBtn.textContent = '🗑️';
        delBtn.setAttribute('aria-label', '删除任务');
        delBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            deleteTask(task.id);
        });

        li.appendChild(textSpan);
        li.appendChild(delBtn);
        return li;
    }

    function renderTasks() {
        if (!taskList) return;
        taskList.innerHTML = '';
        const filtered = getFilteredTasks();

        if (filtered.length === 0) {
            const emptyLi = document.createElement('li');
            emptyLi.className = 'empty-message';
            emptyLi.textContent = filterType === 'all' ? '✨ 暂无任务，添加一条吧！' : (filterType === 'active' ? '✅ 所有任务都已完成！' : '📭 还没有已完成的任务');
            taskList.appendChild(emptyLi);
        } else {
            filtered.forEach(task => {
                const li = document.createElement('li');
                li.className = `task-item ${task.completed ? 'completed' : ''}`;
                li.dataset.id = task.id;

                const textSpan = document.createElement('span');
                textSpan.className = 'task-text';
                textSpan.textContent = task.text;
                textSpan.addEventListener('click', (e) => {
                    e.stopPropagation();
                    toggleTask(task.id);
                });
                textSpan.addEventListener('dblclick', (e) => {
                    e.stopPropagation();
                    startEdit(li, task.id);
                });

                const delBtn = document.createElement('button');
                delBtn.className = 'delete-btn';
                delBtn.textContent = '🗑️';
                delBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    deleteTask(task.id);
                });
                li.appendChild(textSpan);
                li.appendChild(delBtn);
                taskList.appendChild(li);
            });
        }
        updateStats();
    }

    function showToast(message, type = 'info') {
        let toast = document.querySelector('.toast');
        if (toast) {
            toast.remove();
        }
        
        toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        requestAnimationFrame(() => {
            toast.classList.add('show');
        });
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 2000);
    }

    function addTask() {
        const text = taskInput.value.trim();
        if (text === '') {
            showToast('请填写任务内容', 'error');
            return;
        }
        
        const newTask = {
            id: generateId(),
            text: text,
            completed: false
        };
        tasks.push(newTask);
        saveToLocalStorage();
        
        if (tasks.length === 1) {
            renderTasks();
        } else {
            const li = createTaskElement(newTask);
            taskList.insertBefore(li, taskList.firstChild);
            updateStats();
        }
        
        taskInput.value = '';
        taskInput.focus();
        showToast('任务添加成功', 'success');
    }

    function deleteTask(id) {
        const index = tasks.findIndex(task => task.id === id);
        if (index !== -1) {
            tasks.splice(index, 1);
            saveToLocalStorage();
            
            const li = taskList.querySelector(`[data-id="${id}"]`);
            if (li) {
                li.classList.add('removing');
                setTimeout(() => {
                    li.remove();
                    if (tasks.length === 0) {
                        renderTasks();
                    } else {
                        updateStats();
                    }
                }, 300);
            }
            showToast('任务已删除', 'info');
        }
    }

    function toggleTask(id) {
        const task = tasks.find(task => task.id === id);
        if (task) {
            task.completed = !task.completed;
            saveToLocalStorage();
            
            const li = taskList.querySelector(`[data-id="${id}"]`);
            if (li) {
                li.classList.toggle('completed');
            }
            updateStats();
        }
    }

    function clearCompleted() {
        tasks = tasks.filter(task => !task.completed);
        saveToLocalStorage();
        renderTasks();
    }

    function setFilter(type) {
        filterType = type;
        filterBtns.forEach(btn => {
            if (btn.dataset.filter === type) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        renderTasks();
    }

    function bindEvents() {
        addBtn.addEventListener('click', addTask);
        taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                addTask();
            }
        });
        clearCompletedBtn.addEventListener('click', clearCompleted);
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                setFilter(btn.dataset.filter);
            });
        });
    }

    function init() {
        loadFromLocalStorage();
        bindEvents();
        setFilter('all');
        renderTasks();
    }

    init();
})();
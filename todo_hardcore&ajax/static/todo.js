var timeString = function (timestamp) {
    t = new Date(timestamp * 1000)
    t = t.toLocaleTimeString()
    return t
}

var todoTemplate = function (todo) {
    var task = todo.task
    var id = todo.id
    var ut = timeString(todo.ut)
    // data-xx 是自定义标签属性的语法
    // 通过这样的方式可以给任意标签添加任意属性
    // 假设 d 是 这个 div 的引用
    // 这样的自定义属性通过  d.dataset.xx 来获取
    // 在这个例子里面, 是 d.dataset.id
    var t = `
        <div class="todo-cell" id='todo-${id}' data-id="${id}">
            <button class="todo-edit">编辑</button>
            <button class="todo-delete">删除</button>
            <span class='todo-task'>${task}</span>
            <time class='todo-ut'>${ut}</time>
        </div>
    `
    return t
}

var insertTodo = function (todo) {
    var todoCell = todoTemplate(todo)
    // 插入 todo-list
    var todoList = e('.todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

var insertEditForm = function (cell) {
    var form = `
        <div class='todo-edit-form'>
            <input class="todo-edit-input">
            <button class='todo-update'>更新</button>
        </div>
    `
    cell.insertAdjacentHTML('beforeend', form)
}

var loadTodos = function () {
    // 调用 ajax api 来载入数据
    apiTodoAll(function (r) {
        // console.log('load all', r)
        // 解析为 数组
        var todos = JSON.parse(r)
        // 循环添加到页面中
        for (var i = 0; i < todos.length; i++) {
            var todo = todos[i]
            insertTodo(todo)
        }
    })
}

var bindEventTodoAdd = function () {
    var b = e('#id-button-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function () {
        var input = e('#id-input-todo')
        var task = input.value
        log('click add', task)
        var form = {
            'task': task,
        }
        apiTodoAdd(form, function (r) {
            // 收到返回的数据, 插入到页面中
            var todo = JSON.parse(r)
            insertTodo(todo)
        })
    })
}

var bindEventTodoDelete = function () {
    var todoList = e('.todo-list')
    // 注意, 第二个参数可以直接给出定义函数
    todoList.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('todo-delete')) {
            // 删除这个 todo
            var todoCell = self.parentElement
            var todo_id = todoCell.dataset.id
            apiTodoDelete(todo_id, function (r) {
                log('删除成功', todo_id)
                todoCell.remove()
            })
        }
    })
}

var bindEventTodoEdit = function () {
    var todoList = e('.todo-list')
    // 注意, 第二个参数可以直接给出定义函数
    todoList.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('todo-edit')) {
            // 删除这个 todo
            var todoCell = self.parentElement
            insertEditForm(todoCell)
        }
    })
}


var bindEventTodoUpdate = function () {
    var todoList = e('.todo-list')
    // 注意, 第二个参数可以直接给出定义函数
    todoList.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('todo-update')) {
            log('点击了 update ')
            //
            var editForm = self.parentElement
            // querySelector 是 DOM 元素的方法
            // document.querySelector 中的 document 是所有元素的父元素
            var input = editForm.querySelector('.todo-edit-input')
            var task = input.value
            // 用 closest 方法可以找到最近的直系父节点
            var todoCell = self.closest('.todo-cell')
            var todo_id = todoCell.dataset.id
            var form = {
                'id': todo_id,
                'task': task,
            }
            apiTodoUpdate(form, function (r) {
                log('更新成功', todo_id)
                var todo = JSON.parse(r)
                var selector = '#todo-' + todo.id
                var todoCell = e(selector)
                var taskSpan = todoCell.querySelector('.todo-task')
                taskSpan.innerHTML = todo.task
//                todoCell.remove()
            })
        }
    })
}

var bindEvents = function () {
    bindEventTodoAdd()
    bindEventTodoDelete()
    bindEventTodoEdit()
    bindEventTodoUpdate()
}

var __main = function () {
    bindEvents()
    loadTodos()
}

__main()

const canvas = document.getElementById("state"); // id of canvas must be state
const ctx = canvas.getContext("2d");
var paused = true;
var fps = 20;

// initialize canvas size
canvas.width = 0.8 * window.innerWidth;
canvas.height = canvas.width / 2;

// set default git
var col_count = 10
var row_count = col_count / 2;
var grid_spacing = canvas.width / col_count
// initial empty grid
var initial_state = Array(row_count).fill(null)
    .map(() => new Array(col_count).fill(null)
        .map(() => 0));
        
width_height();
current_state = JSON.parse(JSON.stringify(initial_state));
render();


// Event listeners
document.getElementById("expand").addEventListener("click", function (e) {
    current_state.push(Array(col_count).fill(0))
    initial_state.push(Array(col_count).fill(0))

    col_count += 2;
    row_count += 1;

    for (let row = 0; row < row_count; row++) {
        current_state[row].push(0);
        current_state[row].push(0);
        initial_state[row].push(0);
        initial_state[row].push(0);
    }

    width_height();
    render();
});
document.getElementById("cut").addEventListener("click", function (e) {
    col_count -= 2;
    row_count -= 1;
    initial_state.pop();
    current_state.pop();
    for (let row = 0; row < row_count; row++) {
        initial_state[row].pop();
        initial_state[row].pop();
        current_state[row].pop();
        current_state[row].pop();
    }
    width_height();
    render();
});
// Shifting event listeners
document.getElementById("shift_right").addEventListener("click", function () { 
    for (let row = 0; row < row_count; row++) {
        current_state[row].pop();
        current_state[row].unshift(0);
    }
    render();
});
document.getElementById("shift_left").addEventListener("click", function () { 
    for (let row = 0; row < row_count; row++) {
        current_state[row].shift();
        current_state[row].push(0);
    }
    render();
});
document.getElementById("shift_down").addEventListener("click", function () { 
    current_state.pop()
    current_state.unshift(Array(col_count).fill(0))
    render();
});
document.getElementById("shift_up").addEventListener("click", function () { 
    current_state.shift()
    current_state.push(Array(col_count).fill(0))
    render();
});
// Misc event listeners
document.getElementById("fps").addEventListener("click", function () {
    fps=(document.getElementById("fps").value);
});
document.getElementById("set").addEventListener("click", function () { 
    initial_state = JSON.parse(JSON.stringify(current_state));
    render();
});
document.getElementById("return").onclick = function () { 
    current_state = JSON.parse(JSON.stringify(initial_state));
    render();
};
document.getElementById("clear").onclick = function () { 
    current_state = Array(row_count).fill(null)
    .map(() => new Array(col_count).fill(null)
        .map(() => 0));
        render();
};
document.getElementById("invert").onclick = function () { 
    for (let row = 0; row < row_count; row++) {
        for (let col = 0; col < col_count; col++){
            current_state[row][col] = current_state[row][col] ? 0 : 1;
        }
    }
    render();
};
// Window resize event listener
window.addEventListener('resize', 
    function () {
        width_height();
        render();
    }
);
// Click event listeners
canvas.addEventListener('click', 
    function (event) {
        var boundingRect = event.target.getBoundingClientRect();
        var x = event.clientX - boundingRect.left;
        var y = event.clientY - boundingRect.top;

        var col = Math.floor(x / grid_spacing);
        var row = Math.floor(y / grid_spacing);

        current_state[row][col] = current_state[row][col] ? 0 : 1;
        render();
    }
);
// Key event listeners
window.addEventListener('keydown', function (e) {
    if (e.keyCode == '37' || e.keyCode == '38' || e.keyCode == '39' || e.keyCode == '40') {
        e.preventDefault();
    }
});
window.addEventListener('keyup', function (event) {
    if (event.keyCode == '80') {
        paused = paused ? false : true;
        document.getElementById("playback").value = paused ? "Play" : "Pause";
        current_state = next_generation(current_state);
        requestAnimationFrame(animate);
    }
    else if (event.keyCode == '38') {
        // up arrow
        current_state.shift()
        current_state.push(Array(col_count).fill(0))
        render();
    }
    else if (event.keyCode == '40') {
        // down arrow
        current_state.pop()
        current_state.unshift(Array(col_count).fill(0)) 
        render();
    }
    else if (event.keyCode == '37') {
       // left arrow
        for (let row = 0; row < row_count; row++) {
            current_state[row].shift();
            current_state[row].push(0);
        }
        render();
    }
    else if (event.keyCode == '39') {
       // right arrow
        for (let row = 0; row < row_count; row++) {
            current_state[row].pop();
            current_state[row].unshift(0);
        }
        render();
    }
});
// Playback resize listeners
document.getElementById("playback").onclick = function () { 
    paused = paused ? false : true;
    document.getElementById("playback").value = paused ? "Play" : "Pause";
    current_state = next_generation(current_state);
    requestAnimationFrame(animate);
};
// Fill in form
document.getElementById("fill").onclick = function () { 
    document.getElementById("id_state").value = JSON.stringify(initial_state)
};


// Functions
function width_height() {
    canvas.width = 0.8 * window.innerWidth;
    canvas.height = canvas.width / 2;
    grid_spacing = canvas.width / col_count;
};
function animate() {
    if(paused){return;}

    // Animation
    render(current_state)
    current_state = next_generation(current_state);

    // request another animation loop
    setTimeout(function () {requestAnimationFrame(animate);}, 1000 / fps)
};
function render() {
    // ctx.restore()
    for (let row = 0; row < row_count; row++) {
        for (let col = 0; col < col_count; col++){
            ctx.fillStyle = current_state[row][col] ? 'rgb(0, 0, 0)' : 'rgb(255, 255, 255)';
            // ctx.fillStyle = cell ? 'rgb(200, 200, 200)' : 'rgb(225, 250, 245)';
            ctx.fillRect(col * grid_spacing,row * grid_spacing, grid_spacing, grid_spacing);
        }
    }
};
function next_generation(grid) {
    const next_gen = grid.map(arr => [...arr]);

    for (let row = 0; row < row_count; row++) {
        for (let col = 0; col < col_count; col++){
            let cell = grid[row][col]
            let neighbor_count = 0
            // loop over neighbors
            for (let i =- 1; i < 2; i++) {
                for (let j =- 1; j < 2; j++) {
                    if (i === 0 && j === 0) {
                        continue;
                    }
                    
                    if ((row + i) >= 0 && (row + i) < row_count && (col + j) >= 0 && (col + j) < col_count) {
                        neighbor_count += grid[row + i][col + j];
                    }
                }
            }
            // rules determine next generation (next_gen)
            if (cell == 1 && (neighbor_count == 2 || neighbor_count == 3)) {
                next_gen[row][col] = 1;
            } else if (cell == 0 && neighbor_count  == 3) {
                next_gen[row][col] = 1;
            } else {
                next_gen[row][col] = 0;
            }
        }
    }
    return next_gen;        
};


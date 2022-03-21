const canvas = document.getElementById("state"); // id of canvas must be state
const ctx = canvas.getContext("2d");
var paused = true;
var fps = 20;

// initialize canvas size
canvas.width = 0.8 * window.innerWidth;
canvas.height = canvas.width / 2;

// set default git
var col_count = 100;
var row_count = col_count / 2;
var grid_spacing = canvas.width / col_count
// initial empty grid
var initial_state = Array(row_count).fill(null)
    .map(() => new Array(col_count).fill(null)
        .map(() => 0));
        
width_height();
current_state = JSON.parse(JSON.stringify(initial_state));
render(current_state, grid_spacing);


// Event listeners
document.getElementById("grid_size").addEventListener("change", function () {
    var select = document.getElementById('grid_size');
    var option = select.options[select.selectedIndex];
    var val = option.value;
    if (val == "s") {
        col_count = 50;
        row_count = 25;
    } else if (val == "m"){
        col_count = 100;
        row_count = 50;
    } else if (val == "l"){
        col_count = 200;
        row_count = 100;
    } else if (val == "x") {
        col_count = 300;
        row_count = 150;
    }
            
    width_height();

    initial_state = Array(row_count).fill(null)
        .map(() => new Array(col_count).fill(null)
            .map(() => 0)); // Math.floor(Math.random() * 2)
    current_state = JSON.parse(JSON.stringify(initial_state));
    render(current_state, grid_spacing);
});

// Shifting event listeners
document.getElementById("shift_right").addEventListener("click", function () { 
    for (let row = 0; row < row_count; row++) {
        current_state[row].pop();
        current_state[row].unshift(0);
    }
    render(current_state, grid_spacing);
});
document.getElementById("shift_left").addEventListener("click", function () { 
    for (let row = 0; row < row_count; row++) {
        current_state[row].shift();
        current_state[row].push(0);
    }
    render(current_state, grid_spacing);
});
document.getElementById("shift_down").addEventListener("click", function () { 
    current_state.pop()
    current_state.unshift(Array(col_count).fill(0))
    render(current_state, grid_spacing);
});
document.getElementById("shift_up").addEventListener("click", function () { 
    current_state.shift()
    current_state.push(Array(col_count).fill(0))
    render(current_state, grid_spacing);
});
// Misc event listeners
document.getElementById("fps").addEventListener("click", function () {
    fps=(document.getElementById("fps").value);
});
document.getElementById("set").addEventListener("click", function () { 
    initial_state = JSON.parse(JSON.stringify(current_state));
    render(current_state, grid_spacing);
});
document.getElementById("return").onclick = function () { 
    current_state = JSON.parse(JSON.stringify(initial_state));
    render(current_state, grid_spacing);
};
document.getElementById("clear").onclick = function () { 
    current_state = Array(row_count).fill(null)
    .map(() => new Array(col_count).fill(null)
        .map(() => 0));
        render(current_state, grid_spacing);
};
document.getElementById("invert").onclick = function () { 
    for (let row = 0; row < row_count; row++) {
        for (let col = 0; col < col_count; col++){
            current_state[row][col] = current_state[row][col] ? 0 : 1;
        }
    }
    render(current_state, grid_spacing);
};
// Window resize event listener
window.addEventListener('resize', 
    function () {
        width_height();
        render(current_state, grid_spacing);
    }
);
// Input event listeners
canvas.addEventListener('click', 
    function (event) {
        var boundingRect = event.target.getBoundingClientRect();
        var x = event.clientX - boundingRect.left;
        var y = event.clientY - boundingRect.top;

        var col = Math.floor(x / grid_spacing);
        var row = Math.floor(y / grid_spacing);
        console.log(x, y,grid_spacing)
        current_state[row][col] = current_state[row][col] ? 0 : 1;
        render(current_state, grid_spacing);
    }
);
window.addEventListener('keyup', event => {
    if (event.code === 'Space') {
        paused = paused ? false : true;
        document.getElementById("playback").value = paused ? "Play" : "Pause";
        current_state = next_generation(current_state);
        requestAnimationFrame(animate);
    }
});
// Playback resize listeners
document.getElementById("playback").onclick = function () { 
    paused = paused ? false : true;
    document.getElementById("playback").value = paused ? "Play" : "Pause";
    current_state = next_generation(current_state);
    requestAnimationFrame(animate);
};

// Functions
function width_height() {
    canvas.width = 0.8 * window.innerWidth;
    canvas.height = canvas.width / 2;
    grid_spacing = canvas.width / col_count;
}

function animate() {
    if(paused){return;}

    // Animation
    render(current_state)
    current_state = next_generation(current_state);

    // request another animation loop
    setTimeout(function () {requestAnimationFrame(animate);}, 1000 / fps)
}
function render(grid) {
    // ctx.restore()
    for (let row = 0; row < row_count; row++) {
        for (let col = 0; col < col_count; col++){
            let cell = grid[row][col]
            ctx.fillStyle = cell ? 'rgb(0, 0, 0)' : 'rgb(255, 255, 255)';
            // ctx.fillStyle = cell ? 'rgb(200, 200, 200)' : 'rgb(225, 250, 245)';
            ctx.fillRect(col * grid_spacing,row * grid_spacing, grid_spacing, grid_spacing);
        }
    }
}

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
}


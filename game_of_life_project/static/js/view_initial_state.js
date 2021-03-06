const canvas = document.getElementById("state"); // id of canvas must be state
const ctx = canvas.getContext("2d");
var paused = true;
var fps = 20;

const initial_state = window.initial_state
const row_count = initial_state.length;
const col_count = 2*row_count;

width_height();
current_state = JSON.parse(JSON.stringify(initial_state));
render(current_state, grid_spacing);

document.getElementById("return").onclick = function () { 
    current_state = JSON.parse(JSON.stringify(initial_state));
    render(current_state, grid_spacing);
};

window.addEventListener('resize', 
    function () {
        width_height();
        render(current_state, grid_spacing);
    }
);
window.addEventListener('keydown', function (e) {
    if (e.keyCode == '32') {
        e.preventDefault();
    }
});
window.addEventListener('keyup', event => {
    if (event.code === 'Space') {
        paused = paused ? false : true;
        document.getElementById("playback").value = paused ? "Play" : "Pause";
        current_state = next_generation(current_state);
        requestAnimationFrame(animate);
    }
});
// Playback listeners
document.getElementById("playback").onclick = function () { 
    paused = paused ? false : true;
    document.getElementById("playback").value = paused ? "Play" : "Pause";
    current_state = next_generation(current_state);
    requestAnimationFrame(animate);
};

document.getElementById("fps").addEventListener("click", function () {
    fps=(document.getElementById("fps").value);
});

// Functions
function width_height() {
    canvas.width = 0.8 * window.innerWidth;
    canvas.height = canvas.width / 2;
    grid_spacing = canvas.width / col_count
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

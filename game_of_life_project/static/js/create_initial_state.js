const canvas = document.getElementById("state"); // id of canvas must be state
const ctx = canvas.getContext("2d");

canvas.width = 0.8 * window.innerWidth;
canvas.height = canvas.width / 2;
canvas.style = "position:absolute; left: 50%; width: 400px; margin-left: -200px;";

const col_count = 50;
const row_count = col_count / 2;

var grid_spacing = canvas.width / col_count

// 2d array
let grid = Array(row_count).fill(null)
    .map(() => new Array(col_count).fill(null)
        .map(() => 0)); // Math.floor(Math.random() * 2)
width_height();
render(grid, ctx);

// Event listeners
window.addEventListener('resize', 
    function () {
        width_height();
        render(grid, ctx);
    }
);
canvas.addEventListener('click', 
    function (event) {
        var boundingRect = event.target.getBoundingClientRect();
        var x = event.clientX - boundingRect.left;
        var y = event.clientY - boundingRect.top;

        var col = Math.floor(x / grid_spacing);
        var row = Math.floor(y / grid_spacing);
        console.log(x, y,grid_spacing)
        grid[row][col] = grid[row][col] ? 0 : 1;
        render(grid, ctx);
    }
)
window.addEventListener('keyup', event => {
    if (event.code === 'Space') {
        grid = next_generation(grid)
        render(grid);
    }
});

// Functions
function width_height() {
    canvas.width = 0.8 * window.innerWidth;
    canvas.height = canvas.width / 2;
    grid_spacing = canvas.width / col_count
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


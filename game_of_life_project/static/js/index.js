function update(grid, ctx) {
    next_grid = next_generation(grid);
    render(next_grid, ctx);
    setTimeout(update,1);
}
function next_generation(grid) {
    const next_gen = grid.map(arr => [...arr]);

    for (let col = 0; col < grid.length; col++) {
        for (let row = 0; row < grid[col].length; row++){
            const cell = grid[col][row]
            let neighbor_count = 0
            // loop over neighbors
            for (let i =- 1; i < 2; i++) {
                for (let j =- 1; j < 2; j++) {
                    if (i === 0 && j === 0) {
                        continue;
                    }
                    const x_cell = col + i;
                    const y_cell = row + j;
                    
                    if (x_cell >= 0 && y_cell >= 0 && x_cell < col_count && y_cell < row_count) {
                        const current_neighbour = grid[col + i][row + j];
                        neighbor_count += current_neighbour; 
                    }
                }
            }
            // rules determine next generation (next_gen)
            if (cell === 1 && neighbor_count < 2) {
                next_gen[col][row] = 0;
            } else if (cell === 1 && neighbor_count > 3) {
                next_gen[col][row] = 0;
            } else if (cell === 0 && neighbor_count  == 3) {
                next_gen[col][row] = 1;
            }
        }
    }
    return next_gen;        
}
function render(grid, ctx) {
    for (let col = 0; col < grid.length; col++) {
        for (let row = 0; row < grid[col].length; row++){
            const cell = grid[col][row]
            ctx.beginPath();
            ctx.rect(col * grid_spacing, row * grid_spacing, grid_spacing, grid_spacing);
            ctx.fillStyle = cell ? 'rgb(200, 200, 200)' : 'rgb(225, 250, 245)';
            ctx.fill();
            // ctx.strokeStyle = 'rgb(200, 200, 200)' 
            // ctx.stroke();
        }
    }
}

var canvases = document.getElementsByClassName('liked_state');
var grid_spacing = 5

for (let i = 0;i < canvases.length; i++) {
    console.log(canvases[i])
    const canvas = canvases[i]
    const ctx = canvas.getContext("2d");
    
    canvas.width = 400;
    canvas.height = 200;

    var row_count = Math.floor(canvas.height / grid_spacing) + 1
    var col_count = Math.floor(canvas.width / grid_spacing) + 1

    // 2d array
    let grid = Array(col_count).fill(null)
        .map(() => new Array(row_count).fill(null)
            .map(() => Math.floor(Math.random() * 2)));

    update(grid, ctx)

}

var canvases = document.getElementsByClassName('recent_state');
var grid_spacing = 5

for (let i = 0;i < canvases.length; i++) {
    console.log(canvases[i])
    const canvas = canvases[i]
    const ctx = canvas.getContext("2d");
    
    canvas.width = 400;
    canvas.height = 200;

    var row_count = Math.floor(canvas.height / grid_spacing) + 1
    var col_count = Math.floor(canvas.width / grid_spacing) + 1

    // 2d array
    let grid = Array(col_count).fill(null)
        .map(() => new Array(row_count).fill(null)
            .map(() => Math.floor(Math.random() * 2)));

    update(grid, ctx)

}

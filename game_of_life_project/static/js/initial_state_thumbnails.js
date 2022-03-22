var canvases = document.getElementsByClassName('state');
state_list = window.state_list;

for (let i = 0;i < canvases.length; i++) {
    var row_count = state_list[i].length;
    var col_count = 2*row_count;
    var state = state_list[i];
    var canvas = canvases[i];
    var ctx = canvas.getContext("2d");
    
    canvas.width = 400;
    canvas.height = 200;

    var grid_spacing = canvas.width / col_count
    console.log(state)
    render(state, grid_spacing)

}

//  Functions
function render(grid, grid_spacing) {
    for (let row = 0; row < grid.length; row++) {
        for (let col = 0; col < grid[row].length; col++){
            const cell = grid[row][col]
            ctx.fillStyle = cell ? 'rgb(0, 0, 0)' : 'rgb(255, 255, 255)';
            ctx.fillRect(col * grid_spacing,row * grid_spacing, grid_spacing, grid_spacing);
        }
    }
}

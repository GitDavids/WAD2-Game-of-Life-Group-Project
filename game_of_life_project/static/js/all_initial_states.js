var canvases_liked = document.getElementsByClassName('state');
state_list = window.state_list;

for (let i = 0;i < canvases_liked.length; i++) {
    var col_count = state_list[i][0];
    var row_count = col_count / 2;
    var state = state_list[i][1];
    var canvas = canvases_liked[i];
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
function render(grid, ctx, grid_spacing) {
    for (let col = 0; col < grid.length; col++) {
        for (let row = 0; row < grid[col].length; row++){
            const cell = grid[col][row]
            ctx.beginPath();
            ctx.rect(col * grid_spacing, row * grid_spacing, grid_spacing, grid_spacing);
            ctx.fillStyle = cell ? 'rgb(0, 0, 0)' : 'rgb(255, 255, 255)';
            ctx.fill();
            // ctx.strokeStyle = 'rgb(200, 200, 200)' 
            // ctx.stroke();
        }
    }
}

var canvases_liked = document.getElementsByClassName('state');

for (let i = 0;i < canvases_liked.length; i++) {
    console.log(canvases_liked[i])
    var canvas = canvases_liked[i]
    const ctx = canvas.getContext("2d");
    
    canvas.width = 400;
    canvas.height = 200;

    var col_count = 50;
    var row_count = col_count / 2;

    var grid_spacing = canvas.width / col_count

    // 2d array
    let grid = Array(col_count).fill(null)
        .map(() => new Array(row_count).fill(null)
            .map(() => Math.floor(Math.random() * 2)));

    render(grid, ctx, grid_spacing)

}
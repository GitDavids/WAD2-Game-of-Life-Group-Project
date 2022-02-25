document.addEventListener('visibilitychange', function (event) {
    if (document.hidden) {
        console.log('not visible');
    } else {
        console.log('is visible');
    }
});
var pswpElement = document.querySelectorAll('.pswp')[0];

var items = [
    {
        src: '/api/images?id=1',
        w: 800,
        h: 500
    },
    {
        src: '/api/images?id=3',
        w: 1200,
        h: 900
    }
];

var options = {
    index: 0
};

// Initializes and opens PhotoSwipe
var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
gallery.init();

console.log(items);

var

ReactDOM.render(
    <Program page={0}/>,
    document.getElementById("program")
)
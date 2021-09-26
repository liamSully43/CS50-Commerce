document.querySelector("input[name='image']").addEventListener("change", function(e) {
    console.log
    const image = document.querySelector("#image-preview");
    image.src = e.path[0].value;
})
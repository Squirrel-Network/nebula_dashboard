document.addEventListener("DOMContentLoaded", () => {
    console.log("1");
    var day = new Date();
    var year = day.getFullYear();

    document.getElementById("year").innerHTML = year;
});